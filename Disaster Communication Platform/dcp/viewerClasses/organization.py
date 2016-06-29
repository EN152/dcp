# imports
from dcp.importUrls import *
from django.http import Http404
import dcp.dcpSettings
from django.contrib.auth.mixins import LoginRequiredMixin
from dcp.customForms.organizationForms import MembershipForm

class OrganizationView(LoginRequiredMixin, View):
    def getIniviteList(self, usernameSearchString, organization):
        usernameSearchListUser = []
        usernameSearchListInvited = []
        usernameSearchListMember = []
        if usernameSearchString:
            usernameSearchListUser = User.objects.filter(username__contains=usernameSearchString).select_related('profile')
            invites = organization.getInvites()
            members = organization.profile_set.all()
            for userSearch in usernameSearchListUser:
                setTrueInvite = False
                for tempInvite in invites:
                    if tempInvite.profile == userSearch.profile:
                        setTrueInvite = True
                        break
                if setTrueInvite:
                    usernameSearchListInvited.append(True)
                else:
                    usernameSearchListInvited.append(False)
                setTrueMember = False
                for tempMember in members:
                    if tempMember == userSearch.profile:
                        setTrueMember = True
                        break
                if setTrueMember:
                    usernameSearchListMember.append(True)
                else:
                    usernameSearchListMember.append(False)
        return zip(usernameSearchListUser, usernameSearchListInvited, usernameSearchListMember)
    
    def get(self, request, organization, membership, templatePath, usernameSearchString=None):
        return None
    
    def post(self, request, organization, membership, inviteModel, membershipModel):
        post_identifier = request.POST.get('post_identifier')
        user = request.user

        if membership != None:
            if not (membership.isOrganizationAdmin or user.is_superuser or membership.profile == user.profile):
                return HttpResponseForbidden("Insufficent rights")
        elif not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        if post_identifier =='endMembership':
            form = MembershipForm(request.POST, membershipQuery = membershipModel.objects.all())
            if form.is_valid():
                member = get_object_or_404(membershipModel, id=request.POST.get('membership'))
                member.delete()
            else: 
                membership.delete()
            return True
   
        # Only Admin POST from this point
        if membership != None:
            if not (membership.isOrganizationAdmin or user.is_superuser):
                return HttpResponseForbidden("Insufficent rights")
        elif not user.is_superuser:
            return HttpResponseForbidden("Insufficent rights")

        if post_identifier == 'inviteUserSearch':
            inviteUserSearchString = request.POST.get('usernameSearchString')
            return True

        if post_identifier == 'updateMembership':
            form = MembershipForm(request.POST, membershipQuery = membershipModel.objects.all())
            if form.is_valid():
                member = get_object_or_404(membershipModel, id=request.POST.get('membership'))
                isOrganizationAdmin = form.cleaned_data.get('isOrganizationAdmin')
                if isOrganizationAdmin:
                    member.isOrganizationAdmin = True
                else :
                    member.isOrganizationAdmin = False
                isAreaAdmin = form.cleaned_data.get('isAreaAdmin')
                if isAreaAdmin or isOrganizationAdmin:
                    member.isAreaAdmin = True
                else:
                    member.isAreaAdmin = False
                member.save()
                return True
            else:
                return False  

        if post_identifier == 'sendInvite':
            inviteUser = get_object_or_404(User, id=request.POST.get('user_invite_id'))
            invite = inviteModel.objects.get_or_create(profile=inviteUser.profile, organization=organization)
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