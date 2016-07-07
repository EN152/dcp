from dcp.models import Catastrophe
from .imports import *

class Car(models.Model):
	description = models.CharField(max_length=200, null=False)
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

class Special(models.Model):
	description = models.CharField(max_length=200, null=False)
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)

class Event(models.Model):
	title = models.CharField(max_length=200, null=False)
	description = models.CharField(max_length=5000, null=False)
	created_date = models.DateTimeField(default=timezone.now)
	begin_date = models.DateTimeField(null=True)
	numberOfUsers = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(100)])
	numberOfCars = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	numberOfSpecials = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
	members = models.ManyToManyField(User)
	cars = models.ManyToManyField(Car, blank=True)
	specials = models.ManyToManyField(Special, blank=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	createdby = models.ForeignKey(User,related_name='createdEvents',on_delete=models.CASCADE)
	def __unicode__(self):
		return self.title