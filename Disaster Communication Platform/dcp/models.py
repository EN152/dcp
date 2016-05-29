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

class Goods(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=100, null=True)
	description = models.TextField(max_length=500, null=True)
	location_x = models.FloatField(null=True)
	location_y = models.FloatField(null=True)
	created_date = models.DateTimeField(default=timezone.now)
	visibility = models.BooleanField(default=True)

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
	radius = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	
class Offer_Material(Material_Goods):
	bump_date = models.DateTimeField(default=timezone.now)
	report_cnt = models.PositiveSmallIntegerField(default=0)

class Search_Immaterial(Immaterial_Goods):
	radius = models.PositiveSmallIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	
class Offer_Immaterial(Immaterial_Goods):
	bump_date = models.DateTimeField(default=timezone.now)
	report_cnt = models.PositiveSmallIntegerField(default=0)

# Kommentare sind noch nicht ausgereift. Es ist nicht möglich ein ForeignKey von einer Abstract einzubinden (Goods)
# Wenn jemand eine bessere Idee hat, dann bitte ändern
class Comment(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	text = models.TextField(max_length=500, null=True)

	class Meta:
		abstract = True

class Search_Material_Comment(Comment):
	key = models.ForeignKey(Search_Material, on_delete=models.CASCADE, null=True)

class Offer_Material_Comment(Comment):
	key = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True)

class Search_Immaterial_Comment(Comment):
	key = models.ForeignKey(Search_Immaterial, on_delete=models.CASCADE, null=True)

class Offer_Immaterial_Comment(Comment):
	key = models.ForeignKey(Offer_Immaterial, on_delete=models.CASCADE, null=True)

# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
class Message(models.Model):
	From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
	To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
	Text = models.TextField(max_length=5000,null=False)
	SendTime = models.DateTimeField(default=timezone.now)
