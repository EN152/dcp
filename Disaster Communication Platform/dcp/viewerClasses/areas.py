from dcp.importUrls import *

class AreaOverview(View):
	def get(self, request):
		template = 'dcp/content/gebiete/overview.html'
		context = {}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)

class AreaSingle(View):
	def get(self, request):
		template = 'dcp/content/gebiete/gebiet.html'
		form = AreaForm()
		context = {'form' : form}
		return dcp.viewerClasses.authentication.getPageAuthenticated(request, template, context)



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