__author__ = 'Tauren'

import re
from binascii import unhexlify
from shapely import wkb, wkt

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


def convert_strings_to_float(from_num, to_num, target_num):
    # print('->Converting a string <%s/%s/%s> to float: %s' % (from_num, to_num, target_num, err))
    try:
        fn = float(re.sub('[^0-9]', '', from_num))
        tn = float(re.sub('[^0-9]', '', to_num))
        t = float(re.sub('[^0-9]', '', target_num))
        return fn, tn, t
    except ValueError:
        raise ValueError
    except Exception as err:
        print('Error Converting a string <%s/%s/%s> to float: %s' % (from_num, to_num, target_num, err))
        raise err

def check_number_range(fromnum, tonum, target):
    if (not fromnum) or (not tonum) or (not target):
        return False

    try:
        fn, tn, t = convert_strings_to_float(fromnum, tonum, target)
    except:
        return False

    if fn <= t <= tn:
        return True
    elif fn >= t >= tn:
        return True

    return False

