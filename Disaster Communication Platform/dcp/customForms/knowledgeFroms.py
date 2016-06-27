from django import forms
from dcp.models.goods import *
from dcp.models.categorysGoods import *
from dcp.models.catastrophe import Catastrophe

import dcp.dcpSettings

class KnowledgeForm(forms.ModelForm):
    title = forms.CharField(required=True,label='Überschrift',widget=forms.TextInput(attrs={'placeholder': 'Suche Kartoffeln'}))
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    description = forms.CharField(required=False, label='Beschreibung (optional)', widget=forms.Textarea(attrs={'placeholder': 'Ich benötige Kartoffeln für eine Suppe', 'rows': '5'}))
    image = forms.ImageField(required=False, label='Foto (optional)')
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    class Meta:
        model = Knowledge
        fields = ["title", "catastrophe", "description", "image", "location_x", "location_y"]


class PostNewsForm(KnowledgeForm):
    radius = forms.ChoiceField(choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS, required=False, label='Suchradius')
    class Meta:
        model = Post_News
        fields = ["title", "catastrophe", "description", "image", "radius", "location_x", "location_y"]

class PostDangersForm(KnowledgeForm):
    radius = forms.ChoiceField(choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS, required=False, label='Suchradius')
    class Meta:
        model = Post_Dangers
        fields = ["title", "catastrophe", "description", "image", "radius", "location_x", "location_y"]

class PostQuestionssForm(KnowledgeForm):
    radius = forms.ChoiceField(choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS, required=False, label='Suchradius')
    class Meta:
        model = Post_Questions
        fields = ["title", "description", "image"]
