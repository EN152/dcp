from dcp.customForms.organizationForms import GovernmentAreaForm
from dcp.models.organizations import GovernmentArea, Government, Ngo
from dcp.models.profile import Profile

class ChangeGovernmentRightsInArea(object):
    @staticmethod
    def promoteGovernmentRight(request, area):
        """
        Ändert die Rechte einer NGO ins erhöhte
        :author: Jasper
        :return: True, wenn erfolgreich
        """
        user = request.user
        profile = Profile.objects.get(user=user) # .prefetch_related('ngomember_set__ngo__areas', 'governmentmember_set__government__areas') # TODO query optimization
        form = GovernmentAreaForm(request.POST)
        if not form.is_valid():
            return False
        government = form.cleaned_data['government']
        if user.is_superuser:
            return True
        if __canChangeRightsForGovernment(profile, area):
            changeGovernmentRight(form)

    
    @staticmethod
    def __canChangeRightsForGovernment(profile, area):
        """
        Internal Area
        """
        for government in Government.objects.filter(areas=area, governmentmember_set=profile).prefetch_releated('governmentarea_set'):
            for governmentArea in government.areas.all():
                if governmentArea.isFullAdmin:
                    for membership in governmentArea.government.governmentmember_set.get(profile=profile):
                        if membership.isAreaAdmin:
                            return True
        for ngo in Ngo.objects.filter(areas=area, ngomember_set=profile).prefetch_releated('ngo_set'):
            for ngoArea in ngo.areas.all():
                if ngoArea.isFullAdmin:
                    for membership in ngoArea.ngo.ngomember_set.get(profile=profile):
                        if membership.isAreaAdmin:
                            return True
        return False

    @staticmethod
    def __changeGovernmentRight(form):
        government = form.cleaned_data.get('government')
        if form.cleaned_data.get('isFullAdmin'):
            government.isFullAdmin = True
            government.save()
            return True