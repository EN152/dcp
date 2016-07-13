# imports
from dcp.importUrls import *
from django.http import Http404, HttpResponse
from dcp.models.profile import NgoInvite, GovernmentInvite, Invite
from dcp.models.organizations import Ngo, Organization
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from dcp.forms import EditProfileForm
from dcp.dcpSettings import MIN_PASSWORD_LENGTH

class Profil(LoginRequiredMixin, View):
    template = 'dcp/content/spezial/profiluebersicht.html'

    def get(self, request):
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template)

class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        templatePath = 'dcp/content/spezial/profil.html'
        template = loader.get_template(templatePath)
        user = request.user
        inviteNgoList = NgoInvite.objects.filter(profile=user.profile).select_related('organization')
        inviteGovernmentList = GovernmentInvite.objects.filter(profile=user.profile).select_related('organization')
        context = {
            'inviteNgoList': inviteNgoList,
            'inviteGovernmentList': inviteGovernmentList
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        post_identifier = request.POST.get('post_identifier')
        user = request.user
        if post_identifier == 'acceptNgoInvite':
            invite = invite = get_object_or_404(NgoInvite, id=request.POST.get('invite_id'), profile=user.profile)
            membership = invite.acceptInvite()
            return HttpResponseRedirect(reverse('dcp:NgoView', kwargs={'pk':membership.ngo.id}))

        elif post_identifier == 'acceptGovernmentInvite':
            invite = invite = get_object_or_404(GovernmentInvite, id=request.POST.get('invite_id'), profile=user.profile)
            membership = invite.acceptInvite()
            return HttpResponseRedirect(reverse('dcp:GovernmentView', kwargs={'pk':membership.government.id}))
        
        elif post_identifier == 'declineNgoInvite':
            invite = get_object_or_404(NgoInvite, id=request.POST.get('invite_id'), profile=user.profile)
            invite.delete()
            return HttpResponseRedirect(reverse('dcp:ProfileView'))

        elif post_identifier == 'declineGovernmentInvite':
            invite = get_object_or_404(GovernmentInvite, id=request.POST.get('invite_id'), profile=user.profile)
            invite.delete()
            return HttpResponseRedirect(reverse('dcp:ProfileView'))

        raise Http404
        

class EditProfile(LoginRequiredMixin, View):
    def get(self, request, editProfileForm=None):
        templatePath = 'dcp/content/spezial/profilBearbeiten.html'
        template = loader.get_template(templatePath)
        user = User.objects.get(id=request.user.id)
        if editProfileForm is None:
            editProfileForm = EditProfileForm(initial={
                'email' : user.email,
                'first_name': user.first_name,
                'last_name':user.last_name,
                'show_picture':user.profile.show_picture,
                'show_map': user.profile.show_map})

        context = {
            'editProfileForm' : editProfileForm
        }

        return HttpResponse(template.render(context, request))

    def post(self,request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.select_related('profile').get(id=request.user.id)
            profile = user.profile
            user.email = form.cleaned_data.get('email')
            profile.show_picture = form.cleaned_data.get('show_picture')  
            profile.show_map = form.cleaned_data.get('show_map')
            
            password = form.cleaned_data.get('password')
            if password is not None and password != '':
                user.set_password(password)
            user.save()
            profile.save()
            return HttpResponseRedirect(reverse('dcp:ProfileView'))

        else: 
            return self.get(request, editProfileForm=form)


