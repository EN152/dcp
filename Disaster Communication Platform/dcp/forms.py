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

class Search_Material_Form(ModelForm):
    class Meta:
        model = Search_Material
        fields = ['title', 'description', 'location_x', 'location_y', 'radius', 'catastrophe', 'category']
class CatastropheForm(forms.ModelForm):
    Title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Bitte Katastrophentext eingeben'}))
    Location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Bitte Ort der Katastrophe eingeben'}))
    class Meta:
        model = Catastrophe
        fields = ["Title", "Location"]

class CatastropheModelChoiceField(forms.ModelChoiceField):
    """
    Subclassing the ModelChoiceField Form um
    label_from_instance zu überschreiben:
    Siehe hier:https://docs.djangoproject.com/en/1.9/ref/forms/fields/#django.forms.ModelChoiceField
    """
    def label_from_instance(self,obj: Catastrophe):
        return obj.Title + " in " + obj.Location

class CatastropheChoice(forms.Form):
    catastrophe = CatastropheModelChoiceField(queryset=Catastrophe.objects.all().order_by('Title'),empty_label='Bitte eine Katastrophe auswählen',widget=forms.Select(attrs={'class':'form-control','onChange':'this.form.submit()'}),label='Katastrophe')
