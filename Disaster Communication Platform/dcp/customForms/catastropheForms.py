from dcp.models.catastrophe import Catastrophe
from django.forms import *

class CatastropheChoiceFrom(Form):
    catastrophe = ModelChoiceField(queryset=Catastrophe.objects.all().order_by('title'), required=False, empty_label='Keine Katastrophe', label='', widget=Select(attrs={'class':'form-control','onChange':'this.form.submit()'}))
    
class Meta:
        fields = ['catastrophe']

class CatastropheForm(ModelForm):
    from dcp.models.organizations import Ngo, Government

    title = CharField(widget=TextInput(attrs={'class':'form-control','placeholder':'Bitte Katastrophenname eingeben...'}))
    radius = FloatField(min_value=0, max_value=10000, required=True)
    maxOutsideRadius = FloatField(min_value=0, max_value=10000, initial=0, required=False, label='Maximaler Radius für außerhalb des jetzigen für Sub-Gebiete')
    ngos = ModelMultipleChoiceField(queryset=Ngo.objects.all(), required=False, label='NGOs mit uneingeschränktem Zugriff')
    governments = ModelMultipleChoiceField(queryset=Government.objects.all(), required=False, label='Governments mit uneingeschränktem Zugriff')
    location_x = FloatField(required=True, initial=0, widget=HiddenInput())
    location_y = FloatField(required=True, initial=0, widget=HiddenInput())

    class Meta:
        model = Catastrophe
        fields = ["title", "radius", "maxOutsideRadius", "ngos", "governments","location_x", "location_y"]

class CatastropheEditForm(Form):
    from dcp.models.organizations import Ngo, Government

    radius = FloatField(min_value=0, max_value=10000, required=True)
    maxOutsideRadius = FloatField(min_value=0, max_value=10000, initial=0, required=False, label='Maximaler Radius für außerhalb des jetzigen für Sub-Gebiete')
    ngo = ModelChoiceField(queryset=Ngo.objects.all(), required=False, empty_label='Keine neue NGO', label='NGO')
    government = ModelChoiceField(queryset=Government.objects.all(), required=False, empty_label='Keine neue Regierung')

    class Meta:
        fields = ["radius", "maxOutsideRadius", "ngo", "government"]