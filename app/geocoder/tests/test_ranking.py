__author__ = 'Tauren'

from flask.ext.testing import TestCase
from flask import Flask

from app import db
from app.models import AddrFeat
from app.geocoder.address import Address
from app.geocoder.ranking import rank_address_candidates

class TestAddressRanking(TestCase):

    def setUp(self):
        self.canidates = db.session.query(AddrFeat).filter(AddrFeat.fullname == 'CANAL VIEW DR').all()
        self.address = Address('1 Canal View Dr, Center Moriches, NY 11934')
        self.address.number = '1'
        self.address.address_line_1 = 'CANAL VIEW DR'
        self.address.city = 'CENTER MORICHES'
        self.address.zip = '11934'

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_rank_with_numeric_number(self):
        candidates = rank_address_candidates(self.address, self.canidates)
        # [print('\t:%s' % x) for x in candidates]
        assert candidates[0].gid == 786088
        assert candidates[0].rank == 3
        assert candidates[1].gid == 781480
        assert candidates[1].rank == 2

    def test_rank_with_alpha_numeric_number(self):
        self.address.number = '2A'
        candidates = rank_address_candidates(self.address, self.canidates)
        # [print('\t%s:%s' % (x.gid, x)) for x in candidates]
        assert candidates[0].gid == 786088
        assert candidates[0].rank == 3
        assert candidates[1].gid == 781480
        assert candidates[1].rank == 2
