__author__ = 'Tauren'

from flask import abort
from flask.ext.restful import Resource, marshal, fields
from .models import Place
from app import db


place_fields = {
    'id': fields.Integer,
    'city': fields.String,
    'zip': fields.String,
    'state': fields.String,
    'county': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float
}

class PlaceApi(Resource):

    def __int__(self):
        pass

    def get(self, city):
        """ Get city data based on given city
        :return:
        """
        place_data = db.session.query(Place).filter(Place.city == city).all()
        if not place_data:
            abort(404)
        return {'results': marshal(place_data, place_fields)}, 200
