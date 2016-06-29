from django import forms
from dcp.models.goods import *
from dcp.models.categorysGoods import *
from dcp.models.catastrophe import Catastrophe
from dcp.models.polls import *

import dcp.dcpSettings

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(required=True,label='Frage',widget=forms.TextInput(attrs={'placeholder': 'Soll Menschenfleischverzehr für die Dauer der Katastrophe erlaubt werden?'}))
    #catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    description = forms.CharField(required=False, label='Beschreibung (optional)', widget=forms.Textarea(attrs={'placeholder': 'Nähere Begebenheiten?', 'rows': '5'}))
    #image = forms.ImageField(required=False, label='Foto (optional)')
    #location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
   	#location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    #choice = forms.ModelMultipleChoiceField(queryset=Question.objects.all())

    class Meta:
        model = Question
        fields = ["question_text","description"]

class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(required=True, label='Auswahl', widget=forms.TextInput(attrs={'placeholder': 'Antwortoption'}))
    
    class Meta:
    	model = Choice
    	fields = ["choice_text"]