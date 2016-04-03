__author__ = 'Tauren'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, Integer, String, orm
from geoalchemy2 import Geometry

Base = declarative_base()

class Place(Base):

    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    zip = Column(String(5))
    city = Column('place', String(256))
    city_metaphone = Column('place_metaphone', String(10))
    state = Column('state', String(256))
    state_metaphone = Column('state_metaphone', String(10))
    state_code = Column('state_code', String(3))
    county = Column('county', String(256))
    latitude = Column(Numeric(4, 10))
    longitude = Column(Numeric(4, 10))

    @orm.reconstructor
    def init_on_load(self):
        self.score = 0

    def __str__(self):
        return '[id: %s, zip: %s, city: %s, state: %s, rank: %s]' % (self.id, self.zip, self.city, self.state, self.score)


class AddrFeat(Base):

    __tablename__ = 'addrfeat'

    gid = Column(Integer, primary_key=True)
    tlid = Column(Integer)
    fullname = Column(String(100))
    fullname_metaphone = Column(String(10))
    # Left/Right street data
    lfromhn = Column(String(12))
    ltohn = Column(String(12))
    rfromhn = Column(String(12))
    rtohn = Column(String(12))
    zipl = Column(String(5))
    zipr = Column(String(5))
    geom = Column(Geometry('MULTILINESTRING'))

    @orm.reconstructor
    def init_on_load(self):
        self.score = 0

    def __str__(self):
        return '[id: %s, fullname: %s, meta: %s, zipl: %s, zipr: %s]' % (
            self.tlid, self.fullname, self.fullname_metaphone, self.zipl, self.zipr)
