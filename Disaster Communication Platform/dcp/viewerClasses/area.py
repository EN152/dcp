from django.views.generic import View
from django.views.static import loader
from django.shortcuts import get_object_or_404
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import *
from dcp.customForms.organizationForms import AreaForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from geopy.geocoders import Nominatim

class AreaView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        # TODO Permissons
        templatePath = 'dcp/content/organization/area.html'
        template = loader.get_template(templatePath)
        area = get_object_or_404(Area.objects.select_related('catastrophe').prefectch_related('NgoArea_set', 'GovernmentArea_set', 'government_set', 'ngo_set') , id=pk)
        context = {
            'area' : area
        }
        return template.render(request, context)

class AreaAdminView(LoginRequiredMixin,View):
    def get(self, request, create_new_form=AreaForm):
        user = request.user
        catastrophe = user.profile.currentCatastrophe
        if not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")
        templatePath = 'dcp/content/organization/areaAdmin.html'
        template = loader.get_template(templatePath)
        if catastrophe is not None:
            area_list = Area.objects.filter(catastrophe=catastrophe).order_by('created_date').reverse().select_related('catastrophe_set').prefetch_related('ngo_set','government_set').reverse()
        else: 
            area_list = Area.objects.all().order_by('created_date').reverse().select_related('catastrophe').prefetch_related('ngo_set','government_set')


        context = {
            'area_list': area_list,
            'create_new_form' : create_new_form
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")
        
        form = AreaForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)

            geolocator = Nominatim()
            location = geolocator.reverse(str(area.location_x) + " , " + str(area.location_y))
            area.locationString = location.address

            area.save()

            ngos = Ngo.objects.filter(id__in=request.POST.getlist('ngos'))
            createNgoAreas = []
            for ngo in ngos:
                createNgoAreas.append(NgoArea(ngo=ngo, area=area))

            governments = Government.objects.filter(id__in=request.POST.getlist('governments'))
            createGovernmentsAreas = []
            for government in governments:
                createGovernmentsAreas.append(GovernmentArea(government=government, area=area))
            NgoArea.objects.bulk_create(createNgoAreas)
            GovernmentArea.objects.bulk_create(createGovernmentsAreas)
            return HttpResponseRedirect('')
        else:
            return self.get(request, create_new_form=form)