# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Catastrophe(models.Model):
	cat_title = models.CharField(max_length=200)
	cat_location = models.CharField(max_length=100)
	cat_pub_date = models.DateTimeField('date published')
	
	def __unicode__(self):
		return self.cat_title 

# Kommentare sind noch nicht ausgereift. Es ist nicht möglich ein ForeignKey von einer Abstract einzubinden (Goods)
# Wenn jemand eine bessere Idee hat, dann bitte ändern
class Comment_Relation(models.Model):
	date_created = models.DateTimeField(default=timezone.now) # Klassen ohne Variablen verursachen Probleme; "date_created" eine Art Platzhalter

class Comment(models.Model):
	comment_relation = models.ForeignKey(Comment_Relation, on_delete=models.CASCADE, null=False)
	date_created = models.DateTimeField(default=timezone.now)
	text = models.TextField(max_length=5000, null=True)

class Goods(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(max_length=500, null=True)
	location_x = models.FloatField(null=True)
	location_y = models.FloatField(null=True)
	created_date = models.DateTimeField(default=timezone.now)
	visibility = models.BooleanField(default=True)
	comments= models.ForeignKey(Comment_Relation, on_delete=models.DO_NOTHING, null=True)

	def __unicode__(self):
		return self.title

	class Meta:
		abstract = True

class Material_Goods(Goods):	
	CATEGORY_TYPE = (
				('1', 'Groceries'),
				('2', 'Infrastructure'),
				('3', 'Tools'),
				('4', 'Drugs'),
				('5', 'Miscellaneous')
				)
	category = models.CharField(max_length=1, choices=CATEGORY_TYPE)
	# Uploadpfad muss noch generiert werden... (Useranbindung + delete on cascade ? )
	image = models.ImageField(upload_to="/upload/...")

	class Meta:
		abstract = True

class Immaterial_Goods(Goods):
	class Meta:
		abstract = True

class Search_Material(Material_Goods):
	# lon = longitude, lat = latitude (coordinates)
	# signed decimal degrees without compass direction, where negative indicates west/south (e.g. 40.7486, -73.9864)
	radius = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	lon = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	lat = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	
class Offer_Material(Material_Goods):
	bump_date = models.DateTimeField(default=timezone.now)
	report_cnt = models.PositiveSmallIntegerField(default=0)
	lon = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	lat = models.DecimalField(default=0, max_digits=9, decimal_places=6)

class Search_Immaterial(Immaterial_Goods):
	radius = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	lon = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	lat = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	
class Offer_Immaterial(Immaterial_Goods):
	bump_date = models.DateTimeField(default=timezone.now)
	report_cnt = models.PositiveSmallIntegerField(default=0)
	lon = models.DecimalField(default=0, max_digits=9, decimal_places=6)
	lat = models.DecimalField(default=0, max_digits=9, decimal_places=6)

class Message(models.Model):
	# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
	# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
	From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
	To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
	Text = models.TextField(max_length=5000,null=False)
	SendTime = models.DateTimeField(default=timezone.now)
