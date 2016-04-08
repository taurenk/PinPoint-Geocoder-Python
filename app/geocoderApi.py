__author__ = 'Tauren'

from app.geocoder.geocoder import Geocoder
from flask.ext.restful import Resource, marshal, fields
import json

geocoder = Geocoder()


class GeocoderApi(Resource):
    def get(self, address_string):
        results = geocoder.geocode(address_string)
        return {'results': [res.to_dict() for res in results]}, 200