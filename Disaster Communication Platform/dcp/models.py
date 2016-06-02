# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from dcp.customclasses.categorys import *

class Catastrophe(models.Model):
	cat_title = models.CharField(max_length=200)
	cat_location = models.CharField(max_length=100)
	cat_pub_date = models.DateTimeField('date published')
	
	def __unicode__(self):
		return self.cat_title 

class Comment_Relation(models.Model):
	class Meta:
		abstract = False

class Comment(models.Model):
	relation = models.ForeignKey(Comment_Relation, on_delete=models.CASCADE, null=False)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
	created_date = models.DateTimeField(default=timezone.now)
	text = models.TextField(max_length=500, null=False)

	def __unicode__(self):
		return self.text

class Bump_Relation(models.Model):
	class Meta:
		abstract = False

class Report_Relation(models.Model):
	class Meta:
		abstract = False

class Bump(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
	relation = models.ForeignKey(Bump_Relation, on_delete=models.CASCADE, null=False)
	date_created = models.DateTimeField(default=timezone.now)

class Report(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
	relation = models.ForeignKey(Report_Relation, on_delete=models.CASCADE, null=False)
	date_created = models.DateTimeField(default=timezone.now)

class Goods(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
	title = models.CharField(max_length=100, null=False)
	description = models.TextField(max_length=500, null=True)
	location_x = models.FloatField(null=True)
	location_y = models.FloatField(null=True)
	created_date = models.DateTimeField(default=timezone.now)
	comments = models.ForeignKey(Comment_Relation, on_delete=models.DO_NOTHING, null=True)
	bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True)
	reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True)
	visibility = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

	def getComments(self):
		return Comment.objects.filter(relation = self.comments)

	def getBumps(self):
		return Bump.objects.filter(relation = self.bumps)

	def getReports(self):
		return Report.objects.filter(relation = self.reports)

	class Meta:
		abstract = True

class Material_Goods(Goods):
	category = models.CharField(max_length=1, choices=Categorys.CATEGORY_TYPES)
	# Uploadpfad muss noch generiert werden... (Useranbindung + delete on cascade ? )
	image = models.ImageField(upload_to="upload/")

	def getGlyphiconCategoryTypeString(self):
		Categorys.getCategoryGlyphiconTypeString(self.category)

	def getCategoryTypeAsString(self):
		Categorys.getCategoryNameTypeAsString(self.category)

	class Meta:
		abstract = True

class Immaterial_Goods(Goods):
	class Meta:
		abstract = True

class Search_Material(Material_Goods):
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	
class Offer_Material(Material_Goods):
	class Meta:
		abstract = False

class Search_Immaterial(Immaterial_Goods):
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	
class Offer_Immaterial(Immaterial_Goods):
	class Meta:
		abstract = False

# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
class Message(models.Model):
	From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
	To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
	Text = models.TextField(max_length=5000,null=False)
	SendTime = models.DateTimeField(default=timezone.now)
