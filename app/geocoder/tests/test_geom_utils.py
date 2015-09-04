__author__ = 'Tauren'

from flask.ext.testing import TestCase
from flask import Flask
from app import create_app, db
from app.models import AddrFeat
from app.geocoder.utils.geo_utils import convert_geom_to_points
class TestGeocodeAddress(TestCase):

    def setUp(self):
        self.address = db.session.query(AddrFeat).filter(AddrFeat.fullname == 'CAPUTO DR').one()

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_convert_geom_points(self):
        geom = self.address.geom
        points_list = convert_geom_to_points(geom)
        # print(points_list)
        assert points_list[0][0] == '-72.7938789999999898'
        assert points_list[0][1] == '40.8591690000000014'
