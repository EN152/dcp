from dcp.importUrls import *
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden
from dcp.viewerClasses.organization import OrganizationView

class NgoView(dcp.viewerClasses.organization.OrganizationView):
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

    def get(self, request, invalidInput=False):
        templatePath = 'dcp/content/adminstrator/ngoManager.html'
        template = loader.get_template(templatePath)
        user = request.user
        ngo_list = Ngo.objects.all()

        context = {
            'ngo_list': ngo_list,
            'invalidInput': invalidInput
        }
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponseForbidden("Insufficent rights")

        return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponseForbidden("Insufficent rights")

        name = request.POST.get('name')
        name_short = request.POST.get('name_short')

        if not(name and name_short):
            raise Http404
        if len(name_short) != 3:
            return self.get(request, invalidInput=True)

        ngo = Ngo.objects.create(name=name, name_short=name_short)
        url = '/ngo/' # Probleme mit Reverse von Urls
        url += str(ngo.id)
        return HttpResponseRedirect(url)