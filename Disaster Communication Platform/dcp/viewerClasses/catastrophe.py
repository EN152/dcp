from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render, loader
from django.http.response import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from geopy.geocoders import Nominatim
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SuperuserRequiredMixin
from dcp.customForms.catastropheForms import CatastropheChoiceFrom, CatastropheForm, CatastropheEditForm
from dcp.auth.catastropheAuth import isCatastropheAdmin
from dcp.customForms.organizationForms import AddNgoForm, AddGovernmentForm
from dcp.models.catastrophe import Catastrophe
from dcp.models.organizations import Ngo, Government
from dcp.models.profile import Profile

class CatastropheOverviewView(SuperuserRequiredMixin, View):
    template = 'dcp/content/adminstrator/catastropheOverview.html'
    def get(self,request, create_new_form : CatastropheForm = None):
        """
        :author Jasper
        Gibt eine Liste an Katastrohpen aus, mit der Möglichkeit Einträge zu löschen, Namen zu editieren und Katastrophen
        hinzuzufügen
        :param request:
        :return:
        """
        catastropheList = Catastrophe.objects.all().prefetch_related('ngos', 'governments')
        if create_new_form is None:
            create_new_form = CatastropheForm()

        context = {
            'catastrophes':catastropheList, 
            'create_new_form' : create_new_form,
            'catastropheList' : catastropheList
        }
        
        return render(request,self.template,context)

    def post(self, request):
        post_identifier = request.POST.get('post_identifier')
        if post_identifier == 'create':
            form = CatastropheForm(request.POST)
            if not form.is_valid():
                return self.get(request, create_new_form=form)
            catastrophe = form.save(commit=False)
            geolocator = Nominatim()
            location = geolocator.reverse(str(catastrophe.location_x) + " , " + str(catastrophe.location_y))
            if location.address is not None:
                catastrophe.locationString = location.address
            else :
                form.add_error('radius', 'Wähle eine gültige Position')
                return self.get(request, create_new_form=form)
            catastrophe.save()

            ngos = form.cleaned_data['ngos']
            governments = form.cleaned_data['governments']
            for ngo in ngos:
                catastrophe.ngos.add(ngo)
            for government in governments:
                catastrophe.governments.add(government)      

        if post_identifier == 'delete':
            catastrophe = get_object_or_404(Catastrophe, id = request.POST.get('catastrophe_id'))
            catastrophe.delete()

        return HttpResponseRedirect(reverse('dcp:CatastropheOverview'))
        

class CatastropheChangeView(LoginRequiredMixin, View):
    """
    :author: Jasper
    Changes the current catastrophe of the user
    """
    def post(self, request):
        form = CatastropheChoiceFrom(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, id=request.user.profile.id)
            profile.currentCatastrophe = cat = form.cleaned_data.get('catastrophe')
            profile.save()
        return HttpResponse(status=205) # TODO richtigen return wert

class CatastropheEditView(LoginRequiredMixin, View):
    """
    :author: Jasper
    On Overview of a catastrophe and a few edit-buttons
    """
    def get(self, request, pk, catastropheForm : CatastropheEditForm = None):
        templatePath = 'dcp/content/adminstrator/catastropheEdit.html'
        template = loader.get_template(templatePath)
        catastrophe = get_object_or_404(Catastrophe, id=pk)
        user = request.user

        if not catastrophe.isAbleToEdit(user):
            return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))

        if catastropheForm is None:
            catastropheForm = CatastropheEditForm(initial={'radius' : catastrophe.radius, 'maxOutsideRadius': catastrophe.maxOutsideRadius})

        ngos = Ngo.objects.exclude(catastrophes=catastrophe)
        ngoChoices = []
        for ngo in ngos:
            ngoChoices.append((ngo.id, ngo.name))
        catastropheForm['ngo'].field.choices = ngoChoices

        governments = Government.objects.exclude(catastrophes=catastrophe)
        governmentChoices = []
        for government in governments:
            governmentChoices.append((government.id, government.name))
        catastropheForm['government'].field.choices = governmentChoices

        context={
            'catastrophe' : catastrophe,
            'catastropheForm' : catastropheForm
        }
        
        return HttpResponse(template.render(context, request))

    def post(self, request, pk):
        catastrophe = get_object_or_404(Catastrophe, id=pk)
        user = request.user
        profile = user.profile

        if not catastrophe.isAbleToEdit(user):
            return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))

        form = CatastropheEditForm(request.POST)
        if not form.is_valid():
            return self.get(request, pk, catastropheForm=form)

        radius = form.cleaned_data['radius']
        maxOutsideRadius = form.cleaned_data['maxOutsideRadius']
        ngo = form.cleaned_data['ngo']
        government = form.cleaned_data['government']

        if catastrophe.radius > radius:
            form.add_error('radius', 'Der Radius kann nicht verringert werden')
            return self.get(request, pk, catastropheForm=form)

        if catastrophe.maxOutsideRadius > maxOutsideRadius:
            form.add_error('maxOutsideRadius', 'Der Maximal Außerhalb radius kann nicht verringert werden')
            return self.get(request, pk, catastropheForm=form)

        catastrophe.radius = radius
        catastrophe.maxOutsideRadius = maxOutsideRadius

        if ngo is not None:
            catastrophe.ngos.add(ngo)
        if government is not None:
            catastrophe.governments.add(government)

        catastrophe.save()
        return self.get(request, pk)