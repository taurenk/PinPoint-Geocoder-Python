__author__ = 'Tauren'


from flask.ext.testing import TestCase
from flask import Flask
from app import create_app, db

from app.geocoder.geocoder import Geocoder
from app.geocoder.address import Address
from app.geocoder.tests import test_addresses

class TestGeocodeAddress(TestCase):

    def setUp(self):
        self.address_dict = test_addresses.test_address_dict
        self.geocoder = Geocoder()

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_geocoding_basic_addresses(self):
        address = '6 Caputo Drive Manorville NY 11949'
        parsed_address = self.address_dict['6 Caputo Drive Manorville NY 11949']
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

        address = '1 Canal View Dr, Center Moriches, NY 11934'
        parsed_address = self.address_dict['1 Canal View Dr, Center Moriches, NY 11934']
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

        # 492 Montauk Hwy, East Moriches, NY 11940
        address = '492 Montauk Hwy, East Moriches, NY 11940'
        parsed_address = self.address_dict['492 Montauk Hwy, East Moriches, NY 11940']
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

    def test_geocoding_partial_addresses(self):
        address = 'Manorville NY 11949'
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

        address = 'NY'
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

        address = 'NY 10707'
        data = self.geocoder.geocode(address)
        print('Geocode Address Results: %s\n' % data)

class TestExtractCity(TestCase):

    def setUp(self):
        self.address_dict = test_addresses.test_address_dict
        self.geocoder = Geocoder()

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_extract_city(self):
        """ extract_city() should find a city embeded into an address line string """
        address = Address('testing')
        address.address_line_1 = 'MCGUIRK STREET EAST HAMPTON'
        potential_places = self.geocoder.guess_city(address.address_line_1)
        address, city = self.geocoder.extract_city(address,potential_places)
        # City is returning EAST HAMPTON, CONNETICUT.
        assert address.address_line_1 == 'MCGUIRK STREET'
        assert city.city == 'EAST HAMPTON'

    def test_extract_city_FAIL(self):
        """ if extract_city() fails to find a city, expect the address to be unchanged and found city to be None """
        address = Address('testing')
        address.address_line_1 = 'MCGUIRK STREET EAST HAMPTON'
        potential_places = self.geocoder.guess_city('6 CAPUTO DRIVE MANORVILLE')
        address, city = self.geocoder.extract_city(address,potential_places)
        assert address.address_line_1 == 'MCGUIRK STREET EAST HAMPTON'
        assert not city

class TestPlaceQueries(TestCase):

    def setUp(self):
        self.geocoder = Geocoder()

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_places_by_zip_pass(self):
        results = self.geocoder.places_by_zip('11949')
        assert results.city == 'MANORVILLE'

    def test_places_by_zip_fail(self):
        results = self.geocoder.places_by_city('100000')
        assert not results

    def test_places_by_city_list_pass(self):
        results = self.geocoder.places_by_city_list(['MANORVILLE', 'TUCKAHOE'])
        assert len(results) > 0

    def test_addrfeats_by_street(self):
        results = self.geocoder.addrfeats_by_street('CAPUTO DR')
        #print(results[0].fullname)
        assert results[0].fullname == 'CAPUTO DR'