from dcp.importUrls import *
from django.core.urlresolvers import reverse

class NgoView(View):
    """description of class"""

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
        if user.is_authenticated() and user.is_active and user.is_superuser:
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponse(status=403)

        name = request.POST.get('name')
        name_short = request.POST.get('name_short')

        if not(name and name_short):
            return HttpResponse(status=404)
        if len(name_short) != 3:
            return self.get(request, invalidInput=True)

        ngo = Ngo.objects.create(name=name, name_short=name_short)
        url = '/ngo/' # Probleme mit Reverse von Urls
        url += str(ngo.id)
        return HttpResponseRedirect(url)