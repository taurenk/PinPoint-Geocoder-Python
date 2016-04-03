__author__ = 'Tauren'

import logging
from app import db
from app.models import Place
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

        # Currently Address Line 1 could be city or an actualy address line
        results = []
        if address.address_line_1:
            pass

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
        pass

    def places_by_zip(self, zipcode):
        results = db.session.query(Place).filter(Place.zip == zipcode).all()
        logger.info("places_by_zip for zip %s. results count: %s" % (zipcode, len(results)))
        return results

    def places_by_city(self, city, state_code=None, zip=None):
        # Todo; Should tokenize city into possible permutations
        primary, secondary = self.metaphone.process(city)

        queries = [Place.city_metaphone.in_([primary, secondary])]

        if state_code:
            queries.append(Place.state_code == state_code)

        if zip:
            queries.append(Place.zip == zip)

        results = db.session.query(Place).filter(*queries).all()
        logger.info("Places_by_city for city %s (DM: %s) results count: %s." % (city, primary, len(results)))
        return results


