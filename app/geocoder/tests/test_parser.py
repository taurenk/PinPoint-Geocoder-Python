__author__ = 'Tauren'

import unittest

from app.geocoder.parser import AddressParser
from app.geocoder.address import Address


class TestParseAddressStrings(unittest.TestCase):

    def test_parse_simple_address_strings(self):
        address =  Address('6 caputo drive manorville ny 11949')
        AddressParser().parse_address_string(address)
        assert address.number == '6'
        assert address.zip == '11949'
        assert address.state == 'NY'

        address =  Address('1 McGuirk Street East Hampton new jersey 11949')
        AddressParser().parse_address_string(address)
        assert address.number == '1'
        assert address.zip == '11949'
        assert address.state == 'NJ'

    def test_parse_address_with_alphanumberic_number(self):
        address =  Address('1A CapUTO Street manorville South Carolina 11949')
        AddressParser().parse_address_string(address)
        assert address.number == '1A'
        assert address.zip == '11949'
        assert address.state == 'SC'

        address =  Address('1-A Caputo Street East Hampton California 11949')
        AddressParser().parse_address_string(address)
        assert address.number == '1-A'
        assert address.zip == '11949'
        assert address.state == 'CA'

class TestPostParseSimpleAddress(unittest.TestCase):

    def setUp(self):
        self.simple_address_1 =  Address('6 caputo drive manorville ny 11949')
        AddressParser().parse_address_string(self.simple_address_1)
        
    def test_post_parse_simple_address(self):
        pass

