from django.forms import ModelForm
from dcp.models import *
from django import forms
import datetime
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.models import *
from django.db.models.fields import CharField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from dcp.models.categorysGoods import  *
# from dcp.customForms.catastropheForms import * # Old stuff

import dcp.dcpSettings

from django.contrib.admin.widgets import AdminDateWidget

class Offer_Form(ModelForm):
	class Meta:
		model = Goods
		fields = ['title','description']

class UserForm(ModelForm):
	email = forms.CharField(widget=forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput, required=False)
	scndpwd = forms.CharField(max_length=200,widget=forms.PasswordInput, required=False,label='Passwort wiederholen')
	class Meta:
		model = User
		fields = ['email', 'password', 'scndpwd']

class sendMessage(forms.ModelForm):
    Text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder': 'Bitte Nachricht eingeben'}))
    class Meta:
        model = Message
        fields = ['Text']

class Comment_Form(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class MissedPeopleForm(forms.ModelForm):
    title = forms.CharField(required=True,label='Überschrift',widget=forms.TextInput(attrs={'placeholder': 'Lisa, 24 Jahre, Wedding'}))
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    description = forms.CharField(required=True,label='Situationsbeschreibung',widget=forms.TextInput(attrs={'placeholder': 'Verloren im Getummel am Hauptbahnhof am 01. April 2016. Sie hatte eine schwarze Tasche dabei.'}))
    gender = forms.CharField(required=True,label='Geschlecht: m/w',widget=forms.TextInput(attrs={'placeholder': 'w'}))
    age = forms.IntegerField(required=True,label='Alter (in Jahren)',widget=forms.TextInput(attrs={'placeholder': '24'}))
    name = forms.CharField(required=True,label='Name der vermissten Person',widget=forms.TextInput(attrs={'placeholder': 'Lisa Mustermann'}))
    size = forms.IntegerField(required=True,label='Körpergröße (in cm)',widget=forms.TextInput(attrs={'placeholder': '168'}))
    eyeColor = forms.CharField(required=True,label='Augenfarbe',widget=forms.TextInput(attrs={'placeholder': 'grün'}))
    hairColor = forms.CharField(required=True,label='Haarfarbe',widget=forms.TextInput(attrs={'placeholder': 'braun'}))
    characteristics = forms.CharField(required=True,label='Besondere Merkmale (mehrere durch Semikolon trennen!)',widget=forms.TextInput(attrs={'placeholder': 'trägt immer gelbe Schuhe; hat links nur einen Arm'}))
    picture = forms.ImageField(required=False, label='Aktuelles Foto (optional)')
    class Meta:
        model = MissedPeople
        fields = ['title', 'catastrophe','description', 'gender', 'age', 'name',  'size', 'eyeColor', 'hairColor', 'characteristics', 'picture']

class EventPlanningForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label='Aktionsname',widget=forms.TextInput(attrs={'placeholder': 'Marchstraße aufräumen'}))
    description = forms.CharField(max_length=5000, required=False, label='Nähere Informationen',widget=forms.Textarea(attrs={'placeholder' : 'Insgesamt werden 42 Personen mit 7 Fahrzeugen gebraucht. Speziell gesucht wird Kaffee in Thermoskannen. Vielen Dank für Eure Mithilfe!'}))
    begin_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M'],required=True, label='Beginn', widget=forms.TextInput(attrs={ 'placeholder' : '2016-03-04 12:00' }))
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    #begin_date = DateField(widget = AdminDateWidget)
    numberOfUsers = forms.IntegerField(required=True, label="maximale Personenzahl", widget=forms.NumberInput())
    numberOfCars = forms.IntegerField(required=True, label="maximale Fahrzeuganzahl", widget=forms.NumberInput())
    numberOfSpecials = forms.IntegerField(required=True, label="maximale Spezialdinge", widget=forms.NumberInput())

    class Meta:
        model = Event
        fields = ['title', 'description', 'begin_date', 'numberOfUsers', 'numberOfCars', 'numberOfSpecials','catastrophe']


class CategoryFilterForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=CategorysGoods.objects.all(), required=False,widget=forms.CheckboxSelectMultiple())
    class Meta:
        fields = ('categories')

class DeleteEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []
