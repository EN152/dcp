from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from dcp import dcpSettings
from dcp.customclasses.distance.distance import calculateDistanceClass
from dcp.models.catastrophe import Catastrophe
from django.utils import timezone
import datetime

class Organization(models.Model):
    name = models.CharField(max_length=200, null=False)
    name_short = models.CharField(max_length=3, null=False)
    created_date = models.DateTimeField(default=timezone.now, null=False, editable=False)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Area(models.Model):
    catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now, null=False, editable=False)
    # Sollte durch Polygone für die Grenzen ersetzt werden
    locationString = models.CharField(default='', max_length=200, null=True)
    location_x = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    location_y = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(dcpSettings.ORGANIZATIONS_AREA_MAX_RADIUS)])
    # ---------------------------------------------------------------------
    
    def isInArea(self, good):
        distance = calculateDistanceClass.calculate_distance(self.location_x, self.location_y, good.location_x, good.location_y)
        if (distance <= self.radius):
        	return True;
        return False

class Government(Organization):
    areas = models.ManyToManyField(Area, through='GovernmentArea')

    def getInvites(self):
        """
        Gibt eine Liste von den Invites zurück
        :author: Jasper
        :return: Eine Liste mit allen Invites
        """
        from dcp.customclasses.Helpers import getInvites
        
        return getInvites(government=self)

    def getMembers(self):
        """
        Gibt eine Liste von allen Mitgliedern zurück
        :author: Jasper
        :return: Eine Liste mit allen Mitgliedern
        """
        from .profile import Profile
        
        users = []
        for profile in Profile.objects.filter(government=self).select_related('user'):
        	users.append(profile.user)
        return  sorted(users, key=lambda u: u.profile.date_joined_organization, reverse=True)

class Ngo(Organization):
    areas = models.ManyToManyField(Area, through='NgoArea')

    def getInvites(self):
        """
        Gibt eine Liste von den Invites zurück
        :author: Jasper
        :return: Eine Liste mit allen Invites
        """
        from dcp.customclasses.Helpers import getInvites
        
        return getInvites(ngo=self)

    def getMembers(self):
        """
        Gibt eine Liste von allen Mitgliedern zurück
        :author: Jasper
        :return: Eine Liste mit allen Mitgliedern
        """
        from .profile import Profile
        
        users = []
        for profile in Profile.objects.filter(ngo=self).select_related('user'):
        	users.append(profile.user)
        return  sorted(users, key=lambda u: u.profile.date_joined_organization, reverse=True)

class AreaRealtion(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=False)
    canDeleteElements = models.BooleanField(null=False, default=False)
    created_date = models.DateTimeField(default=timezone.now, null=False, editable=False)
    class Meta:
        abstract = True

class GovernmentArea(AreaRealtion):
    government = models.ForeignKey(Government, on_delete=models.CASCADE, null=False)
    canCreateNgoArea = models.BooleanField(null=False, default=False)
    canAddNgo = models.BooleanField(null=False, default=False)
    canDeleteNgo = models.BooleanField(null=False, default=False)


class NgoArea(AreaRealtion):
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)