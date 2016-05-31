from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.db.models.fields import CharField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']