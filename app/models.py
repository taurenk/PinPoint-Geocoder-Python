__author__ = 'Tauren'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, Integer, String, orm
from geoalchemy2 import Geometry
from collections import defaultdict


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
        return '[id: %s, zip: %s, city: %s, state: %s, rank: %s]' % (
        self.id, self.zip, self.city, self.state, self.score)


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
        return '[id: %s, fullname: %s, zipl: %s, zipr: %s]' % (
            self.tlid, self.fullname, self.zipl, self.zipr)


class AddressResult:

    def __init__(self, formatted_address, level, score=0,
                 primary_number=None, street_fullname=None,
                 city_name=None, state_abbreviation=None, zipcode=None,
                 lat=None, lon=None, tlid=None, addrfeat_record=None):

        self.score = score
        self.level = level
        self.formatted_address = formatted_address

        self.primary_number = primary_number
        self.street_fullname = street_fullname
        self.city_name = city_name
        self.state_abbreviation = state_abbreviation
        self.zipcode = zipcode

        self.lat = lat
        self.lon = lon
        self.tlid = tlid
        self.addrfeat_record = addrfeat_record

    def __str__(self):
        string = "<street: %s, city: %s, state: %s, zip: %s>" % (self.street_fullname, self.city_name, self.state_abbreviation, self.zipcode)
        return string

    def to_dict(self):

        output = {
            "score": self.score,
            "level": self.level,
            "formatted_address": self.formatted_address,
            "geometry": {
                "location": {
                    "lat": str(self.lat),
                    "lon": str(self.lon)
                }
            },
            "components": {
                "city_name": self.city_name,
                "state": self.state_abbreviation,
                "zipcode": self.zipcode
            }
        }

        if self.primary_number:
            output["components"]["primary_number"] = self.primary_number
        if self.street_fullname:
            output["components"]["street_fullname"] = self.street_fullname
        if self.tlid:
            output["tiger_line_id"] = self.tlid

        return output
