from django.views.generic import View
from django.views.static import loader
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import Ngo
from dcp.customForms.organizationForms import NgoForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from dcp.models.profile import Invite_Ngo

class NgoView(OrganizationView):
    """description of class"""
    def get(self, request, pk, usernameSearchString=None):
        templatePath= 'dcp/content/organization/ngo.html'
        user = request.user
        ngo = get_object_or_404(Ngo, id=pk)

        return super().get(request, ngo, templatePath, usernameSearchString=usernameSearchString)

    def post(self, request, pk):
        ngo = get_object_or_404(Ngo, id = pk)
        
        superReturn = super().post(request, ngo, Invite_Ngo)
        if superReturn == True:
            return self.get(request, pk, request.POST.get('usernameSearchString'))
        elif superReturn is not None:
            return superReturn

#        post_identifier = request.POST.get('post_identifier')
        user = request.user

        # Abfragen sind aus zukünftige Gründen (Erweiterung) so seltsam aufgebaut
        if not (user.is_active and user.is_authenticated() and (user.profile.ngo == ngo or user.is_superuser)):        
            return HttpResponseForbidden("Insufficent rights")
        if not (user.is_superuser or user.profile.is_organization_admin):
           return HttpResponseForbidden("Insufficent rights")
        if not (user.is_superuser):
           return HttpResponseForbidden("Insufficent rights")

        raise Http404

class NgoManagerView(View):
    """description of class"""

    def get(self, request, create_new_form=NgoForm):
        templatePath = 'dcp/content/adminstrator/ngoManager.html'
        template = loader.get_template(templatePath)
        user = request.user
        ngo_list = Ngo.objects.all()

        context = {
            'ngo_list': ngo_list,
            'create_new_form' : create_new_form
        }
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponseForbidden("Insufficent rights")

        return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            raise HttpResponseForbidden()
        form = NgoForm(request.POST)

        if form.is_valid():
            ngo = form.save()
        else:
            return self.get(request, create_new_form=form)

        url = '/ngo/' # Probleme mit Reverse von Urls TODO
        url += str(ngo.id)
        return HttpResponseRedirect(url)