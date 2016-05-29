from django import forms
from .models import Message

class sendMessage(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['Text']