__author__ = 'Tauren'

import unittest

from parser import AddressParser

from app.geocoder.address import Address

class TestParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_address_string(self):
        address =  Address('6 caputo drive manorville ny 11949')
        AddressParser().parse_address_string(address)

        assert address.number == '6'
        assert address.zip == '11949'
        assert address.state == 'NY'

if __name__ == '__main__':
    unittest.main()