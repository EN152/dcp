from django import forms
from dcp.models.goods import *
from dcp.models.categorysGoods import *
from dcp.models.catastrophe import Catastrophe
from dcp.models.polls import *

import dcp.dcpSettings

class QuestionForm(forms.ModelForm):
	title = forms.CharField(required=True,label='Frage',widget=forms.TextInput(attrs={'placeholder': 'Soll Einbruch in Supermärkte für die Dauer der Katastrophe erlaubt werden?'}))
	text = forms.CharField(required=False, label='Beschreibung (optional)', widget=forms.Textarea(attrs={'placeholder': 'Nähere Begebenheiten?', 'rows': '5'}))
	catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
	choice_text = forms.CharField(required=True, label='Auswahl', widget=forms.TextInput(attrs={'placeholder': 'Antwortoptionen - mehrere mit Semikolon trennen!'}))


	class Meta:
		model = Question
		fields = ["title", "text", "catastrophe", "choice_text"]