from .imports import *
from .catastrophe import*

class Government(models.Model):
	name = models.CharField(max_length=200, null=False)
	name_short = models.CharField(max_length=3, null=False)
	created_date = models.DateTimeField(default=timezone.now)
	# Sollte durch Polygone für die Grenzen ersetzt werden
	location_x = models.FloatField(null=False)
	location_y = models.FloatField(null=False)
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])
	# ---------------------------------------------------------------------

	def getInvites(self):
		"""
		Gibt eine Liste von den Invites zurück
		:author: Jasper
		:return: Eine Liste mit allen Invites
		"""
		return getInvites(government=self)
		
	def getMembers(self):
		"""
		Gibt eine Liste von allen Mitgliedern zurück
		:author: Jasper
		:return: Eine Liste mit allen Mitgliedern
		"""
		users = []
		from .profile import Profile
		for profile in Profile.objects.filter(government=self):
			users.append(profile.user)
		return  sorted(users, key=lambda u: u.profile.date_joined_organization, reverse=True)

	def isInArea(self, good):
		distance = distance.calculateDistanceClass.calculate_distance(self.location_x, self.location_y, good.location_x, good.location_y)
		if (distance <= self.radius):
			return True;
		return False
		
