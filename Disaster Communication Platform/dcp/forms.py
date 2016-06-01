from django.forms import ModelForm
from dcp.models import *
from django import forms
import datetime
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.db.models.fields import CharField
from django.core.validators import MaxLengthValidator, MinLengthValidator

class Offer_Form(ModelForm):
	class Meta:
		model = Goods
		fields = ['title','description']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class sendMessage(forms.ModelForm):
    Text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder': 'Bitte Nachricht eingeben'}))
    class Meta:
        model = Message
        fields = ['Text']

class Comment_Form(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class Search_Material_Form(ModelForm):
    class Meta:
        model = Search_Material
        fields = ['tile', 'description', 'location_x', 'location_y', 'radius', 'catastrophe']