from django.forms import ModelForm
from dcp.models import *
from django import forms
import datetime

class Offer_Form(ModelForm):
	class Meta:
		model = Goods
		fields = ['title','description']
	#title = forms.CharField(max_length=100, null=True)
	#description = forms.TextField(max_length=500, null=True)