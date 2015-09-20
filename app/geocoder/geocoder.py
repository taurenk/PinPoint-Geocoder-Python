__author__ = 'Tauren'

import traceback

from app import db
from .address import Address
from .parser import AddressParser
from app.models import Place, AddrFeat
import app.geocoder.ranking

class Geocoder:

    def __init__(self):
        self.address_parser = AddressParser()

    def geocode(self, address_string):
        try:
            address = self.address_parser.parse_address_string(Address(address_string))

            if address.address_line_1:
                print('geocoding address...')
                address = self.geocode_address(address)
                return address
            else:
                return None

        except Exception as error:
            print('Error occured while geocoding: %s' % error)
            print('Traceback: %s' % traceback.format_exc())

    def geocode_address(self, address):

        # 1. Find Zipcode
        potential_places = []
        if address.zip:
            potential_places.append(self.places_by_zip(address.zip))

        # 2a. extract city based on found zip or 'guess'
        address, guessed_place = self.extract_city(address, potential_places)
        # 2b. if no city is found, try and guess by potential string combinations
        if not guessed_place:
            guessed_places = self.guess_city(address.address_line_1)
            guessed_places += potential_places
            address, guessed_place = self.extract_city(address, guessed_places)

        # 3. If there is no place, do something....
        #     case; if zip return that.
        if not guessed_place:
            print('\t>Cannot find a for given address string: %s' % address)
            return None

        potential_places.append(guessed_place)
        print('-AddrFeat search for <%s>' % address.address_line_1)

        # 4. Post parse the address
        """Will need to apply post parse logic as street names (fullname) are stored in dataset with standardization.
        This is particularly difficult due to the may factors that are in an address string,
        such as pre/post dir + types and the latter being in the acutal street name [EAST ST]
        * Acutally, should try to tokenize the entire address and try combinations...
        """
        address = self.address_parser.post_parse_address(address)

        # 5. figure if we have no address....what now?
        if not address.address_line_1:
            return None

        # 6. search for potential addrfeats
        print('-Searching for address: <%s>' % address.address_line_1)
        potential_addrfeats = self.addrfeats_by_street(address.address_line_1)

        # 7. rank potential addrfeats
        ranked_addresses = app.geocoder.ranking.rank_address_candidates(address, potential_addrfeats)
        print('Ranked Results:')
        [print('\t>%s' % addrfeat) for addrfeat in ranked_addresses]

        #8. Interpolate coordinates

        return ranked_addresses[0]

    def extract_city(self, address, potential_places):
        """ Given a list of potential strings, return
        :param address:
        :param potential_places:
        :return: address object, extracted city string
        """
        sorted_list = sorted(potential_places, key=lambda k: k.city)
        for place in sorted_list:
            # TODO: Fuzzy match this!
            if place.city in address.address_line_1:
                address.address_line_1 = address.address_line_1.replace(place.city, '').strip()
                address.city = place.city
                return address, place
        return address, None

    def guess_city(self, address_string):
        """ Parse and address string into tokens. Run tokens against database to produce potentual cities
        :param address_string:
        :return: list of Place objects
        """
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

