import math

class calculateDistanceClass(object):
	@staticmethod
	def calculate_distance(lon1, lat1, lon2, lat2):
		R = 6371e3; # meter
		phi1 = lat1.radians()
		phi2 = lat2.radians()
		deltaphi = (lat2-lat1).radians()
		deltalambda = (lon2-lon1).radians()

		# Haversine Formula
		a = math.sin(deltaphi/2)**2 + math.cos(phi1) * mat.cos(phi2) * Math.sin(deltalambda/2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		distance = R * c

		return distance