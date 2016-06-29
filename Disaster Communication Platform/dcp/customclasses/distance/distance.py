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
    """ DOCS PENDING """
    pass