__author__ = 'Tauren'


from flask.ext.testing import TestCase
from flask import Flask
from app import create_app, db

from app.geocoder.geocoder import Geocoder
from app.geocoder.address import Address

class TestGeocoder(TestCase):

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
        assert results[0].city == 'MANORVILLE'

    def test_places_by_zip_fail(self):
        results = self.geocoder.places_by_city('100000')
        assert not results

    def test_places_by_city_list_pass(self):
        results = self.geocoder.places_by_city_list(['MANORVILLE', 'TUCKAHOE'])
        assert len(results) > 0

    def test_extract_city(self):
        address = Address('testing')
        address.address_line_1 = 'MCGUIRK STREET EAST HAMPTON'
        pass

if __name__ == '__main__':
    TestGeocoder()