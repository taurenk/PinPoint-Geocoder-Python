__author__ = 'Tauren'

from math import radians, sin, cos, atan2, sqrt, degrees, asin, pi

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

def interpolate(points_list, target_number):
    pass
    #


#
# def interpolate(self,candidate, address):
#         """ Basic Street to Coordinates Algorithm [Interpolation]
#         Convert multiline string, determine which side of street,
#         total houses, total distance of line,
#         for each point to point:
#             determine bearing, add until line is filled or steps
#             count is met. change bearing if new line point is hit.
#         """
#         points = []
#         points = self.convert_multilinestring(candidate[16])
#
#         # determine sid e better...please?!
#         if candidate[16] != None:
#             try:
#                 """
#                 print '\tSide=%s' % candidate[-1]
#                 print '\tLfrom/Lto=%s-%s' % (candidate[12],candidate[13])
#                 print '\tRfrom/Rto=%s-%s' % (candidate[14],candidate[15])
#                 """
#                 fromnum = tonum = 0
#
#                 if candidate[-1] == 'L':
#                     # set the if bigger/swap here
#                     fromnum = int(candidate[12])
#                     tonum = int(candidate[13])
#                 else:
#                     fromnum = int(candidate[14])
#                     tonum = int(candidate[15])
#
#
#                 fromnum = float(fromnum)
#                 tonum = float(tonum)
#
#                 # This rule is a thing...
#                 if fromnum == tonum: return [points[0][0], points[0][1]]
#
#                 # Convert multilinestring to lists of points[lists]
#                 total_dist = 0
#                 dist_dict = {}
#                 for idx in range(len(points)-1):
#                     dist_dict[idx] = self.haversine(points[idx][0], points[idx][1], points[idx+1][0], points[idx+1][1])
#                     total_dist += dist_dict[idx]
#
#                 total_steps = 0
#                 if fromnum <=  tonum:
#                     total_steps = (tonum-fromnum)
#                 else:
#                     total_steps = (fromnum-tonum)
#
#                 target_hn = float(address.number)
#                 ratio = total_dist / ((tonum-fromnum)/2) # tohn could be smaller than
#                 target_dist = ((target_hn - fromnum)/2) * ratio
#
#
#                 interpolated_point = None
#                 counted_dist = 0
#                 for k in dist_dict:
#                     counted_dist += dist_dict[k]
#                     if counted_dist >= target_dist:
#                         delta = counted_dist-target_dist
#                         segment_distance = dist_dict[k]-delta
#
#                         bearing = self.bearing2(points[k][0], points[k][1], points[k+1][0], points[k+1][1])
#
#                         interpolated_point = self.find_point2(points[k][0], points[k][1], bearing, segment_distance)
#                         break
#
#                 if interpolated_point is None: raise Exception('Failed to Geocode')
#                 else: return interpolated_point
#             except:
#                 print 'ERROR%s' % sys.exc_info()[0]
#                 return [points[0][0], points[0][1]]
#         else:
#             return None
