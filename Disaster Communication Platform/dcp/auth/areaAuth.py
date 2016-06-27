from dcp.models.organizations import Government, Ngo, Area
from dcp.models.profile import Profile

@staticmethod
def isAreaAdmin(profile : Profile, area : Area) -> type.BooleanType:
    """
    Internal Method to determine if a profile(user) is an AreaAdmin
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is an AreaAdmin
    """
    for government in Government.objects.filter(areas=area, profile_set=profile).prefetch_releated('governmentarea_areas'):
        for governmentArea in government.areas.all():
            if governmentArea.isFullAdmin:
                for membership in governmentArea.government.profiles_set.filter(profile=profile):
                    if membership.isAreaAdmin:
                        return True
    for ngo in Ngo.objects.filter(areas=area, ngomember_set=profile).prefetch_releated('ngo_areas'):
        for ngoArea in ngo.areas.all():
            if ngoArea.isFullAdmin:
                for membership in ngoArea.ngo.ngomember_set.filter(profile=profile):
                    if membership.isAreaAdmin:
                        return True
    return False

@staticmethod
def isCatastropheAdminByArea(profile : Profile, area : Area) -> type.BooleanType:
    """
    Internal Method to determine if a profile(user) is a catastrophe admin
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a full catastrophe admin
    """
    areaCatastrope = area.Catastrophe
    for placeholder in Ngo.objects.filter(areas=area, profile_set=profile, catastrophes=areaCatastrophe):
        return True
    for placeholder in Government.objects.filter(areas=area, profile_set=profile, catastrophes=areaCatastrophe):
        return True
    return False

@staticmethod
def canCreateSubArea(profile : Profile, area : Area) -> type.BooleanType:
    """
    Internal Method to determine if a profile(user) can create Sub Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a allowed to create a Sub Area
    """
    for government in Government.objects.filter(areas=area, profile_set=profile).prefetch_releated('governmentarea_areas'):
        for governmentArea in government.areas.all():
            if governmentArea.canCreateSubArea:
                for membership in governmentArea.government.profiles_set.filter(profile=profile):
                    if membership.isAreaAdmin:
                        return True
    return False

@staticmethod
def canManageNgo(profile : Profile, area : Area) -> type.BooleanType:
    """
    Internal Method to determine if a profile(user) can Manage an Ngo in an Area
    Should only be used in auth
    :author: Jasper
    :param profile: The profile to check the rights for
    :param area: The area for the authorization validation
    :return: Boolean whether a user is a can Manage an Ngo in an Area
    """
    for government in Government.objects.filter(areas=area, profile_set=profile).prefetch_releated('governmentarea_areas'):
        for governmentArea in government.areas.all():
            if governmentArea.canManageNgo:
                for membership in governmentArea.government.profiles_set.filter(profile=profile):
                    if membership.isAreaAdmin:
                        return True

def canDeleteElements(profile : Profile, area : Area) -> type.BooleanType:
    pass