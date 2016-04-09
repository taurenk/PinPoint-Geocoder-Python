__author__ = 'Tauren'

import re
from app.geocoder.utils.regex import Regex
from app.geocoder.utils.standards import Standards


class AddressParser:

    def __init__(self):
        self.regex = Regex()
        self.standards = Standards()

    def parse_address_string(self, address):
        address_string = address.address_string.upper()

        # Remove excess spaces + commas
        address_string = re.sub('\s\s+', '', address_string)
        address_string = address_string.replace(',', '')

        zip = self.regex.zip_regex.search(address_string)
        if zip:
            address.zip = zip.group(0).strip()
            address_string = address_string.replace(address.zip, '').strip()

        state = self.regex.state_regex.search(address_string)

        if state:
            address.state = state.group(0).strip().upper()
            address_string = address_string[0:state.span()[0]]

            # State Standardization to abbreviation
            if address.state in Standards().states:
                address.state = self.standards.states[address.state.upper()]

        number = self.regex.number_regex.search(address_string)
        if number:
            address.number = number.group(0).strip()
            address_string = address_string.replace(address.number, '').strip()
        address.address_line_1 = address_string.title().strip()
        return address

    def post_parse_address(self, address):
        """
        :param address:
        :return: address object
        """
        # Crudely standardize address
        street_tokens = address.address_line_1.split(' ')

        # Take first value in street and see if we can standardize it.
        if street_tokens[-1] in self.regex.cannonical_street_types:
            # swap value to standard abbreviation
            street_tokens[-1] = self.regex.cannonical_street_types[street_tokens[-1]]

        address.address_line_1 = ' '.join(street_tokens)
        return address