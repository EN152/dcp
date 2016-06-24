# imports
from dcp.importUrls import *
from django.http import Http404
import dcp.dcpSettings

class OrganizationView(View):
    def get(self, request, organization, templatePath, usernameSearchString=None):
        template = loader.get_template(templatePath)
        user = request.user

        if usernameSearchString == '':
            usernameSearchString == None

        if not(user.is_authenticated() and user.is_active and (user.profile.getOrganization() == organization or user.is_superuser)):
            return HttpResponseForbidden("Insufficent rights")

        usernameSearchListUser = []
        usernameSearchListInvited = []
        usernameSearchListMember = []
        if usernameSearchString:
            usernameSearchListUser = User.objects.filter(username__contains=usernameSearchString)
            for userSearch in usernameSearchListUser:
                setTrueInvite = False
                for tempInvite in organization.getInvites():
                    if tempInvite.user == userSearch:
                        setTrueInvite = True
                        break
                if setTrueInvite:
                    usernameSearchListInvited.append(True)
                else:
                    usernameSearchListInvited.append(False)
                setTrueMember = False
                for tempMember in organization.getMembers():
                    if tempMember == userSearch:
                        setTrueMember = True
                        break
                if setTrueMember:
                    usernameSearchListMember.append(True)
                else:
                    usernameSearchListMember.append(False)
        usernameSearchList = zip(usernameSearchListUser, usernameSearchListInvited, usernameSearchListMember)

        context = {
            'organization': organization,
            'usernameSearchString': usernameSearchString,
            'usernameSearchList': usernameSearchList
        }

        return HttpResponse(template.render(context, request))
    
    def post(self, request, organization, inviteModel):
        post_identifier = request.POST.get('post_identifier')
        user = request.user

        if user.is_active and user.is_authenticated() and (user.profile.getOrganization() == organization or user.is_superuser):
            if post_identifier =='contactMember':
                return None # TODO

            if post_identifier =='endMembership':
                member = get_object_or_404(User.objects.select_related('profile'), id = request.POST.get('member_id'))
                if not (member == user or user.profile.is_organization_admin or user.is_superuser):
                    return HttpResponseForbidden("Insufficent rights")
                member.profile.resetOrganization()
                if member == user:
                    return HttpResponseRedirect('/')
                return True

            if user.is_superuser or user.profile.is_organization_admin:    
                if post_identifier == 'inviteUserSearch':
                    inviteUserSearchString = request.POST.get('usernameSearchString')
                    return True

                if post_identifier == 'promoteAdmin':
                    member = get_object_or_404(User, id = request.POST.get('member_id'))
                    member.profile.setOrganizationAdmin(True)
                    return True

                if post_identifier == 'degrateAdmin':
                    member = get_object_or_404(User, id = request.POST.get('member_id'))
                    member.profile.setOrganizationAdmin(False)
                    return True

                if post_identifier == 'sendInvite':
                    userInvite = get_object_or_404(User, id = request.POST.get('user_invite_id'))
                    invite = inviteModel.objects.get_or_create(user=userInvite, organization=organization)
                    return True

                if post_identifier == 'discardInvite':
                    invite = get_object_or_404(inviteModel, id = request.POST.get('invite_id'))
                    invite.delete()
                    return True

                if user.is_superuser:
                    if post_identifier == 'deleteOrganization':
                        organization.delete()
                        return HttpResponseRedirect('/')
        return False 