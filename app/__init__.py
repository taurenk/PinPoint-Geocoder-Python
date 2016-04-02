__author__ = 'Tauren'

from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    from .placeApi import PlaceApi

    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    app.db = db
    api = Api(app)
    api.add_resource(PlaceApi, '/api/v1.0/place/<string:city>')

    return app