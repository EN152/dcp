from dcp.importUrls import *
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseForbidden

class NgoView(View):
    """description of class"""
    def get(self, request, pk, usernameSearchString=None):
        templatePath= 'dcp/content/organization/ngo.html'
        template = loader.get_template(templatePath)
        user = request.user
        ngo = get_object_or_404(Ngo, id=pk)

        if usernameSearchString == '':
            usernameSearchString == None

        if not(user.is_authenticated() and user.is_active and (user.profile.ngo == ngo or user.is_superuser)):
            return HttpResponseForbidden("Insufficent rights")

        usernameSearchListUser = []
        usernameSearchListInvited = []
        usernameSearchListMember = []
        if usernameSearchString:
            usernameSearchListUser = User.objects.filter(username__contains=usernameSearchString)
            for userSearch in usernameSearchListUser:
                setTrueInvite = False
                for tempInvite in ngo.getInvites():
                    if tempInvite.user == userSearch:
                        setTrueInvite = True
                        break
                if setTrueInvite:
                    usernameSearchListInvited.append(True)
                else:
                    usernameSearchListInvited.append(False)
                setTrueMember = False
                for tempMember in ngo.getMembers():
                    if tempMember == userSearch:
                        setTrueMember = True
                        break
                if setTrueMember:
                    usernameSearchListMember.append(True)
                else:
                    usernameSearchListMember.append(False)
        usernameSearchList = zip(usernameSearchListUser, usernameSearchListInvited, usernameSearchListMember)

        context = {
            'organization': ngo,
            'usernameSearchString': usernameSearchString,
            'usernameSearchList': usernameSearchList
        }
        return HttpResponse(template.render(context, request))

    def post(self, request, pk):
        user = request.user
        ngo = get_object_or_404(Ngo, id = pk)
        post_identifier = request.POST.get('post_identifier')

        if not (user.is_active and user.is_authenticated() and (user.profile.ngo == ngo or user.is_superuser)):
            return HttpResponseForbidden("Insufficent rights")

        if post_identifier =='contactMember':
            return None # TODO

        if post_identifier =='endMembership':
            member = get_object_or_404(User, id = request.POST.get('member_id'))
            if not (member == user or user.profile.is_organization_admin or user.is_superuser):
                return HttpResponseForbidden("Insufficent rights")
            member.profile.resetOrganization()
            if member == user:
                return HttpResponseRedirect('/')
            self.get(request, pk)

        if not (user.is_superuser or user.profile.is_organization_admin):
            return HttpResponseForbidden("Insufficent rights")
    
        if post_identifier == 'sendInvite':
            userInvite = get_object_or_404(User, id = request.POST.get('user_invite_id'))
            invite = Invite_Ngo.objects.get_or_create(user=userInvite, organization=ngo)
            return self.get(request, pk)
    
        if post_identifier == 'inviteUserSearch':
            inviteUserSearchString = request.POST.get('usernameSearchString')
            return self.get(request, pk, usernameSearchString=inviteUserSearchString)

        if post_identifier == 'discardInvite':
            invite = get_object_or_404(Invite_Ngo, id = request.POST.get('invite_id'))
            invite.delete()
            return self.get(request, pk)
        
        if post_identifier == 'promoteAdmin':
            member = get_object_or_404(User, id = request.POST.get('member_id'))
            member.profile.setOrganizationAdmin(True)
            return self.get(request, pk)

        if post_identifier == 'degrateAdmin':
            member = get_object_or_404(User, id = request.POST.get('member_id'))
            member.profile.setOrganizationAdmin(False)
            return self.get(request, pk)

        if not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        if post_identifier == 'deleteOrganization':
            ngo = get_object_or_404(Ngo, id = pk)
            ngo.delete()
            return HttpResponseRedirect('/')

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