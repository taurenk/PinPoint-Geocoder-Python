__author__ = 'Tauren'

from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    import placeApi
    import addrfeatApi
    import geocoderApi

    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    app.db = db

    api = Api(app)
    api.add_resource(placeApi.PlaceApi, '/api/v1.0/place/<string:city>')
    api.add_resource(addrfeatApi.AddrfeatApi, '/api/v1.0/addrfeat/<string:street_name>')
    api.add_resource(geocoderApi.GeocderApi, '/api/v1.0/geocoder/<string:address_string>')

    return app