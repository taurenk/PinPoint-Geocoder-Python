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
    county = Column('county', String(256))
    latitude = Column(Numeric(4, 10))
    longitude = Column(Numeric(4, 10))

    def __str__(self):
        return '[id: %s, zip: %s, city: %s, state: %s]' % (self.id, self.zip, self.city, self.state)
