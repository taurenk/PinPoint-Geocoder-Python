__author__ = 'Tauren'

from math import radians, sin, cos, atan2, sqrt, degrees, asin, pi
import app.geocoder.ranking

def haversine(lat1, lon1, lat2, lon2):
    """ Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    delta_lat = (lat2-lat1)
    delta_lon = (lon2-lon1)
    a = sin(delta_lat/2) * sin(delta_lat/2) +\
            cos(lat1) * cos(lat2) * \
            sin(delta_lon/2) * sin(delta_lon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return 6371 * c

def bearing(lat1, lon1, lat2, lon2):
    """ Calculate bearing """
    lat1, lat2 = map(radians, [lat1,lat2])
    delta = radians((lon2-lon1))
    y = sin(delta) * cos(lat2)
    # y = sin(lon2-lon1) * cos(lat2);
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2-lon1)
    bearing = atan2(y, x)
    return (degrees(bearing) + 360) % 360

def find_point(lat, lon, bearing, distance):
    """ create a new point from origin point via
    a distance and bearing
    """
    d = distance/63741
    lat, lon, bearing = map(radians, [lat, lon, bearing])

    new_lat = asin( sin(lat) * cos(d) + cos(lat) * sin(d) * cos(bearing) )
    new_lon = lon + atan2(sin(bearing)*sin(d)*cos(lat),
                     cos(d)-sin(lat)*sin(new_lat))
    new_lon = (new_lon+3*pi) % (2*pi) - pi #normalize...
    return [degrees(new_lat), degrees(new_lon)]

def interpolate(points_list, target_number, lfrom, lto, rfrom, rto):

    from_number, to_number = None, None
    if app.geocoder.ranking.check_number_range(lfrom, lto, target_number):
        from_number, to_number = lfrom, lto
    elif app.geocoder.ranking.check_number_range(rfrom, rto, target_number):
         from_number, to_number = rfrom, rto
    else:
        return from_number, to_number

    if from_number < to_number:
        temp = from_number
        from_number = from_number
        to_number = temp

    dist_dict = {}
    # Confirmed; all records have atleast 2 points
    for idx in range(len(points_list)-1):
        dist_dict[idx] = haversine(points_list[idx][1], points_list[idx][0],
                                   points_list[idx+1][1], points_list[idx+1][0])

    print('Dist dict: %s' % dist_dict)
