__author__ = 'Tauren'

from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


def create_app():
    from .placeApi import PlaceApi
    from .geocoderApi import GeocoderApi
    from .addrfeatApi import AddrfeatApi

    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    app.db = db
    api = Api(app)
    api.add_resource(PlaceApi, '/api/v1.0/place/<string:city>')
    api.add_resource(GeocoderApi, '/api/v1.0/geocoder/<string:address_string>')
    api.add_resource(AddrfeatApi, '/api/v1.0/addrfeat/<string:tlid>')

    return app