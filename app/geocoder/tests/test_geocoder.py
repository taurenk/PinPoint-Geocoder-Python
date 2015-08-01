__author__ = 'Tauren'

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from config import SQLALCHEMY_DATABASE_URI
from app.geocoder.geocoder import Geocoder

class TestGeocoder(unittest.TestCase):

    def setUp(self):
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        # self.connection = Session.configure(bind=engine)
        session = sessionmaker(bind=engine)
        self.geocoder =  Geocoder(session)

    def test_places_by_zip_pass(self):
        results = self.geocoder.places_by_zip('11949')
        print('Places By Zip: %s' % results)

if __name__ == '__main__':
    unittest.main()