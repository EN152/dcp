# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from dcp.customclasses.categorys import Categorys
from dcp.customclasses.Helpers import get_object_or_none
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import dcp.customclasses

class Catastrophe(models.Model):
    Title = models.CharField(max_length=200)
    Location = models.CharField(max_length=100) # Soll das so? Nicht per Map Anzeigen?r
    PubDate = models.DateTimeField('date published', default=timezone.now)
    def __unicode__(self):
        return self.Title
    def isAbleToEdit(self,user : User):
        """
        Gibt zurück, ob ein Benutzer eine Katastrophe bearbeiten darf oder nicht
        :param user: Der Benutzer, der erfragt
        :return: True falls er darf, False falls nciht
        """
        return user.has_perm('dcp.EditCatastrophe')
    class Meta:
            permissions = (
                ("EditCatastrophe","Kann eine Katastrophe editieren/löschen"),
                ("CreateCatastrophe","Kann eine Katastrophe erstellen"),
            )
            unique_together = ('Title','Location')

class Profile(models.Model): # Wir erweitern das User Modell, wie es hier beschrieben wird:https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(User)
    currentCatastrophe = models.ForeignKey(Catastrophe,related_name='currentCatastrophe',null=True,blank=True) # TODO: Kaskade?
    def setCatastropheById(self,catId):
        """
        Setzt eine neue Katastrophe
        :author: Vincent
        :param catId: Die Id der neuen Katastrophe
        :return: False falls nicht erfolgreich, True falls erfolgreich
        """
        if catId is None: # Mache nichts
            return False
        try:
            catId = int(catId)
        except ValueError: #  catId kein Int
            return False
        newCatastrophe = get_object_or_none(Catastrophe,id=catId)
        if newCatastrophe is None:
            return False
        else:
            self.currentCatastrophe = newCatastrophe
            return True

    def get_profile_or_none(user: User):
            """
            Hole das Profil eines Benutzers
            Sonderfall Anonymous Benutzer: Default Profile
            :param user: Der Benutzer, dessen Profil man erfragen will
            :return: Das Profil des Benutzers, falls existent, sonst None
            """
            if user.is_anonymous():
                return Profile(currentCatastrophe=None)
            if user is None:
                return None
            else:
                return get_object_or_none(Profile, user=user)
    def get_profile_or_create(user: User):
        """
        Hole das Profil eines Benutzers oder erstelle es, falls er noch keins hat
        :param user: Der Benutzer, dessen Profil man erstellen will
        :return: None falls Fehler, sonst das Profil
        """
        if user.is_anonymous():
            return Profile(currentCatastrophe=None)
        if user is None:
            return None
        else:
            p = Profile.get_profile_or_none(user)
            if p is None:
                p = Profile(user=user,currentCatastrophe=None)
                p.save()
            return p

def create_profile(sender, **kwargs):
    """
    Zusammen mit post_save wird immer ein Profil erstellt,
    wenn ein Nutzer erstellt wird
    Siehe hier: https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
    :param sender:
    :param kwargs:
    :return:
    """
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

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
        return 'Search_immaterial'

class Offer_Immaterial(Immaterial_Goods):
    timeline_badge_color = models.CharField(max_length=100, null=False, default='red')
    timeline_glyphicon = models.CharField(max_length=100, null=False, default='glyphicon-transfer')

    def getGoodType(self):
        return 'Offer_Immaterial'

class Conversation(models.Model):
    Starter  = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Starter')
    Receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='Receiver')
    class Meta:
        unique_together = ('Starter','Receiver')
    def getConversationOrNone(userOne: User,userTwo: User):
        """
        Schaut nach, ob bereits eine Konversation zwischen zwei Nutzern
        in der Datenbank gespeichert ist. Falls ja wird die Konversation zurückgegeben,
        sonst None. Auf die Reihenfolge der Nutzer wird nicht geachtet, es
        ist also egal wer die Konversation tatsächlich gestartet hat
        :author Vincent
        :param userone: Chatteilnehmer1
        :param usertwo: Chatteilnehmer2
        :return: Konversation falls existent, sonst None
        """
        conversation = dcp.customclasses.Helpers.get_object_or_none(Conversation,
                                                                         Starter=userOne,
                                                                         Receiver=userTwo)

        if conversation is None:
            conversation = dcp.customclasses.Helpers.get_object_or_none(Conversation, Starter=userTwo,
                                                                         Receiver=userOne)


# Zur delete Cascade: Ich bin mir nicht sicher, ob das wirklich so sinnvoll ist.
# Die Frage ist, was bringen Nachrichten an einen nicht existierenden User -> Verhalten muss noch definiert werden.
class Message(models.Model):
    From  = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='From')
    To = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name='To')
    Text = models.TextField(max_length=5000,null=False)
    SendTime = models.DateTimeField(default=timezone.now)
    Conversation = models.ForeignKey(Conversation, null=False, related_name='Conversation')

class MissedPeople(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # catastrophe = models.ForeignKey(Catastrophe, on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #bumps = models.ForeignKey(Bump_Relation, on_delete=models.DO_NOTHING, null=True)
    #reports = models.ForeignKey(Report_Relation, on_delete=models.DO_NOTHING, null=True)

    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=5000, null=False)
    gender = models.CharField(max_length=1, null=False)
    age = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    name = models.CharField(max_length=100, null=False)
    size = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(250)])
    eyeColor = models.CharField(max_length=50, null=False)
    hairColor = models.CharField(max_length=50, null=False)
    characteristics = models.CharField(max_length=500, null=False)
    # picture = ???

    def __unicode__(self):
        return self.title