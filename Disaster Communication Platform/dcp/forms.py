from django import forms
from .models import Message

class sendMessage(forms.ModelForm):
    Text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-sm','placeholder': 'Bitte Nachricht eingeben'}))
    class Meta:
        model = Message
        fields = ['Text']