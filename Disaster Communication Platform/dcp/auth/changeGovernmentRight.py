from dcp.customForms.organizationForms import GovernmentAreaForm
from dcp.models.organizations import GovernmentArea
from dcp.models.profile import Profile

class ChangeGovernmentRight(object):
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
        if user.is_superuser:
            return True
        for obj in profile.ngos