from .imports import *
from .catastrophe import *
from .profile import *

class Ngo(models.Model):
	name = models.CharField(max_length=200, null=False)
	name_short = models.CharField(max_length=3, null=False)
	created_date = models.DateTimeField(default=timezone.now)

	def getInvites(self):
		"""
		Gibt eine Liste von den Invites zurück
		:author: Jasper
		:return: Eine Liste mit allen Invites
		"""
		return getInvites(ngo=self)

	def getMembers(self):
		"""
		Gibt eine Liste von allen Mitgliedern zurück
		:author: Jasper
		:return: Eine Liste mit allen Mitgliedern
		"""
		users = []
		for profile in Profile.objects.filter(ngo=self):
			users.append(profile.user)
		return  sorted(users, key=lambda u: u.profile.date_joined_organization, reverse=True)

	def getAreas(self):
		"""
		Gibt eine Liste von den Gebieten zurück
		:author: Jasper
		:return: Eine Liste mit allen Gebieten
		"""
		return Ngo_Area.ojects.filter(ngo=self)

	def isInArea(self, good):
		for area in self.getAreas():
			distance = distance.calculateDistanceClass.calculate_distance(area.location_x, area.location_y, good.location_x, good.location_y)
			if (distance <= area.radius):
			    return True;
		return False

class Ngo_Area(models.Model):
	ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)
	created_date = models.DateTimeField(default=timezone.now)
	# Sollte durch Polygone für die Grenzen ersetzt werden
	location_x = models.FloatField(null=False)
	location_y = models.FloatField(null=False)
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	# ---------------------------------------------------------------------

	def isInArea(self, good):
		distance = distance.calculateDistanceClass.calculate_distance(self.location_x, self.location_y, good.location_x, good.location_y)
		if (distance <= self.radius):
			return True;
		return False
