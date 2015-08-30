__author__ = 'Tauren'

import traceback

from app import db
from .address import Address
from .parser import AddressParser
from app.models import Place, AddrFeat

class Geocoder:

    def __init__(self):
        self.address_parser = AddressParser()

    def geocode(self, address_string):
        try:
            address = self.address_parser.parse_address_string(Address(address_string))

            """ Try to figure out as much knowledge about the given data as possible:
                Case; Intersection - needs to pass 'intersection regex'
                Case; Normal Address
                Case; City/State/Zip
                    - Here we want to figure out what we can and return it!
            """
            if address.address_line_1:
                print('geocoding address...')
                self.geocode_address(address)
            elif address.zip:
                pass
            else:
                return None  # throw 404

        except Exception as error:
            print('Error occured while geocoding: %s' % error)
            print('Traceback: %s' % traceback.format_exc())

    def geocode_address(self, address):
        potential_places = []
        if address.zip:
            potential_places.append(self.places_by_zip(address.zip))

        # We get alot of "noise" back in this, so only save off what we actually need
        # Todo future: think about ranking them and taking top x ranked guesses.
        address, guessed_place = self.extract_city(address, potential_places)
        if guessed_place:
            print('\t-We found the city [1-1]: %s' % guessed_place)
        else:
            guessed_places = self.guess_city(address.address_line_1)
            guessed_places += potential_places

            print('-Guessing City: %s' % address.address_line_1)
            address, guessed_place = self.extract_city(address, guessed_places)
            print('-Guessed_Place: %s' % guessed_place)

        if not guessed_place:
            print('\t>>Cannot find a for given address string: %s' % address)
            # Todo; geocode zip if available?
            return None

        potential_places.append(guessed_place)
        print('-AddrFeat search for <%s>' % address.address_line_1)

        """Will need to apply post parse logic as street names (fullname) are stored in dataset with standardization.
        This is particularly difficult due to the may factors that are in an address string,
        such as pre/post dir + types and the latter being in the acutal street name [EAST ST]
        * Acutally, should try to tokenize the entire address and try combinations...
        """
        address = self.address_parser.post_parse_address(address)

        print('-Searching for address: <%s>' % address.address_line_1)

        potential_addrfeats = self.addrfeats_by_street(address.address_line_1)
        print('-Potential AddrFeats:')
        [print('\t%s' % addrfeat) for addrfeat in potential_addrfeats]
        return potential_addrfeats

    def extract_city(self, address, potential_places):
        """ Given a list of potential strings, return
        :param address:
        :param potential_places:
        :return:
        """
        sorted_list = sorted(potential_places, key=lambda k: k.city)
        for place in sorted_list:
            print('Potential City: %s' % place)
            # TODO: Fuzzy match this!
            if place.city in address.address_line_1:
                address.address_line_1 = address.address_line_1.replace(place.city, '').strip()
                address.city = place.city
                return address, place
        return address, None

    def guess_city(self, address_string):
        tokens = address_string.split(' ')[-3:]
        guess_tokens = []
        # make all combinations of tokens
        for idx, token in enumerate(tokens):
            guess_tokens.append(token)
            if idx == 1:
                guess_tokens.append('%s %s' % (guess_tokens[0], token))
            if idx == 2:
                guess_tokens.append('%s %s' % (guess_tokens[0], token))
                guess_tokens.append('%s %s' % (guess_tokens[1], token))
        guessed_places = self.places_by_city_list(guess_tokens)
        return guessed_places

    def geocode_zipcode(self, zipcode):
        """ Given a zipcode, return a matching Place.
        :param zipcode:
        :return: Place
        """
        results = self.places_by_zip(zipcode)
        if results:
            return results
        return None

    def places_by_zip(self, zipcode):
        # Zipcodes should match 1 for 1 (uniquly), so return only one result.
        results = db.session.query(Place).filter(Place.zip == zipcode).one()
        return results

    def places_by_city(self, city):
        """ Given a city, using Postgresql fuzzy matching to retireve a list of potential places
        :param city:
        :return:
        """
        # Let's change this to get 'fuzzy results'
        results = db.session.query(Place).filter(Place.city == city).all()
        return results

    def places_by_city_list(self, city_list):
        results = db.session.query(Place).filter(Place.city.in_(city_list)).all()
        return results

    def addrfeats_by_street(self, street):
        results = db.session.query(AddrFeat).filter(AddrFeat.fullname == street).all()
        return results

