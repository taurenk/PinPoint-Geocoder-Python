__author__ = 'Tauren'

from app.geocoder.geocoder import Geocoder
from flask.ext.restful import Resource, marshal, fields
from flask import got_request_exception
from app import app

geocoder = Geocoder()


class GeocoderApi(Resource):

    def get(self, address_string):
        results = geocoder.geocode(address_string)
        if len(results) == 0:
            return {'results': []}, 200
        else:
            return {'results': [res.to_dict() for res in results]}, 200

    def log_exception(sender, exception, **extra):
        """ Log an exception to our logging framework """
        app.logger.error('Error in Geocoding Service: %s', exception)

    got_request_exception.connect(log_exception, app)