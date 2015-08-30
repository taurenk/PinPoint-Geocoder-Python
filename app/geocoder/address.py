__author__ = 'Tauren'

class Address:

    def __init__(self, address_string):
        self.original_address_string = address_string
        self.address_string = address_string
        self.number = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.city = None
        self.state = None
        self.zip = None

    def __str__(self):
        """ Very helpful for testing!
        :return:
        """
        return '#: %s, line1: %s, city: %s, state: %s. zip: %s' % (self.number, self.address_line_1, self.city, self.state, self.zip)

    def to_json(self):
        return None