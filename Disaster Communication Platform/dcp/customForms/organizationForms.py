from django import forms
from dcp.models.organizations import *

class GovernmentForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name', min_length=5, widget=forms.TextInput(attrs={'placeholder' : 'Deutschland'}))
    name_short = forms.CharField(required=True, label='Kurzname (3 Zeichen)', min_length=3, max_length=3, widget=forms.TextInput(attrs={'placeholder': 'DEU'}))

    class Meta:
        model = Government
        fields = ["name", "name_short"]

class NgoForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name', min_length=5, widget=forms.TextInput(attrs={'placeholder' : 'Greenpeace'}))
    name_short = forms.CharField(required=True, label='Kurzname (3 Zeichen)', min_length=3, max_length=3, widget=forms.TextInput(attrs={'placeholder': 'GRE'}))

    class Meta:
        model = Ngo
        fields = ["name", "name_short"]