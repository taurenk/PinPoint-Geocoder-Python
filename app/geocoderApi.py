__author__ = 'Tauren'

from flask.ext.restful import Resource
from app.geocoder.geocoder import Geocoder
from flask.ext.restful import Resource, marshal, fields

geocoder = Geocoder()

place_fields = {
    'id': fields.Integer,
    'city': fields.String,
    'zip': fields.String,
    'state': fields.String,
    'county': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'score': fields.Integer
}

class GeocoderApi(Resource):

    def __int__(self):
        pass

    def get(self, address_string):
        results = geocoder.geocode(address_string)
        return {'results':  marshal(results, place_fields)}, 200
