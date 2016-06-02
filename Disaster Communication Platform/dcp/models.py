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
		list = []
		for comment in Comment.objects.all():
			if comment.relation == self.comments:
				list.append(comment)
		return list

	def getBumps(self):
		list =[]
		for bump in Bump.objects.all():
			if bump.relation == self.bumps:
				list.append(bump)
		return list

	def getReports(self):
		list =[]
		for report in Report.objects.all():
			if report.relation == self.reports:
				list.append(report)
		return list

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
	image = models.ImageField(upload_to="upload/")

	def getGlyphiconString(self):
		if self.category == '1':
			return "glyphicon glyphicon-cutlery"
		elif self.category == '2':
			return "glyphicon glyphicon-home"
		elif self.category == '3':
			return "glyphicon glyphicon-wrench"
		elif self.category == '4':
			return "glyphicon glyphicon-plus"
		elif self.category == '5':
			return "glyphicon glyphicon-question-sign"

	def stringToCategoryType(category):
		if category == 'Groceries':
			return 1
		if category == 'Infrastructure':
			return 2
		if category == 'Tools':
			return 3
		if category == 'Drugs':
			return 4
		if category == 'Miscellaneous':
			return 5

	def getCategoryTypeAsString(self):
		if self.category == '1':
			return "Lebensmittel"
		elif self.category == '2':
			return "Infrastruktur"
		elif self.category == '3':
			return "Werkzeuge"
		elif self.category == '4':
			return "Medikamenten"
		elif self.category == '5':
			return "Sonstiges"

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
