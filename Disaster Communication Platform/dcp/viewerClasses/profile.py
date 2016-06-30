# imports
from dcp.importUrls import *
from django.http import Http404, HttpResponse
from dcp.models.profile import NgoInvite, GovernmentInvite, Invite
from dcp.models.organizations import Ngo, Organization
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

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
    template = 'dcp/content/spezial/profilBearbeiten.html'
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = UserForm(initial={'email' : user.email,'first_name': user.first_name,'last_name':user.last_name,'password':''})
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template, {'form': form})
    def post(self,request):
        if request.method == "POST":  
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                email = request.POST.get("email")
                password = request.POST.get("password")
                scndpwd = request.POST.get("scndpwd")
                if email != None: # Der Nutzer will die Email ändern
                    user.email = email
                    user.save()
                
                if password != None and password != scndpwd:
                    messages.add_message(request, messages.INFO,'Passwörter nicht identisch')
                    return render(request, self.template, {'form': form})
                else:
                    user.set_password(password)
                    user.save()
                    return HttpResponseRedirect(reverse('dcp:ProfileView'))
        return HttpResponseRedirect(reverse('dcp:ProfileView'))




