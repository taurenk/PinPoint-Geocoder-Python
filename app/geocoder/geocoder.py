__author__ = 'Tauren'

import logging
from app import db
from app.models import Place, AddrFeat
from .address import Address
from .parser import AddressParser
from .metaphone import meta
from .ranking import rank_city_candidates

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
            print('res: %s' % results)

        if len(results) == 0 and address.address_line_1:
            address.city = address.address_line_1
            address.address_line_1 = None
            results = self.geocode_city(address)

        return results

    def geocode_city(self, address):
        logger.info("Geocoding city for address %s" % address)

        places = []
        if address.zip:
            places = self.places_by_zip(address.zip)

        if len(places) == 0 and address.city:
            # places = self.places_by_city(address.city, address.state, address.zip)
            places = self.places_by_city(address.city)

        if places:
            return rank_city_candidates(address.city, address.state, address.zip, places)
        else:
            return []

    def geocode_address(self, address):

        addr_feats = []
        place_candidates = self.geocode_city(address)

        if len(place_candidates) == 0:
            return []

        if place_candidates and address.city == None:
            for place_candidate in place_candidates:
                if place_candidate.city in address.address_line_1:
                    logger.info("")
                    address.city = place_candidate.city
                    address.address_line_1.replace(address.city, '')

        # Todo; tokenize address line string
        zips = [place.zip for place in place_candidates]
        addr_candidates = self.addrfeat_by_street_and_zips(address.address_line_1, zips)
        for a in addr_candidates:
            print("AC: %s" % a)
        return addr_feats

    def addrfeat_by_street_and_zips(self, street_name, zipcodes):
        primary, secondary = self.metaphone.process(street_name)
        filters = [AddrFeat.fullname_metaphone.in_([primary, secondary])]

        if zipcodes:
            filters.append(AddrFeat.zipl.in_(zipcodes))
            filters.append(AddrFeat.zipr.in_(zipcodes))

        results = db.session.query(AddrFeat).filter(*filters).all()
        logger.info("addrfeat_by_street_and_zips for street_name '%s' and zips '%s' results: %s" % (street_name, zipcodes, len(results)))
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



