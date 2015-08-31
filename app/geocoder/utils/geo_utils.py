__author__ = 'Tauren'

from shapely import wkb, wkt
from binascii import unhexlify

def convert_geom_to_points(geom):
    """ Convert binary geom column to list of lat/lon point strings
    :param geom: geom data
    :return: list of lists containing lat/lon as string.
    """
    binary = unhexlify(geom.desc)
    point = wkb.loads(binary)
    data = wkt.dumps(point)
    data = data.replace('MULTILINESTRING ((', '')
    data = data.replace('))', '')
    point_list = data.split(',')
    points = [p.split(' ') for p in point_list]
    return points