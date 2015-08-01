__author__ = 'Tauren'

import traceback

from .address import Address
from .parser import AddressParser


class Geocoder:

    def __init__(self):
        pass

    def geocode(self, address_string):
        try:
            address = AddressParser().parse_address_string(Address(address_string))
        except Exception as error:
            print('Error occured while geocoding: %s' % error)
            print('Traceback: %s' % traceback.format_exc())

    def geocode_address(self):
        pass

    def geocode_zipcode(self):
        pass

