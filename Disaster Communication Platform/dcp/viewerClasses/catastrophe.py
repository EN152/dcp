# imports
from dcp.importUrls import *


class DeleteCatastropheView(views.SuperuserRequiredMixin,DeleteView):
    model = Catastrophe
    template_name =  'dcp/content/adminstrator/deleteCatastrophe.html'
    def get_success_url(self):
        return reverse_lazy('dcp:CatastropheOverview')
class CreateOrEditCatastrophe(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/createOrEditCatastrophe.html'
    nextUrl = reverse_lazy('dcp:CatastropheOverview')
    def get(self,request):
        # Hat jemand die Id eine Katastrophe übergeben?
        inputId = request.GET.get('catid')
        if inputId  == None:
            form = CatastropheForm()
            return render(request, self.template, context={
                'form': form,
            })
        else:
            catastrophe = dcp.customclasses.Helpers.get_object_or_none(Catastrophe,id=inputId)
            if not catastrophe.isAbleToEdit(request.user):
                return HttpResponseForbidden(render(request,'dcp/content/spezial/403.html'))
            if catastrophe == None:
                return HttpResponseRedirect(self.nextUrl)
            else:
                form = CatastropheForm(instance=catastrophe)
                return render(request,self.template,context={'form':form})
    def post(self,request):
        form = CatastropheForm(request.POST)
        inputId = request.GET.get('catid')
        if form.is_valid():
            title = form.cleaned_data["Title"]
            location = form.cleaned_data["Location"]
            if inputId is None: # Keine Inputid -> Erstelle die Katastrophe direkt
                Catastrophe.objects.create(Title=title, Location=location)
                return HttpResponseRedirect(self.nextUrl)
            else: # Doch eine bereits bestehende Katastrophe?
                catastrophe = dcp.customclasses.Helpers.get_object_or_none(Catastrophe, id=inputId)
                if catastrophe is None:
                    return HttpResponseRedirect(self.nextUrl)
                else:
                    if not catastrophe.isAbleToEdit(request.user):
                        return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))
                    catastrophe.Title = title
                    catastrophe.location = location
                    catastrophe.PubDate = timezone.now()
                    catastrophe.save()
                    return HttpResponseRedirect(self.nextUrl)
        else: # Falls Form nicht valid
            return render(request, self.template, context={'form': form})

            