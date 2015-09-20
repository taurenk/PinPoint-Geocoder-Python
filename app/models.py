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
    state = Column('name1', String(256))
    state_abbreviation = Column('code1', String(2))
    county = Column('name2', String(256))
    latitude = Column(Numeric(4, 10))
    longitude = Column(Numeric(4, 10))

    def __str__(self):
        return '[id: %s, zip: %s, city: %s, state: %s]' % (self.id, self.zip, self.city, self.state)


class AddrFeat(Base):

    __tablename__ = 'addrfeat'

    gid = Column(Integer, primary_key=True)
    tlid = Column(Integer)
    fullname = Column(String(100))
    state = Column(String(128))
    # Left/Right street data
    lfromhn = Column(String(12))
    ltohn = Column(String(12))
    rfromhn = Column(String(12))
    rtohn = Column(String(12))
    zipl = Column(String(5))
    zipr = Column(String(5))
    # Parsed Street Data
    name = Column(String(100))
    predirabrv = Column(String(15))
    pretypabrv = Column(String(50))
    suftypabrv = Column(String(50))

    geom = Column(Geometry('MULTILINESTRING'))

    @orm.reconstructor
    def init_on_load(self):
        self.rank = 0

    def __str__(self):
        return '[%s - %s - %s - %s - %s - <%s>]' % (self.rank, self.fullname, self.state, '%s/%s' % (self.zipl, self.zipr),
                                             'L: <%s-%s> /R: <%s-%s>' % (self.lfromhn, self.ltohn,
                                                                         self.rfromhn, self.rtohn),
                                                    self.geom)

class AddressResult:
    """ class for an address result"""

    def __init__(self, addrfeat=None, place=None):
        self.street_line_1 = None
        self.street_line_2 = None
        self.city = None
        self.state = None
        self.zipcode = None
        self.zip_plus_four = None
        self.lattitude = None
        self.longitude = None

    def convert_addrfeat(self, addrfeat):
        pass
    def convert_place(self, place):
        pass

    def to_json(self):
        dict = {'street_line_1': self.street_line_1,
                'city': self.city,
                'state': self.state,
                'zip': self.zipcode
                }
        return dict