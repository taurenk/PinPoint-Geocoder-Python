__author__ = 'Tauren'

import logging
from app import db
from app.models import Place, AddrFeat, AddressResult
from .address import Address
from .parser import AddressParser
from .metaphone import meta
from .ranking import rank_city_candidates, rank_address_results
from sqlalchemy import text
from .utils.geo_utils import convert_geom_to_points
logger = logging.getLogger('geocoder')


class Geocoder:
    def __init__(self):
        self.metaphone = meta()
        self.address_parser = AddressParser()

    def geocode(self, address_string):
        address = self.address_parser.parse_address_string(Address(address_string))
        logger.info("Geocoding: %s" % address)
        print('Geocoding: %s' % address)

        results = []
        if address.address_line_1:
            results = self.geocode_address(address)

        if len(results) == 0:
            if address.city == None:
                address.city = address.address_line_1
                address.address_line_1 = None
            results = self.geocode_city(address)

        logger.info("Found %s Results." % len(results))
        return results

    def geocode_address(self, address):
        logger.info("Geocode Address %s" % address)

        address, places = self.find_city(address)

        if (address.address_line_1 == None or address.address_line_1 == '') and address.city:
            logger.info("Extracted city from address line. Not Street left.")
            return []

        zips = [place.zip for place in places]
        addr_candidates = self.addrfeat_by_street_and_zips(address.address_line_1, zips)

        if addr_candidates == []:
            addr_candidates = self.addrfeat_by_street_and_zips_fuzzy(address.address_line_1, zips)

        results = [self.build_address_result(address, addrfeat, places)
                   for addrfeat in addr_candidates]

        results = rank_address_results(address.address_line_1, address.city, address.state, address.zip, results)

        for i in range(3):
            logger.info("Address Result: #%s - %s " % (i, results[0]))
        return results

    def geocode_city(self, address):
        logger.info("Geocoding city for address %s" % address)

        address, places = self.find_city(address)

        if places:
            ranked_places = rank_city_candidates(address.city, address.state, address.zip, places)
            results = [AddressResult(address.original_address_string, "city", place.score,
                                     None, None, place.city, place.state_code, place.zip,
                                     lat=place.latitude, lon=place.longitude) for place in ranked_places]
            return [result for result in results if result.score > 0]
        else:
            return []

    def find_city(self, address):
        places = []
        if address.zip:
            places = self.places_by_zip(address.zip)

        if address.address_line_1:
            address_tokens = self.tokenize_street(address.address_line_1)
            places += self.places_by_city(address_tokens)
        elif address.city:
            places += self.places_by_city([address.city])

        if places and address.city == None:
            address = self.extract_city(address, places)

        return address, places

    def extract_city(self, address, places):
        logger.info("Extracting City From Address: %s" % address)
        for place in places:
            if place.city in address.address_line_1:
                logger.info("Extracted city '%s' from address line 1 '%s'" % (place.city ,address.address_line_1 ))
                address.city = place.city
                address.address_line_1 = address.address_line_1.replace(address.city, '').strip()

        return address

    def tokenize_street(self, address_line):
        street_tokens = [address_line]

        if address_line.count(" ") > 0:
            tokens = address_line.split(" ")
            street_tokens.append(tokens[-1])
            street_tokens.append(tokens[-2] + " " + tokens[-1])
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

        address_result = AddressResult(address.original_address_string, "street", score=0,
                                       primary_number=address.number, street_fullname=addrfeat.fullname)

        address_result.addrfeat_record = addrfeat
        address_result.tlid = str(addrfeat.tlid)

        for place in place_candidates:
            if place.zip == addrfeat.zipr or place.zip == addrfeat.zipl:
                address_result.zipcode = place.zip
                address_result.city_name = place.city
                address_result.state_abbreviation = place.state_code
        return address_result

