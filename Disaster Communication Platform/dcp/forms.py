from django.contrib.auth.models import User
from django.forms.models import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')