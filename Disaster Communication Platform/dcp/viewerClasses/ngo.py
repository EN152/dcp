from django.views.generic import View
from django.views.static import loader
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import Ngo
from dcp.customForms.organizationForms import NgoForm, MembershipForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from dcp.models.profile import NgoInvite, NgoMember
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse

class NgoView(OrganizationView):
    """description of class"""
    def get(self, request, pk, usernameSearchString=None):
        templatePath= 'dcp/content/organization/organization.html'
        template = loader.get_template(templatePath)
        user = request.user
        ngo = get_object_or_404(Ngo, id=pk)
        try:
            membership = NgoMember.objects.get(profile=user.profile,ngo=ngo)
        except NgoMember.DoesNotExist:
            membership = None

        if membership is None and not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        usernameSearchList = self.getIniviteList(usernameSearchString,ngo)  
        memberlist = ngo.ngomember_set.all().prefetch_related('profile__user')
        membershipFormList = []
        for membership in memberlist:
            membershipForm = MembershipForm(membership=membership, membershipQuery=memberlist)
            membershipFormList.append(membershipForm)

        areas = ngo.areas.all()

        context = {
            'organization': ngo,
            'areas' : areas,
            'usernameSearchString': usernameSearchString,
            'usernameSearchList': usernameSearchList,
            'membership' : membership,
            'membershipFormList' : membershipFormList
        }

        return HttpResponse(template.render(context, request))

    def post(self, request, pk):
        ngo = get_object_or_404(Ngo, id = pk)

        post_identifier = request.POST.get('post_identifier')
        user = request.user

        try:
            membership = NgoMember.objects.get(profile=user.profile,ngo=ngo)
        except NgoMember.DoesNotExist:
            membership = None

        if membership is None and not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")
        
        superReturn = super().post(request, ngo, membership, NgoInvite, NgoMember)
        if superReturn == True:
            return self.get(request, pk, request.POST.get('usernameSearchString'))
        elif superReturn == False:
            pass
        else:
            return superReturn

        raise Http404

class NgoManagerView(LoginRequiredMixin,View):
    """description of class"""

    def get(self, request, create_new_form=NgoForm):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponseForbidden("Insufficent rights")

        templatePath = 'dcp/content/adminstrator/ngoManager.html'
        template = loader.get_template(templatePath)
        
        ngo_list = Ngo.objects.all().prefetch_related('profile_set')

        context = {
            'ngo_list': ngo_list,
            'create_new_form' : create_new_form
        }


        return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_superuser):
            raise HttpResponseForbidden("Insufficent rights")
        form = NgoForm(request.POST)

        if form.is_valid():
            ngo = form.save()
        else:
            return self.get(request, create_new_form=form)

        return HttpResponseRedirect(reverse('dcp:NgoView', kwargs={'pk':ngo.id}))