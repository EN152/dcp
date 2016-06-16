# imports
from dcp.importUrls import *
from django.http import Http404

class MyProfile(View):
    template = 'dcp/content/spezial/profil.html'

           
    def get(self, request):
        user = request.user
        inviteList = user.profile.getInvites()
        context = {
            'inviteList': inviteList
        }
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template, context)

    def post(self, request):
        post_identifier = request.POST.get('post_identifier')
        user = request.user
        if post_identifier == 'accept_invite':
            if not(user.is_authenticated() and user.is_active):
                return HttpResponse(status=403)
            invite_type = request.POST.get('invite_type')
            invite_id = request.POST.get('invite_id')
            organization_id = request.POST.get('organization_id')
            print(invite_id)
            if invite_type is None or invite_id is None or organization_id is None:
                raise Http404
            if invite_type == 'Invite_Ngo':
                if not user.profile.acceptNgoInviteById(organization_id):
                    raise Http404
                url = '/ngo/' # TODO Probleme mit Reverse von Urls
                url += str(organization_id)
                return HttpResponseRedirect(url)

            elif invite_type == 'Invite_Goverment':
                if not user.profile.acceptGovermentInviteById(organization_id):
                    raise Http404
                url = '/goverment/' # TODO Probleme mit Reverse von Urls
                url += str(organization_id)
                return HttpResponseRedirect(url)
            else:
                raise Http404
        
        if post_identifier == 'decline_invite':
            if not(user.is_authenticated() and user.is_active):
                return HttpResponse(status=403)
            invite_type = request.POST.get('invite_type')
            invite_id = request.POST.get('invite_id')
            if invite_type is None or invite_id is None:
                raise Http404
            if invite_type == 'Invite_Ngo':
                Invite_Ngo.objects.get(id=invite_id).delete()
                return self.get(request)
            elif invite_type == 'Invite_Goverment':
                Invite_Goverment.objects.get(id=invite_id).delete()
                return self.get(request)
            else:
                raise Http404
        raise Http404

class EditProfile(View):
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
                    return HttpResponseRedirect("/profil/")
        return HttpResponseRedirect("/profil/")




