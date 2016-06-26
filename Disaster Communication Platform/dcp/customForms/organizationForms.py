from django import forms
from dcp.models.organizations import *
from dcp.models.profile import Member

class GovernmentForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name', min_length=5, widget=forms.TextInput(attrs={'placeholder' : 'Deutschland'}))
    name_short = forms.CharField(required=True, label='Kurzname (3 Zeichen)', min_length=3, max_length=3, widget=forms.TextInput(attrs={'placeholder': 'DEU'}))

    class Meta:
        model = Government
        fields = ["name", "name_short"]

class NgoForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name', min_length=5, widget=forms.TextInput(attrs={'placeholder' : 'Greenpeace'}))
    name_short = forms.CharField(required=True, label='Kurzname (3 Zeichen)', min_length=3, max_length=3, widget=forms.TextInput(attrs={'placeholder': 'GRE'}))

    class Meta:
        model = Ngo
        fields = ["name", "name_short"]

class AreaForm(forms.ModelForm):
    ngos = forms.ModelMultipleChoiceField(queryset=Ngo.objects.all(), required=False, label='NGOs')
    governments = forms.ModelMultipleChoiceField(queryset=Government.objects.all(), required=False, label='Governments')
    catastrophe = forms.ModelChoiceField(required=True, queryset=Catastrophe.objects.all(), label='Katastrophe', empty_label=None)
    radius = forms.FloatField(min_value=0, max_value=10000, required=True)
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    
    class Meta:
        model = Area
        fields = ["ngos", "governments", "catastrophe", "radius", "location_x", "location_y"]

class MembershipForm(forms.Form):
    membership = forms.ModelChoiceField(queryset=None, required=True, label='Membership',widget=forms.HiddenInput(),empty_label=None)
    username = forms.CharField(label="Nutername", widget=forms.TextInput(attrs={'readonly': 'True'}))
    isOrganizationAdmin = forms.BooleanField(required=False ,label='Organization Admin')
    isAreaAdmin = forms.BooleanField(required=False, label='Gebiete Admin')
    created_date = forms.DateTimeField(required=True, label='Datum beigetreten', widget=forms.DateTimeInput(attrs={'readonly': 'True'}))

    class Meta:
        fields = ["membership", "userName", "isOrganizationAdmin", "isAreaAdmin", "created_date"]

    def __init__(self, *args, **kwargs):
        # self.fields['membership'].queryset = kwargs.get('membershipQuery')
        membershipQuery = kwargs.get('membershipQuery')
        membership = kwargs.get('membership')
        
        if membership is not None :
            username = membership.profile.user.username
            isOrganizationAdmin = membership.isOrganizationAdmin
            isAreaAdmin = membership.isAreaAdmin
            created_date = membership.created_date
            kwargs.update(initial={
                'username' : username,
                'membership' : membership,
                'isOrganizationAdmin' : isOrganizationAdmin,
                'isAreaAdmin' : isAreaAdmin,
                'created_date' : created_date
            })
        try :
            del kwargs['membershipQuery']
            del kwargs['membership']
        except :
            pass
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['membership'].queryset = membershipQuery