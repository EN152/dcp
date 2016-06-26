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
    # Fully managing Catastrophe
    catastrophe = models.ManyToManyField(Catastrophe)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Area(models.Model):
    catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now, null=False, editable=False)
    parrent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    maxOutsideRadius = models.FloatField(null=False, validators=[MinValueValidator(-180), MaxValueValidator(180)])
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
    
    # TODO Query Optimization
    def getGoods(self):
        from dcp.models.goods import Goods
        list = []
        for good in Goods.getAllGoods():
            if self.isInArea(good):
                list.append(good)
        return list

    def getOffers(self):
        from dcp.models.goods import Goods
        list = []
        for good in Goods.getAllOffers():
            if self.isInArea(good):
                list.append(good)
        return list

    def getSearches(self):
        from dcp.models.goods import Goods
        list = []
        for good in Goods.getAllSearches():
            if self.isInArea(good):
                list.append(good)
        return list
    # Haben keine Location
    def getMissingPersons():
        pass
    # TODO, wo ist das Model?
    def getEvents():
        pass

class Government(Organization):
    areas = models.ManyToManyField(Area, through='GovernmentArea')

    def getInvites(self):
        """
        Gibt eine Liste von den Invites zurück
        :author: Jasper
        :return: Eine Liste mit allen Invites
        """
        from dcp.models.profile import GovernmentInvite
        return GovernmentInvite.objects.filter(organization=self).select_related('profile')

class Ngo(Organization):
    areas = models.ManyToManyField(Area, through='NgoArea')

    def getInvites(self):
        """
        Gibt eine Liste von den Invites zurück
        :author: Jasper
        :return: Eine Liste mit allen Invites
        """
        from dcp.models.profile import NgoInvite
        return NgoInvite.objects.filter(organization=self).select_related('profile')

class AreaRelation(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=False)
    isFullAdmin = models.BooleanField(null=False, default=False)
    canDeleteElements = models.BooleanField(null=False, default=False)
    created_date = models.DateTimeField(default=timezone.now, null=False, editable=False)
    class Meta:
        abstract = True

class GovernmentArea(AreaRelation):
    government = models.ForeignKey(Government, on_delete=models.CASCADE, null=False)
    canCreateNgoArea = models.BooleanField(null=False, default=False)
    canManageNgo = models.BooleanField(null=False, default=False)


class NgoArea(AreaRelation):
    ngo = models.ForeignKey(Ngo, on_delete=models.CASCADE, null=False)