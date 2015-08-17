__author__ = 'Tauren'

import unittest

from app.geocoder.utils.regex import Regex
from app.geocoder.utils import standards

class TestRegex(unittest.TestCase):

    def setUp(self):
        self.regex = Regex()

    def test_street_types(self):
        address_tokens = ['6', 'CAPUTO', 'DRIVE']
        if address_tokens[-1] in self.regex.cannonical_street_types:
            assert self.regex.cannonical_street_types[address_tokens[-1]] == 'DR'
        else:
            assert False

if __name__ == '__main__':
    TestRegex()
