__author__ = 'Tauren'

import unittest
from flask import Flask
from flask.ext.testing import TestCase

from app import db
from app.models import AddrFeat
from app.geocoder.geomath import haversine, bearing, find_point, interpolate
from app.geocoder.utils import geo_utils

class TestGeomath(unittest.TestCase):

    def test_haversine(self):
        pass

    def test_bearing(self):
        pass

    def test_find_point(self):
        pass


class TestInterpolation(TestCase):

    def setUp(self):
        self.address = db.session.query(AddrFeat).filter(AddrFeat.gid == 811529).one()

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_interpolation_easy(self):
        print('Addr: %s' % self.address)
        coords = geo_utils.convert_geom_to_points(self.address.geom)

        interpolated_points = interpolate(coords, '6', self.address.lfromhn, self.address.ltohn,
                                          self.address.rfromhn, self.address.rtohn)
