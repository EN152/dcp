# imports
from dcp.importUrls import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from geopy.geocoders import Nominatim
from django.views.generic import View
from dcp.customForms.catastropheForms import CatastropheChoiceFrom, CatastropheForm


class DeleteCatastropheView(views.SuperuserRequiredMixin,DeleteView):
    model = Catastrophe
    template_name =  'dcp/content/adminstrator/deleteCatastrophe.html'
    def get_success_url(self):
        return reverse('dcp:CatastropheOverview')

class CreateCatastrophe(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/createOrEditCatastrophe.html'

    def get(self,request):
        # Hat jemand die Id eine Katastrophe übergeben?
        inputId = request.GET.get('catid')
        if inputId  == None:
            create_new_form = CatastropheForm()
            return render(request, self.template, context={
                'create_new_form': create_new_form,
            })
        else:
            catastrophe = get_object_or_404(Catastrophe,id=inputId)
            if not catastrophe.isAbleToEdit(request.user):
                return HttpResponseForbidden(render(request,'dcp/content/spezial/403.html'))
            if catastrophe == None:
                return HttpResponseRedirect(self.nextUrl)
            else:
                create_new_form = CatastropheForm(instance=catastrophe)
                return render(request,self.template,context={'create_new_form':create_new_form})
    def post(self,request):
        form = CatastropheForm(request.POST)
        inputId = request.GET.get('catid')
        if form.is_valid():
            if inputId is None: # Keine Inputid -> Erstelle die Katastrophe direkt
                catastrophe = form.save(commit=False)
                geolocator = Nominatim()
                location = geolocator.reverse(str(catastrophe.location_x) + " , " + str(catastrophe.location_y))
                catastrophe.locationString = location.address
                catastrophe.save()
                return HttpResponseRedirect(reverse('dcp:CatastropheOverview'))
            else: # Doch eine bereits bestehende Katastrophe?
                catastrophe = get_object_or_404(Catastrophe, id=inputId)
                if catastrophe is None:
                    return HttpResponseRedirect(self.nextUrl)
                else:
                    if not catastrophe.isAbleToEdit(request.user):
                        return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))
                    title = form.cleaned_data["title"]
                    locationString = form.cleaned_data["locationString"]
                    location_x = form.cleaned_data["location_x"]
                    location_y = form.cleaned_data["location_y"]
                    location = geolocator.reverse(str(location_x) + " , " + str(location_y))
                    catastrophe.title = title
                    catastrophe.locationString = location.address
                    catastrophe.created_date = timezone.now()
                    catastrophe.save()
                    return HttpResponse(reverse('dcp:CatastropheOverview'))
        else: # Falls Form nicht valid
            return render(request, self.template, context={'form': form})

class CatastropheOverview(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/catastropheOverview.html'
    def get(self,request):
        """
        :author Vincent
        Gibt eine Liste an Katastrohpen aus, mit der Möglichkeit Einträge zu löschen, Namen zu editieren und Katastrophen
        hinzuzufügen
        :param request:
        :return:
        """
        catastropheList = Catastrophe.objects.all().prefetch_related('ngos', 'governments')
        return render(request,self.template,context={'catastrophes':catastropheList})

    # TODO, delete button?
    def post(self, request):
        pass

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
        return HttpResponse(status=205)

# NOT IN USE; WILL BE IMPLEMENTED
class CatastropheEditView(LoginRequiredMixin, View):
    """
    :author: Jasper
    On Overview of a catastrophe and a few editbuttons
    """
    def get(self, request, pk):
        templatePath = 'dcp/content/catastrophe/catastropheEdit.html'
        template = loader.get_template(templatePath)
        catastrophe = get_object_or_404(Catastrophe, id=pk)
        if user.is_superuser or isAreaAdmin(user.profile, area) or canManageNgo(user.profile, area):
            addNgoForm = AddNgoForm()
            ngos = Ngo.objects.exclude(areas=area)
            ngoChoices = []
            for ngo in ngos:
                ngoChoices.append((ngo.id, ngo.name))
            addNgoForm['ngo'].field.choices = ngoChoices
        else :
            addNgoForm = None
        


    def post(self, request, pk):
        catastrophe = get_object_or_404(Catastrophe, id=inputId)
        if catastrophe is None:
            return HttpResponseRedirect(self.nextUrl)
        else:
            if not catastrophe.isAbleToEdit(request.user):
                return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))
            locationString = form.cleaned_data["locationString"]
            location_x = form.cleaned_data["location_x"]
            location_y = form.cleaned_data["location_y"]
            location = geolocator.reverse(str(location_x) + " , " + str(location_y))
            catastrophe.title = title
            catastrophe.locationString = location.address
            catastrophe.created_date = timezone.now()
            catastrophe.save()
            return HttpResponse(reverse('dcp:CatastropheOverview'))
