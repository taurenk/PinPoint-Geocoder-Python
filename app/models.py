__author__ = 'Tauren'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Numeric, Integer, String, orm
from geoalchemy2 import Geometry
from binascii import unhexlify
from shapely import wkb, wkt

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

    @staticmethod
    def geom_to_points(geom):
        """
        Convert binary geom column to list of lat/lon point strings
        :return: list of lists containing lat/lon as string.
        """
        binary = unhexlify(geom.desc)
        point = wkb.loads(binary)
        data = wkt.dumps(point)
        data = data.replace('MULTILINESTRING ((', '')
        data = data.replace('))', '')
        point_list = data.split(',')
        points = [p.strip().split(' ') for p in point_list]
        # point_list = [float(point_list[0]), float(point_list[1])]

        points_to_float_list = [
            [float(point[0]), float(point[1])] for point in points]
        return points_to_float_list


class AddressResult:

    def __init__(self,
                 original_string,
                 primary_number=None,
                 addr_feat=None, place_record=None, score=None):

        self.original_string = original_string
        self.primary_number = primary_number
        self.addr_feat = addr_feat
        self.place = place_record
        self.score = score
        self.lat = None
        self.lon = None

    def __str__(self):
        string = "<street: %s, city: %s, state: %s, zip: %s>" % (self.street, self.city, self.state, self.zip)
        return string

    def to_dict(self):

        output = {
            "score": self.score,
            "original_address": self.original_string,
            "geometry": {},
            "components": {}
        }

        if self.primary_number:
            output["components"]["primary_number"] = self.primary_number

        if self.addr_feat:
            output["components"]["street_fullname"] = self.addr_feat.fullname
            output["tiger_line_id"] = str(self.addr_feat.tlid)

        if self.place:
            output["components"]["city"] = self.place.city
            output["components"]["state"] = self.place.state_code
            output["components"]["zipcode"] = self.place.zip

        if self.lat and self.lon:
            output["geometry"]["location"] = {"lat": str(self.lat), "lon": str(self.lon)}
        elif self.place:
            output["geometry"]["location"] = {"lat": str(self.place.latitude), "lon": str(self.place.longitude)}

        return output
