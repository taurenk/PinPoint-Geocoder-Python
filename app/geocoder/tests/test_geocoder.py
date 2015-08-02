__author__ = 'Tauren'


from flask.ext.testing import TestCase
from flask import Flask
from app import create_app, db

from app.geocoder.geocoder import Geocoder

class TestGeocoder(TestCase):

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_places_by_zip_pass(self):
        results = Geocoder().places_by_zip('11949')
        assert results[0].city == 'MANORVILLE'

if __name__ == '__main__':
    TestGeocoder()