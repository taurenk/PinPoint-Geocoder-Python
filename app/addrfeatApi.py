__author__ = 'Tauren'

from flask import abort
from flask.ext.restful import Resource, marshal, fields
from models import AddrFeat
from app import db


addrfeat_fields = {
    'gid': fields.Integer,
    'tlid': fields.Integer,
    'fullname': fields.String,
    'state': fields.String,

    'lfromhn': fields.String,
    'ltohn': fields.String,
    'rfromhn': fields.String,
    'rtohn': fields.String,
    'zipl': fields.String,
    'zipr': fields.String,

    'name': fields.String,
    'predirabrv': fields.String,
    'pretypabrv': fields.String,
    'suftypabrv': fields.String
}

class AddrfeatApi(Resource):

    def __int__(self):
        pass

    def get(self, street_name):
        """ Get city data based on given city
        :return:
        """
        addrfeat_data = db.session.query(AddrFeat).filter(AddrFeat.fullname == street_name).all()
        if not addrfeat_data:
            abort(404)
        return {'results': marshal(addrfeat_data, addrfeat_fields)}, 200
