from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.db.models.fields import CharField
from django.core.validators import MaxLengthValidator, MinLengthValidator

class UserForm(ModelForm):
    scndpwd = CharField(default = '',validators=[MinLengthValidator(0), MaxLengthValidator(50)])
    class Meta:
        model = User
        include = ('email', 'password', 'scndpwd')
        exclude = ('username',)