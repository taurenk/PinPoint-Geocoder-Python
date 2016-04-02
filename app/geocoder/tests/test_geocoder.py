__author__ = 'Tauren'

from flask.ext.testing import TestCase
from flask import Flask
from app import db
from app.geocoder.geocoder import Geocoder



class TestGeocodeAddress(TestCase):
    def setUp(self):
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
        data = self.geocoder.geocode(address)


class TestPlacesByCity(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def setUp(self):
        self.geocoder = Geocoder()

    def test_places_by_city_with_results(self):
        cities = self.geocoder.places_by_city('Manorville')
        assert len(cities) == 17

    def test_places_by_city_with_no_results(self):
        cities = self.geocoder.places_by_city('RETURNS NOTHING')
        assert len(cities) == 0
