from django.forms import *
from django.contrib.auth.models import User
from dcp.dcpSettings import MIN_PASSWORD_LENGTH

class RegisterForm(ModelForm):
    username = CharField(required=True, label='', max_length=100, min_length=3, widget=TextInput(attrs={'placeholder':'Benutzername'}))
    email = EmailField(required=True, label='', widget=EmailInput(attrs={'placeholder' : 'E-Mail'}))
    password = CharField(required=True, min_length=MIN_PASSWORD_LENGTH, label='', widget=PasswordInput(attrs={'placeholder': 'Passwort'}))
    passwordRepeat = CharField(required=True, min_length=MIN_PASSWORD_LENGTH, label='', widget=PasswordInput(attrs={'placeholder': 'Passwort'}))

    class Meta:
        model = User
        fields =  ["username", "email", "password", "passwordRepeat"]

    def clean(self):
        super(RegisterForm, self).clean()
        if self.cleaned_data.get('password') != self.cleaned_data.get('passwordRepeat'):
            self.add_error('password', 'Passwörter stimmen nicht überein')
            self.add_error('passwordRepeat','')
        for user in User.objects.filter(username=self.cleaned_data.get('username')):
            self.add_error('username', 'Nutzername bereits vergeben')
            break
        return self.cleaned_data

class LoginForm(Form):
    username = CharField(required=True, label='', max_length=100, min_length=3, widget=TextInput(attrs={'placeholder':'Benutzername'}))
    password = CharField(required=True, label='', widget=PasswordInput(attrs={'placeholder': 'Passwort'}))

    class Meta:
        fields =  ["username", "password"]