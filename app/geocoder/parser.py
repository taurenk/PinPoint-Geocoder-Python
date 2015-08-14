__author__ = 'Tauren'

from app.geocoder.utils.regex import Regex
from app.geocoder.utils.standards import Standards


class AddressParser:

    def __init__(self):
        self.regex = Regex()
        self.standards = Standards()

    def parse_address_string(self, address):
        address_string = address.address_string.upper()

        zip = self.regex.zip_regex.search(address_string)
        if zip:
            address.zip = zip.group(0).strip()
            address_string = address_string.replace(address.zip, '').strip()

        state = self.regex.state_regex.search(address_string)
        print(state)

        if state:
            address.state = state.group(0).strip().upper()
            address_string = address_string[0:state.span()[0]]

            # State Standardization to abbreviation
            if address.state in Standards().states:
                address.state = self.standards.states[address.state.upper()]

        # TODO: What if pre text? What if number LIKE A701?
        number = self.regex.number_regex.search(address_string)
        if number:
            address.number = number.group(0).strip()
            address_string = address_string.replace(address.number, '').strip()
        address.address_line_1 = address_string
        return address