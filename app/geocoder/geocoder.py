__author__ = 'Tauren'

import traceback

from app import db
from .address import Address
from .parser import AddressParser
from app.models import Place, AddrFeat

class Geocoder:

    def __init__(self):
        pass

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

    def geocode_address(self, address):
        """ Try to further parse address in pieces.
        :return:
        """
        potential_places = []
        if address.zip:
            potential_places.append(self.places_by_zip(address.zip))
        # we will *never* have city at this point in the algorithm.

        if not potential_places:
            tokens = address.address_line_1.split(' ')[-3:]
            guess_tokens = []
            # make all combinations of tokens
            for idx, token in enumerate(tokens):
                guess_tokens.append(token)
                if idx > 0:
                    guess_tokens[0] += token
                if idx > 1:
                    guess_tokens[1] += token
            potential_places.append(self.places_by_city_list(guess_tokens))

        # Try and extract potential places from city from address string
        potential_places = [p.city for p in potential_places]
        self.extract_city(address.address_line_1, potential_places)

        # We can find a city without a city, state and zip....

    def extract_city(self, address, place_list):
        # Sort by longest string
        # match up against street_string
        # Return Place that fits OR None if none fit.

        # MODIFY ALGO TO MATCH LAST LENGTHS...
        place_list.sort(key=len)
        place_list.reverse()

        for place in place_list:
            if place in address.address_line_1:
                address.address_line_1 = address.address_line_1.replace(place, '')
                break

    def geocode_zipcode(self):
        pass

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

