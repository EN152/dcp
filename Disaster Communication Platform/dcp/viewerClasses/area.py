from django.views.generic import View
from django.views.static import loader
from django.shortcuts import get_object_or_404
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import *
from dcp.customForms.organizationForms import AreaForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

class AreaView(View):
    def get(self, request, pk):
        user = request.user
        if not(user.is_authenticated() and user.is_active):
            HttpResponseRedirect('/')
        area = get_object_or_404(Area, id=pk)


class AreaAdminView(View):
    def get(self, request, create_new_form=AreaForm):
        user = request.user
        if not(user.is_authenticated() and user.is_active):
            HttpResponseRedirect('/')
        if not user.is_superuser:
            HttpResponseForbidden
        templatePath = 'dcp/content/organization/areaAdmin.html'
        template = loader.get_template(templatePath)
        area_list = Area.objects.all()

        context = {
            'area_list': area_list,
            'create_new_form' : create_new_form
        }
        return HttpResponse(template.render(context, request))