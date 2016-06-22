from dcp.importUrls import *
from dcp.viewerClasses.organization import OrganizationView

class GovernmentView(dcp.viewerClasses.organization.OrganizationView):
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

    def get(self, request, invalidInput=False):
        templatePath = 'dcp/content/adminstrator/governmentManager.html'
        template = loader.get_template(templatePath)
        user = request.user
        government_list = Government.objects.all()

        context = {
            'government_list': government_list,
            'invalidInput': invalidInput
        }
        if user.is_authenticated() and user.is_active and user.is_superuser:
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponse(status=403)

        name = request.POST.get('name')
        name_short = request.POST.get('name_short')
        position_x = request.POST.get('position_x')
        position_y = request.POST.get('position_y')
        radius = request.POST.get('radius')

        if not(name and name_short and position_x and position_y and radius):
            return self.get(request, invalidInput=True)
        try:
            position_x = float(position_x)
            position_y = float(position_y)
            radius = int(radius)
        except:
            return self.get(request, invalidInput=True)

        if len(name_short) != 3 or len(name) <= 3:
            return self.get(request, invalidInput=True)

        ngo = Government.objects.create(name=name, name_short=name_short, location_x= position_x, location_y = position_y, radius=radius)
        url = '/government/' # Probleme mit Reverse von Urls
        url += str(ngo.id)
        return HttpResponseRedirect(url)