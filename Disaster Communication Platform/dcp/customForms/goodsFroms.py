from django import forms
from dcp.models.goods import *
from dcp.models.categorysGoods import *
from dcp.models.catastrophe import Catastrophe

import dcp.dcpSettings

class GoodForm(forms.ModelForm):
    title = forms.CharField(required=True,label='Überschrift',widget=forms.TextInput(attrs={'placeholder': 'Suche Kartoffeln'}))
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    description = forms.CharField(required=False, label='Beschreibung (optional)', widget=forms.Textarea(attrs={'placeholder': 'Ich benötige Kartoffeln für eine Suppe', 'rows': '5'}))
    image = forms.ImageField(required=False, label='Foto (optional)')
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    class Meta:
        model = Goods
        fields = ["title", "catastrophe", "description", "image", "location_x", "location_y"]

class SearchMaterialForm(GoodForm):
    category = forms.ModelChoiceField(queryset=CategorysGoods.objects.all(), required=True, label='Kategorie', empty_label=None)
    radius = forms.ChoiceField(choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS, required=False, label='Suchradius')
    class Meta:
        model = Search_Material
        fields = ["title", "category", "catastrophe", "description", "image", "radius", "location_x", "location_y"]

class SearchImmaterialForm(GoodForm):
    radius = forms.ChoiceField(choices=dcp.dcpSettings.RADIUS_CHOICES_GOODS, required=False, label='Suchradius')
    class Meta:
        model = Search_Immaterial
        fields = ["title", "catastrophe", "description", "image", "radius", "location_x", "location_y"]

class OfferMaterialForm(GoodForm):
    category = forms.ModelChoiceField(queryset=CategorysGoods.objects.all(), required=True, label='Kategorie', empty_label=None)
    class Meta:
        model = Offer_Material
        fields = ["title", "category", "catastrophe", "description", "image", "location_x", "location_y"]

class OfferImmaterialForm(GoodForm):
    class Meta:
        model = Offer_Immaterial
        fields = ["title", "catastrophe", "description", "image", "location_x", "location_y"]

