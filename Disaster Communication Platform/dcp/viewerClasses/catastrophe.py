# imports
from dcp.importUrls import *
from django.core.urlresolvers import reverse_lazy, reverse
from geopy.geocoders import Nominatim
from django.views.generic import View


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
        catastropheList = Catastrophe.objects.all().prefetch_related('ngo_set', 'government_set')
        return render(request,self.template,context={'catastrophes':catastropheList})
            