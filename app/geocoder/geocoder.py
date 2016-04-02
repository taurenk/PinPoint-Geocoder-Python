__author__ = 'Tauren'

import logging
from app import db
from app.models import Place
from .address import Address
from .parser import AddressParser
from .metaphone import meta

logger = logging.getLogger('geocoder')


class Geocoder:
    def __init__(self):
        self.metaphone = meta()
        self.address_parser = AddressParser()

    def geocode(self, address_string):
        address = self.address_parser.parse_address_string(Address(address_string))

    def geocode_city(self, address):
        logger.info("Geocoding city for address %s" % address)

        places = []
        if address.zip:
            places = self.places_by_zip(address.zip)

        if len(places) == 0 and address.city:
            places = self.places_by_city(address.city)

    def geocode_address(self, address):
        pass

    def places_by_zip(self, zipcode):
        # Are there Duplicate Zip Codes?
        results = db.session.query(Place).filter(Place.zip == zipcode).one()
        return results

    def places_by_city(self, city):
        # This should tokenize the city better.
        primary, secondary = self.metaphone.process(city)

        results = db.session.query(Place) \
            .filter(Place.city_metaphone.in_([primary, secondary])) \
            .all()
        return results


