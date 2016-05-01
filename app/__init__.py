__author__ = 'Tauren'

from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()
app = Flask(__name__)


def attach_logger(app):

    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    app.logger.addHandler(handler)


def create_app():
    from .placeApi import PlaceApi
    from .geocoderApi import GeocoderApi
    from .addrfeatApi import AddrfeatApi

    app.config.from_object('config')

    attach_logger(app)

    db.init_app(app)
    app.db = db
    api = Api(app)

    api.add_resource(PlaceApi, '/api/v1.0/place/<string:city>')
    api.add_resource(GeocoderApi, '/api/v1.0/geocoder/<string:address_string>')
    api.add_resource(AddrfeatApi, '/api/v1.0/addrfeat/<string:tlid>')

    return app