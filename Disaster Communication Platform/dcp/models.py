# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from dcp.customclasses.categorys import Categorys
# from abc import abstractmethod

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
	# Timelinevariablen müssen in jeder Subklasse neu gesetzt werden

	def __unicode__(self):
		return self.title

	def getComments(self):
		return Comment.objects.filter(relation = self.comments)

	def getBumps(self):
		return Bump.objects.filter(relation = self.bumps)

	def getReports(self):
		return Report.objects.filter(relation = self.reports)

	def getGood(type, id):
		if type == 'Search_Material':
			return Search_Material.objects.get(id=id)
		if type == 'Search_Immaterial':
			return Search_Immaterial.objects.get(id=id)
		if type == 'Offer_Material':
			return Offer_Material.objects.get(id=id)
		if type == 'Offer_Immaterial':
			return Offer_Immaterial.objects.get(id=id)
		return None
	def stringToGoodClass(type):
		if type == 'Search_Material':
			return Search_Material
		if type == 'Search_Immaterial':
			return Search_Immaterial
		if type == 'Offer_Material':
			return Offer_Material
		if type == 'Offer_Immaterial':
			return Offer_Immaterial
		return None

	def getAllGoods():
	    listOfGoods = []
	    for oneGood in Search_Material.objects.all():
	        listOfGoods.append(oneGood)
	    for oneGood in Offer_Immaterial.objects.all():
	        listOfGoods.append(oneGood)
	    for oneGood in Offer_Material.objects.all():
	        listOfGoods.append(oneGood)
	    for oneGood in Search_Immaterial.objects.all():
	        listOfGoods.append(oneGood)
	    return listOfGoods

	def isSearchedForByString(self, searchString):
		if searchString in self.description or searchString in self.title:
			return True
		else:
			return False



	class Meta:
		abstract = True

class Material_Goods(Goods):
	category = models.CharField(max_length=1, choices=Categorys.CATEGORY_TYPES)
	# Uploadpfad muss noch generiert werden... (Useranbindung + delete on cascade ? )
	image = models.ImageField(upload_to="upload/")

	def getCategoryGlyphiconAsString(self):
		return Categorys.getCategoryGlyphiconAsString(self.category)

	def getCategoryNameAsString(self):
		return Categorys.getCategoryNameAsString(self.category)

	class Meta:
		abstract = True

class Immaterial_Goods(Goods):
	class Meta:
		abstract = True

class Search_Material(Material_Goods):
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	timeline_badge_color = models.CharField(max_length=100, null=False, default='blue')
	timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-search')

	def getGoodType(self):
		return 'Search_Material'
	
class Offer_Material(Material_Goods):
	timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
	timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')

	def getGoodType(self):
		return 'Offer_Material'

class Search_Immaterial(Immaterial_Goods):
	radius = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
	timeline_badge_color = models.CharField(max_length=100, null=False, default='blue')
	timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-search')

	def getGoodType(self):
		return 'Search_Immaterial'
	
class Offer_Immaterial(Immaterial_Goods):
	timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
	timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')
	
	def getGoodType(self):
		return 'Offer_Immaterial'

class Conversation(models.Model):
	Starter  = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Starter')
	Receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Receiver')

# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
class Message(models.Model):
	From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
	To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
	Text = models.TextField(max_length=5000,null=False)
	SendTime = models.DateTimeField(default=timezone.now)
	Conversation = models.ForeignKey(Conversation, null=False, related_name='Conversation')