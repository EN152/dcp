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

class AreaForm(forms.ModelForm):
    ngos = forms.ModelMultipleChoiceField(queryset=Ngo.objects.all(), required=False, label='NGOs')
    governments = forms.ModelMultipleChoiceField(queryset=Government.objects.all(), required=False, label='Governments')
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    radius = forms.FloatField(min_value=0, max_value=10000, required=True)
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    
    class Meta:
        model = Area
        fields = ["ngos", "governments", "catastrophe", "radius", "location_x", "location_y"]