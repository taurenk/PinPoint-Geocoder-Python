__author__ = 'Tauren'

from flask.ext.restful import Resource


class GeocderApi(Resource):

    def __int__(self):
        pass

    def get(self, address_string):
        return {'results': {'Feature Not yet Supported.'}}, 200
