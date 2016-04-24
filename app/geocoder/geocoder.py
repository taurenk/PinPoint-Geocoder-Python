__author__ = 'Tauren'

import logging
from app import db
from app.models import Place, AddrFeat, AddressResult
from .address import Address
from .parser import AddressParser
from .metaphone import meta
from .ranking import rank_city_candidates, rank_address_results
from sqlalchemy import text

logger = logging.getLogger('geocoder')


class Geocoder:
    def __init__(self):
        self.metaphone = meta()
        self.address_parser = AddressParser()

    def geocode(self, address_string):

        address = self.address_parser.parse_address_string(Address(address_string))
        logger.info("Geocoding: %s" % address)

        results = []
        if address.address_line_1:
            results = self.geocode_address(address)

        if results == []:
            results = self.geocode_city(address)

        logger.info("Found %s Results." % len(results))
        return results

    def geocode_address(self, address):
        logger.info("Geocode Address %s" % address)

        # We will never initially parse a city from a street
        place_candidates = self._find_city_candidates(address.address_line_1, address.city, address.zip)
        new_street_string, found_city = self._extract_city_from_street(address.address_line_1, place_candidates)

        if new_street_string and found_city:
            address.address_line_1 = new_street_string
            address.city = found_city

        if (address.address_line_1 == None or address.address_line_1 == ''):
            logger.info("No Street Found in Address.")
            return []

        zips = [place.zip for place in place_candidates]

        address.address_line_1 = self.address_parser.standardize_street_string(address.address_line_1)
        addr_candidates = self.addrfeat_by_street_and_zips(address.address_line_1, zips)

        if addr_candidates == []:
            addr_candidates = self.addrfeat_by_street_and_zips_fuzzy(address.address_line_1, zips)

        results = [self.build_address_result(address, addrfeat, place_candidates)
                   for addrfeat in addr_candidates]

        # results = rank_address_results(address.address_line_1, address.city, address.state, address.zip, results)
        return results

    def geocode_city(self, address):
        logger.info("Geocoding city for address %s" % address)

        place_candidates = self._find_city_candidates(address.address_line_1, address.city, address.zip)
        new_street_string, found_city = self._extract_city_from_street(address.address_line_1, place_candidates)

        if new_street_string and found_city:
            address.address_line_1 = new_street_string
            address.city = found_city

        ranked_places = rank_city_candidates(address.city, address.state, address.zip, place_candidates)
        results = [AddressResult(address.address_string,None,None,place,None) for place in ranked_places]
        return results

    def _find_city_candidates(self, street, city, zip):
        logger.info("Searching for City in Address <%s, %s, %s>" % (street, city, zip))
        places = []

        # TODO; the street tokens are too generic and yield way too many results
        #if street:
        #    address_tokens = self._tokenize_street(street)
        #    places += self.places_by_city(address_tokens)
        if city:
            places += self.places_by_city([city])
        if zip:
            places += self.places_by_zip(zip)

        return places

    def _extract_city_from_street(self, street, place_candidates):
        logger.info("place_candidates to Extract City From Street: %s" % street)
        for place in place_candidates:
            if place.city in street:
                logger.info("Extracted city '%s' from address line 1 '%s'" % (place.city, street))
                new_street_string = street.replace(place.city, '').strip()
                return new_street_string, place.city
        return None, None

    def _tokenize_street(self, address_line):
        street_tokens = [address_line]

        if address_line.count(" ") > 0:
            tokens = address_line.split(" ")
            street_tokens.append(tokens[-1])
            street_tokens.append(tokens[-2] + " " + tokens[-1])
        print(street_tokens)
        return street_tokens

    def addrfeat_by_street_and_zips(self, street_name, zipcodes):
        primary, secondary = self.metaphone.process(street_name)
        filters = [AddrFeat.fullname_metaphone.in_([primary, secondary])]

        if zipcodes:
            filters.append(AddrFeat.zipl.in_(zipcodes))
            filters.append(AddrFeat.zipr.in_(zipcodes))

        results = db.session.query(AddrFeat).filter(*filters).all()
        logger.info("addrfeat_by_street_and_zips for street_name '%s' and zips '%s' results: %s" % (
        street_name, zipcodes, len(results)))
        return results

    def addrfeat_by_street_and_zips_fuzzy(self, street_name, zipcodes):
        filters = [text("levenshtein(fullname, '%s') <= 3" % (street_name))]

        if zipcodes:
            filters.append(AddrFeat.zipl.in_(zipcodes))
            filters.append(AddrFeat.zipr.in_(zipcodes))

        results = db.session.query(AddrFeat).filter(*filters).all()

        logger.info("addrfeat_by_street_and_zips_fuzzy for street_name '%s' and zips '%s' results: %s" % (
        street_name, zipcodes, len(results)))
        return results

    def places_by_zip(self, zipcode):
        results = db.session.query(Place).filter(Place.zip == zipcode).all()
        logger.info("places_by_zip for zip %s. results count: %s" % (zipcode, len(results)))
        return results

    def places_by_city(self, city_strings, state_code=None, zip=None):

        metaphones = []
        for city in city_strings:
            primary, secondary = self.metaphone.process(city)
            metaphones.append(primary)
            metaphones.append(secondary)

        filters = [Place.city_metaphone.in_(metaphones)]
        if state_code:
            filters.append(Place.state_code == state_code)
        if zip:
            filters.append(Place.zip == zip)
        results = db.session.query(Place).filter(*filters).all()
        logger.info("Places_by_city for city %s (DM: %s) results count: %s." % (city_strings, metaphones, len(results)))
        return results

    def build_address_result(self, address, addrfeat, place_candidates):
        for place in place_candidates:
            if place.zip == addrfeat.zipr or place.zip == addrfeat.zipl:
                return AddressResult(address.original_address_string,address.number,addrfeat,place)

