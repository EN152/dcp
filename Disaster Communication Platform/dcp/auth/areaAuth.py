from dcp.models.organizations import Government, Ngo, Area, NgoArea, GovernmentArea
from dcp.models.profile import Profile


def isAreaAdmin(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) is an AreaAdmin
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is an AreaAdmin
    """
    # Verified by Jasper, other verification pending
    for government in Government.objects.filter(areas=area, profile=profile, governmentarea__isFullAdmin=True, governmentmember__isAreaAdmin=True):
        return True
    for ngo in Ngo.objects.filter(areas=area, profile=profile, ngoarea__isFullAdmin=True, ngomember__isAreaAdmin=True):
        return True
    return False


def isCatastropheAdminByArea(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) is a catastrophe admin
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a full catastrophe admin
    """
    areaCatastrophe = area.catastrophe
    for placeholder in Ngo.objects.filter(areas=area, profile=profile, catastrophes=areaCatastrophe):
        return True
    for placeholder in Government.objects.filter(areas=area, profile=profile, catastrophes=areaCatastrophe):
        return True
    return False


def canCreateSubArea(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) can create Sub Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a allowed to create a Sub Area
    """
    # Verified by Jasper, other verification pending
    for government in Government.objects.filter(areas=area, profile=profile, governmentarea__canCreateSubArea=True, governmentmember__isAreaAdmin=True):
        return True
    return False


def canManageNgo(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) can Manage an Ngo in an Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a can Manage an Ngo in an Area
    """
    # Verified by Jasper, other verification pending
    for government in Government.objects.filter(areas=area, profile=profile, governmentarea__canManageNgo=True, governmentmember__isAreaAdmin=True):
        return True
    return False


def canViewArea(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) can view the Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user can view the Area
    """
    # Not verified
    for obj in Government.objects.filter(areas=area, profile=profile):
        return True
    for obj in  Ngo.objects.filter(areas=area, profile=profile):
        return True


def canDeleteElementsByArea(profile : Profile, area : Area) -> bool:
    """
    Internal Method to determine if a profile(user) can delete an elment in an Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user can delete an Element in the Area
    """
    for ngoArea in NgoArea.objects.filter(ngo__profile=profile, area=area).all():
        if ngoArea.isFullAdmin:
            return True
        if ngoArea.canDeleteElements:
            return True
    for governmentArea in GovernmentArea.objects.filter(government__profile=profile, area=area).all():
        if governmentArea.isFullAdmin:
            return True
        if governmentArea.canDeleteElements:
            return True