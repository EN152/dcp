from django.views.generic import View
from django.views.static import loader
from django.shortcuts import get_object_or_404
from dcp.viewerClasses.organization import OrganizationView
from dcp.models.organizations import Government
from dcp.customForms.organizationForms import GovernmentForm, MembershipForm
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from dcp.models.profile import GovernmentInvite, GovernmentMember
from django.core.urlresolvers import reverse

class GovernmentView(OrganizationView):
    def get(self, request, pk, usernameSearchString=None):
        # TODO Permission
        templatePath= 'dcp/content/organization/government.html'
        template = loader.get_template(templatePath)
        user = request.user
        government = get_object_or_404(Government, id=pk) 
        try:
            membership = GovernmentMember.objects.get(profile=user.profile,government=government)
        except GovernmentMember.DoesNotExist:
            membership = None

        if membership is None and not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        usernameSearchList = self.getIniviteList(usernameSearchString,government) 
        memberlist = government.governmentmember_set.all()

        membershipFormList =[]
        for membership in memberlist:
            membershipForm = MembershipForm(membership=membership, membershipQuery=memberlist)
            membershipFormList.append(membershipForm)

        context = {
            'organization': government,
            'membershipFormList' : membershipFormList,
            'usernameSearchString': usernameSearchString,
            'usernameSearchList': usernameSearchList,
            'membership' : membership
        }

        return HttpResponse(template.render(context, request))

    def post(self, request, pk):
        government = get_object_or_404(Government, id=pk)
        user = request.user

        try:
            membership = GovernmentMember.objects.get(profile=user.profile,government=government)
        except GovernmentMember.DoesNotExist:
            membership = None

        if membership is None and not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        superReturn = super().post(request, government, membership, GovernmentInvite, GovernmentMember)
        if superReturn == True:
            return self.get(request, pk, request.POST.get('usernameSearchString'))
        elif superReturn == False:
            pass
        else:
            return superReturn

        raise Http404

class GovernmentManagerView(View):
    """description of class"""

    def get(self, request, invalidInput=False, create_new_form=GovernmentForm):
        templatePath = 'dcp/content/adminstrator/governmentManager.html'
        template = loader.get_template(templatePath)
        user = request.user
        government_list = Government.objects.all().prefetch_related('profile_set')

        context = {
            'government_list': government_list,
            'create_new_form' : create_new_form
        }
        if user.is_authenticated() and user.is_active and user.is_superuser:
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user = request.user
        if not(user.is_authenticated() and user.is_active and user.is_superuser):
            return HttpResponseForbidden("Insufficent rights")

        form = GovernmentForm(request.POST)
        if form.is_valid():
            government = form.save()
        else:
            self.get(request, create_new_form=form)

        return HttpResponseRedirect(reverse('dcp:GovernmentView', kwargs={'pk':government.id}))