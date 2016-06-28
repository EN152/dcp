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
    maxOutsideRadius = forms.FloatField(min_value=0, max_value=1000, initial=0, required=False, label='Maximaler Radius für außerhalb des jetzigen für Sub-Gebiete')
    location_x = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    location_y = forms.FloatField(required=True, initial=0, widget=forms.HiddenInput())
    
    class Meta:
        model = Area
        fields = ["ngos", "governments", "catastrophe", "radius", "maxOutsideRadius", "location_x", "location_y"]

class RemoveFromAreaForm(forms.Form):
    ngos = forms.ModelMultipleChoiceField(queryset=Ngo.objects.all(), required=False, label='NGOs')
    governments = forms.ModelMultipleChoiceField(queryset=Government.objects.all(), required=False, label='Governments')

class AddNgoForm(forms.Form):
    ngo = forms.ModelChoiceField(queryset=Ngo.objects.all(), empty_label= None,required=True, label='NGO')

    class Meta:
        fields = ["ngo"]

class AddGovernmentForm(forms.Form):
    government = forms.ModelChoiceField(queryset=Government.objects.all(), empty_label = None, required=True, label='Government')

    class Meta:
        fields = ["government"]

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


class NgoAreaForm(forms.Form):
    """
    First invisable field will be identified as NgoArea.id
    """
    ngoArea = forms.ModelChoiceField(queryset=NgoArea.objects.all(), required=True, label='ngoArea', widget=forms.HiddenInput(), empty_label=None)
    isFullAdmin = forms.BooleanField(required=False, label='Full Admin')
    canDeleteElements = forms.BooleanField(required=False, label='Kann Elemente löschen')

    class Meta:
        fields = ["ngoArea", "isFullAdmin", "canDeleteElements"]

    def __init__(self, *args, **kwargs):
        ngoArea = kwargs.get('ngoArea')
        
        if ngoArea is not None :
            isFullAdmin = ngoArea.isFullAdmin
            canDeleteElements = ngoArea.canDeleteElements
            kwargs.update(initial={
                'ngoArea' : ngoArea,
                'isFullAdmin' : isFullAdmin,
                'canDeleteElements' : canDeleteElements,
            })
        try :
            del kwargs['ngoArea']
        except :
            pass
        super(NgoAreaForm, self).__init__(*args, **kwargs)


class GovernmentAreaForm(forms.Form):
    """
    First invisable field will be identified as GovernmentArea.id
    """
    governmentArea = forms.ModelChoiceField(queryset=GovernmentArea.objects.all(), required=True, label='governmentArea', widget=forms.HiddenInput(), empty_label=None)
    isFullAdmin = forms.BooleanField(required=False, label='Full Admin')
    canDeleteElements = forms.BooleanField(required=False, label='Kann Elemente löschen')
    canManageNgo = forms.BooleanField(required=False, label='Kann eine NGO in das Gebiet aufnehmen')
    canCreateSubArea = forms.BooleanField(required=False, label='Kann ein Sub-Gebiet erstellen')

    class Meta:
        fields = ["governmentArea", "isFullAdmin", "canDeleteElements", "canManageNgo", "canCreateNgoArea"]

    def __init__(self, *args, **kwargs):
        governmentArea = kwargs.get('governmentArea')
        
        if governmentArea is not None :
            isFullAdmin = governmentArea.isFullAdmin
            canDeleteElements = governmentArea.canDeleteElements
            canManageNgo = governmentArea.canManageNgo
            canCreateSubArea = governmentArea.canCreateSubArea
            kwargs.update(initial={
                'governmentArea' : governmentArea,
                'isFullAdmin' : isFullAdmin,
                'canDeleteElements' : canDeleteElements,
                'canManageNgo' : canManageNgo,
                'canCreateSubArea' : canCreateSubArea
            })
        try :
            del kwargs['governmentArea']
        except :
            pass
        super(GovernmentAreaForm, self).__init__(*args, **kwargs)