from dcp.models.catastrophe import Catastrophe
from dcp.models.profile import Profile

def isCatastropheAdmin(profile : Profile, catastrophe : Catastrophe) -> bool:
    """
    Internal Method to determine if a profile(user) is a catastrophe admin
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param catastrophe: The catastrophe for the authorization validation
    :return: Boolean whether a user is full Catastrophe Admin
    """
    # Verified by Jasper, other verification pending

    if profile.user.is_superuser:
        return True

    for placeholder in Catastrophe.objects.filter(id=catastrophe.id, ngos__profile=profile, ngos__ngomember__isOrganizationAdmin=True):
        return True

    for placeholder in Catastrophe.objects.filter(id=catastrophe.id, governments__profile=profile,governments__governmentmember__isOrganizationAdmin=True):
        return True

    return False