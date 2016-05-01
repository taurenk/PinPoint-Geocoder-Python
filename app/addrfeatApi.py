__author__ = 'Tauren'

from flask import abort
from flask.ext.restful import Resource, marshal, fields
from .models import AddrFeat
from app import db


class GeomToList(fields.Raw):
    def format(self, geom):
        return AddrFeat.geom_to_points(geom)

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
    'suftypabrv': fields.String,
    'geom': GeomToList
}

class AddrfeatApi(Resource):

    def __int__(self):
        pass

    def get(self, tlid):
        addrfeat_data = db.session.query(AddrFeat).filter(AddrFeat.tlid == tlid).all()
        if not addrfeat_data:
            abort(404)
        return {'results': marshal(addrfeat_data, addrfeat_fields)}, 200
