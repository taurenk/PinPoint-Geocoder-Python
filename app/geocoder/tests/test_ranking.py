__author__ = 'Tauren'

import unittest
from flask.ext.testing import TestCase
from flask import Flask

from app import db
from app.models import AddrFeat
from app.geocoder.address import Address
from app.geocoder.ranking import rank_address_candidates, check_number_range

class TestAddressRankingBasic(TestCase):

    def setUp(self):
        self.candidates = db.session.query(AddrFeat).filter(AddrFeat.fullname == 'CANAL VIEW DR').all()
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
        candidates = rank_address_candidates(self.address, self.candidates)
        # [print('\t:%s' % x) for x in candidates]
        assert candidates[0].gid == 786088
        assert candidates[0].rank == 3
        assert candidates[1].gid == 781480
        assert candidates[1].rank == 2

    def test_rank_with_alpha_numeric_number(self):
        self.address.number = '2A'
        candidates = rank_address_candidates(self.address, self.candidates)
        # [print('\t%s:%s' % (x.gid, x)) for x in candidates]
        assert candidates[0].gid == 786088
        assert candidates[0].rank == 3
        assert candidates[1].gid == 781480
        assert candidates[1].rank == 2

class TestAddressRankingAdvanced(TestCase):

    def setUp(self):
        self.candidates = db.session.query(AddrFeat).filter(AddrFeat.fullname == 'OLD WALT WHITMAN RD').all()
        self.address = Address('A1850 OLD WALT WHITMAN RD, MELVILLE, NY 11747')
        self.address.number = 'A1850'
        self.address.address_line_1 = 'OLD WALT WHITMAN RD'
        self.address.city = 'MELVILLE'
        self.address.zip = '11747'

    def create_app(self):
        """ Set up an app object with testing config """
        app = Flask(__name__)
        app.config.from_object('config')
        db.init_app(app)
        app.db = db
        return app

    def test_rank_address_with_odd_number(self):
        candidates = rank_address_candidates(self.address, self.candidates)
        # [print('\t%s:%s' % (x.gid, x)) for x in candidates]
        assert candidates[0].gid == 752161
        assert candidates[0].rank == 3

        assert candidates[1].gid == 778335
        assert candidates[1].rank == 2

        assert candidates[2].gid == 752156
        assert candidates[2].rank == 2
        assert candidates[3].gid == 752160
        assert candidates[3].rank == 2

class TestCheckNumberRange(unittest.TestCase):

    def test_check_number_range_same_side(self):
        test1 = check_number_range('1', '10', '5')
        print(test1)
        assert test1

        test2 = check_number_range('1', '10', '10')
        assert test2

        test3 = check_number_range('10', '1', '5')
        assert test3

        test4 = check_number_range('10', '1', '1')
        assert test4



