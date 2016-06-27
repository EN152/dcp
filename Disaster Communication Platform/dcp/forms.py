from django.forms import ModelForm
from dcp.models import *
from django import forms
import datetime
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.forms.models import *
from django.db.models.fields import CharField
from django.core.validators import MaxLengthValidator, MinLengthValidator

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

class CatastropheForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Bitte Katastrophentext eingeben'}))
    radius = forms.FloatField(min_value=0, max_value=10000, required=True)
    maxOutsideRadius = forms.FloatField(min_value=0, max_value=10000, initial=0, required=False, label='Maximaler Radius für außerhalb des jetzigen für Sub-Gebiete')
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    class Meta:
        model = Catastrophe
        fields = ["title", "radius", "location_x", "location_y"]

class CatastropheModelChoiceField(forms.ModelChoiceField):
    """
    Subclassing the ModelChoiceField Form um
    label_from_instance zu überschreiben:
    Siehe hier:https://docs.djangoproject.com/en/1.9/ref/forms/fields/#django.forms.ModelChoiceField
    """
    def label_from_instance(self,obj: Catastrophe):
        return obj.title + " in " + obj.locationString

class CatastropheChoice(forms.Form):
    catastrophe = CatastropheModelChoiceField(queryset=Catastrophe.objects.all().order_by('title'),empty_label='Katastrophe auswählen...',widget=forms.Select(attrs={'class':'form-control','onChange':'this.form.submit()'}),label='')

class MissedPeopleForm(forms.ModelForm):
    title = forms.CharField(required=True,label='Überschrift',widget=forms.TextInput(attrs={'placeholder': 'Lisa, 24 Jahre, Wedding'}))
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
        fields = ['title', 'description', 'gender', 'age', 'name',  'size', 'eyeColor', 'hairColor', 'characteristics', 'picture']

class EventPlanningForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label='Aktionsname',widget=forms.TextInput(attrs={'placeholder': 'Marchstraße aufräumen'}))
    description = forms.CharField(max_length=5000, required=False, label='Nähere Informationen',widget=forms.Textarea(attrs={'placeholder' : 'Insgesamt werden 42 Personen mit 7 Fahrzeugen gebraucht. Speziell gesucht wird Kaffee in Thermoskannen. Vielen Dank für Eure Mithilfe!'}))
    begin_date = forms.DateField(required=True, label='Beginn', widget=forms.TextInput(attrs={'class': 'datepicker', 'placeholder' : '2016-03-04 12:00' }))
    #begin_date = DateField(widget = AdminDateWidget)
    numberOfUsers = forms.IntegerField(required=True, label="maximale Personenzahl", widget=forms.NumberInput())
    numberOfCars = forms.IntegerField(required=True, label="maximale Fahrzeuganzahl", widget=forms.NumberInput())
    numberOfSpecials = forms.IntegerField(required=True, label="maximale Spezialdinge", widget=forms.NumberInput())

    class Meta:
        model = Event
        fields = ['title', 'description', 'begin_date', 'numberOfUsers', 'numberOfCars', 'numberOfSpecials']