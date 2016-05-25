from __future__ import unicode_literals
from django.db import models
from datetime import timezone
from django.utils import timezone
from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Catastrophe(models.Model):
	cat_title = models.CharField(max_length=200)
	cat_location = models.CharField(max_length=100)
	cat_pub_date = models.DateTimeField('date published')
	
	def __unicode__(self):
		return self.cat_title 
	
class Search(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=True)
	CATEGORY_TYPE = (
				('1','Groceries',),
				('2,', 'Infrastructure'),
				('3', 'Tools'),
				('4', 'Drugs'),
				)
	category = models.CharField(max_length=1, choices=CATEGORY_TYPE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	radius = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	location_x = models.FloatField()
	location_y = models.FloatField()
	image = models.ImageField()
	created_date = models.DateTimeField(default=timezone.now)
	visibility = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title
	
class Offer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=True)
	CATEGORY_TYPE = (
				('1','Groceries',),
				('2,', 'Infrastructure'),
				('3', 'Tools'),
				('4', 'Drugs'),
				)
	category = models.CharField(max_length=1, choices=CATEGORY_TYPE)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=500)
	location_x = models.FloatField()
	location_y = models.FloatField()
	image = models.ImageField()
	created_date = models.DateTimeField(default=timezone.now)
	bump_date = models.DateTimeField(default=timezone.now)
	report_cnt = models.PositiveSmallIntegerField(default=0)
	visibility = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title
	