import math
from geopy.distance import vincenty

class calculateDistanceClass(object):
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        first = (lat1, lon1)
        second = (lat2, lon2)
        return vincenty(first, second).km

		#R = 6371e3; # meter
		#phi1 = lat1.radians()
		#phi2 = lat2.radians()
		#deltaphi = (lat2-lat1).radians()
		#deltalambda = (lon2-lon1).radians()
        #
		## Haversine Formula
		#a = math.sin(deltaphi/2)**2 + math.cos(phi1) * mat.cos(phi2) * Math.sin(deltalambda/2)**2
		#c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		#distance = R * c
        #
		#return distance

def getAreasForElement(location_x : float, location_y : float) -> bool:
    """
    Gets all areas based on the given cordinates
    :author: Jasper
    :param location_x: The location_x (lat) as float
    :param location_y: The object location_y (lng) as float
    :return: List of all areas found
    """
    from dcp.models.organizations import Area
    list = []
    for area in Area.objects.all():
        distance = calculateDistanceClass.calculate_distance(location_x, location_y, area.location_x, area.location_y)
        if distance <= area.radius:
            list.append(area)
    return list