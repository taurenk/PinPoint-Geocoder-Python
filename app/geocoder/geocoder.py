__author__ = 'Tauren'

import traceback

from .address import Address
from .parser import AddressParser
from app.models import Place, AddrFeat

class Geocoder:

    def __init__(self, postgresql_connection):
        self.db = postgresql_connection

    def geocode(self, address_string):
        try:
            address = AddressParser().parse_address_string(Address(address_string))

            """ Try to figure out as much knowledge about the given data as possible:
                Case; Intersection - needs to pass 'intersection regex'
                Case; Normal Address
                Case; City/State/Zip
                    - Here we want to figure out what we can and return it!
            """
            # This is just for testing..
            if ' and ' in address.address_line_1:
                return {'Error': 'Intersections not yet supported.'}
            elif address.address_line_1:
                pass
            elif address.zip:
                pass
            else:
                return None # throw 404

        except Exception as error:
            print('Error occured while geocoding: %s' % error)
            print('Traceback: %s' % traceback.format_exc())

    def geocode_address(self):
        """ Try to further parse address in pieces.
        :return:
        """

    def geocode_zipcode(self):
        pass

    def places_by_zip(self, zipcode):
        # TODO; zipcodes should be 1 for 1; CONFIRM and DOCUMENT HERE.
        results = self.db.session.query(Place).filter(Place.zip == zipcode).all()
        return results

    def places_by_city(self, city):
        """ Given a city, using Postgresql fuzzy matching to retireve a list of potential places
        :param city:
        :return:
        """
        pass
