__author__ = 'Tauren'

import unittest

from flask.ext.testing import TestCase
from flask import Flask
from app import db
from app.models import AddrFeat
from app.geocoder.utils import geo_utils


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
        points_list = geo_utils.convert_geom_to_points(geom)
        print(points_list)
        assert points_list[0][0] == '-72.7938789999999898'
        assert points_list[0][1] == '40.8591690000000014'


class TestStringsToFloat(unittest.TestCase):

    def test_convert_strings_to_float(self):
        from_num, to_num, target_num = geo_utils.convert_strings_to_float('1', '100', '50')
        assert from_num == 1.0 and to_num == 100.0 and target_num == 50.0

        from_num, to_num, target_num = geo_utils.convert_strings_to_float('1A', '100A', '50B')
        assert from_num == 1.0 and to_num == 100.0 and target_num == 50.0

        from_num, to_num, target_num = geo_utils.convert_strings_to_float('A1A', 'AA100A', 'BB-50B')
        assert from_num == 1.0 and to_num == 100.0 and target_num == 50.0

    def test_convert_strings_to_float_fail(self):
        try:
             from_num, to_num, target_num = geo_utils.convert_strings_to_float(None, 'AA100A', 'BB-50B')
        except Exception as error:
            assert ValueError


class TestCheckNumberRange(unittest.TestCase):

    def test_check_number_range(self):
        assert geo_utils.check_number_range('1', '10', '6')
        assert not geo_utils.check_number_range('1', '10', '11')

    def test_check_number_range_fail(self):
        try:
            geo_utils.check_number_range('1', '10.0',  None)
        except Exception as error:
            assert ValueError


