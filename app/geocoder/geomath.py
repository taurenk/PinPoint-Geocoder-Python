__author__ = 'Tauren'

from math import radians, sin, cos, atan2, sqrt, degrees, asin, pi


class GeoMath:

    def __init__(self):
        pass

    def haversine(self, lat1, lon1, lat2, lon2):
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

    def bearing(self, lat1, lon1, lat2, lon2):
        """ Calculate bearing """
        lat1, lat2 = map(radians, [lat1,lat2])
        delta = radians((lon2-lon1))
        y = sin(delta) * cos(lat2)
        # y = sin(lon2-lon1) * cos(lat2);
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2-lon1)
        bearing = atan2(y, x)
        return (degrees(bearing) + 360) % 360

    def find_point(self, lat, lon, bearing, distance):
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

    def interpolate(self, points_list, target_number,
                    left_from_house_number, left_to_house_number,
                    right_from_house_number, right_to_house_number):

        from_number, to_number = left_from_house_number, right_to_house_number

        """
        Let's simplify things for now and only take the highest/lowest numbers.
        Later, we can add in logic to determine house side
        """
        if left_from_house_number <= right_from_house_number:
            from_number = left_from_house_number
        if left_to_house_number >= right_to_house_number:
            to_number = left_to_house_number

        dist_dict = {}
        # TODO Confirm; all records in addrfeat table have atleast 2 points
        for idx in range(len(points_list)-1):
            dist_dict[idx] = self.haversine(points_list[idx][1], points_list[idx][0],
                                       points_list[idx+1][1], points_list[idx+1][0])

        print('Dist dict: %s' % dist_dict)