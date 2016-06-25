from django.views.generic import View
from django.views.static import loader
from django.shortcuts import get_object_or_404
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import Government
from dcp.customForms.organizationForms import GovernmentForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from dcp.models.profile import Invite_Government

class GovernmentView(OrganizationView):
    def get(self, request, pk, usernameSearchString=None):
        templatePath= 'dcp/content/organization/government.html'
        government = get_object_or_404(Government, id=pk)

        return super().get(request, government, templatePath, usernameSearchString=usernameSearchString)

    def post(self, request, pk):
        government = get_object_or_404(Government, id=pk)
        superReturn = super().post(request, government, Invite_Government)
        if superReturn == True:
            return self.get(request, pk, request.POST.get('usernameSearchString'))
        elif superReturn is not None:
            return superReturn

#       post_identifier = request.POST.get('post_identifier')
        user = request.user

        # Abfragen sind aus zukünftige Gründen (Erweiterung) so seltsam aufgebaut
        if not (user.is_active and user.is_authenticated() and (user.profile.government == government or user.is_superuser)):        
            return HttpResponseForbidden("Insufficent rights")
        if not (user.is_superuser or user.profile.is_organization_admin):
           return HttpResponseForbidden("Insufficent rights")
        if not (user.is_superuser):
           return HttpResponseForbidden("Insufficent rights")

        raise Http404

class GovernmentManagerView(View):
    """description of class"""

    def get(self, request, invalidInput=False, create_new_form=GovernmentForm):
        templatePath = 'dcp/content/adminstrator/governmentManager.html'
        template = loader.get_template(templatePath)
        user = request.user
        government_list = Government.objects.all()

        context = {
            'government_list': government_list,
            'invalidInput': invalidInput,
            'create_new_form' : create_new_form
        }
        if user.is_authenticated() and user.is_active and user.is_superuser:
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponse(status=403)

        form = GovernmentForm(request.POST)
        if form.is_valid():
            government = form.save()
        else:
            self.get(request, create_new_form=form)

        url = '/government/' # TODO Probleme mit Reverse von Urls 
        url += str(government.id)
        return HttpResponseRedirect(url)