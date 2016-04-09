__author__ = 'Tauren'

import logging
from app import db
from app.models import Place, AddrFeat, AddressResult
from .address import Address
from .parser import AddressParser
from .metaphone import meta
from .ranking import rank_city_candidates, rank_address_candidates
from sqlalchemy import text

logger = logging.getLogger('geocoder')


class Geocoder:
    def __init__(self):
        self.metaphone = meta()
        self.address_parser = AddressParser()

    def geocode(self, address_string):
        address = self.address_parser.parse_address_string(Address(address_string))
        print('Geocoding Address: %s' % address)
        # Currently Address Line 1 could be city or an actualy address line
        results = []
        if address.address_line_1:
            results = self.geocode_address(address)
            print('geocode address res: %s' % results)

        if len(results) == 0:
            print('Found 0 results, geocoding city')
            address.city = address.address_line_1
            address.address_line_1 = None
            results = self.geocode_city(address)

        return results

    def geocode_city(self, address):
        logger.info("Geocoding city for address %s" % address)
        print("Geocoding city for address %s" % address)

        places = []
        if address.zip:
            places = self.places_by_zip(address.zip)

        if len(places) == 0 and address.city:
            places = self.places_by_city(address.city)

        if places:
            ranked_places = rank_city_candidates(address.city, address.state, address.zip, places)
            results = [AddressResult(address.original_address_string, place.score, "city",
                                     None, None, place.city, place.state_code, place.zip,
                                     lat=place.latitude, lon=place.longitude) for place in ranked_places]
            return results
        else:
            return []

    def geocode_address(self, address):
        logger.info("Geocoding address for address %s" % address)

        place_candidates = []
        if address.zip:
            place_candidates = self.places_by_zip(address.zip)
        if len(place_candidates) == 0 and address.city:
            place_candidates = self.places_by_city(address.city)

        if len(place_candidates) == 0:
            return []

        # Match State OR Zip
        if place_candidates and address.city == None:
            for place_candidate in place_candidates:
                if place_candidate.city in address.address_line_1:
                    address.city = place_candidate.city.strip()
                    address.address_line_1 = address.address_line_1.replace(address.city, '').strip()

        print("Address Now: %s" % address)
        if address.address_line_1 == None and address.city:
            # Return to city geocoder, for now (all though this seems to be a waste).
            return []

        # Todo; tokenize address line string
        zips = [place.zip for place in place_candidates]
        addr_candidates = self.addrfeat_by_street_and_zips(address.address_line_1, zips)
        for a in addr_candidates:
            print("AddrFeat Candidate: %s" % a)

        results = [self.build_address_result(address, addrfeat, place_candidates)
                   for addrfeat in addr_candidates]
        return results

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

    def places_by_city(self, city, state_code=None, zip=None):
        # Todo; Should tokenize city into possible permutations
        primary, secondary = self.metaphone.process(city)

        filters = [Place.city_metaphone.in_([primary, secondary])]
        if state_code:
            filters.append(Place.state_code == state_code)

        if zip:
            filters.append(Place.zip == zip)

        results = db.session.query(Place).filter(*filters).all()
        logger.info("Places_by_city for city %s (DM: %s) results count: %s." % (city, primary, len(results)))
        return results

    def build_address_result(self, address, addrfeat, place_candidates):

        address_result = AddressResult(address.original_address_string, None, "street",
                                       address.number, addrfeat.fullname)
        for place in place_candidates:
            if place.zip == addrfeat.zipr or place.zip == addrfeat.zipl:
                address_result.zipcode = place.zip
                address_result.city_name = place.city
                address_result.state_abbreviation = place.state_code

        return address_result
