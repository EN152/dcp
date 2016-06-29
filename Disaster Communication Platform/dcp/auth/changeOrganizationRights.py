from dcp.customForms.organizationForms import GovernmentAreaForm, NgoAreaForm
from dcp.models.profile import Profile
from django.http.request import HttpRequest
from dcp.models.organizations import Area, GovernmentArea, NgoArea
from dcp.auth.areaAuth import canCreateSubArea, canManageNgo, isAreaAdmin, isCatastropheAdminByArea
from dcp.dcpSettings import ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS


def changeGovernmentRight(request : HttpRequest, area :  Area, changeTo : bool) -> bool:
    """
    Processes the new rights for an government of the request & area into the 'changeTo' type
    This method only changes one permisson at time
    It does permission handeling via .areaAuth
    :author: Jasper
    :param request: The HTTP request which contains the new rights, build via GovernmentAreaForm
    :param area: The Area for which the rights should be changed
    :param changeTo: A boolean which determines whether a to upgrade or downgrade the rights
    :return: Boolean depending on success
    """
    user = request.user
    isSuperuser = user.is_superuser
    profile = user.profile # Profile.objects.get(user=user).prefetch_related('ngomember_set__ngo__areas', 'governmentmember_set__government__areas') # TODO query optimization
    form = GovernmentAreaForm(request.POST)
    success = False
    if not form.is_valid():
        return False
    governmentArea = form.cleaned_data.get('governmentArea')
    area = governmentArea.area

    if request.POST.get('isFullAdmin') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or (isSuperuser and ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS):
            governmentArea.isFullAdmin = changeTo
            success = True
    if request.POST.get('canDeleteElements') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or (isSuperuser and ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS):
            governmentArea.canDeleteElements = changeTo
            success = True
    if request.POST.get('canCreateSubArea') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or (isSuperuser and ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS):
            governmentArea.canCreateSubArea = changeTo
            success = True
    if request.POST.get('canManageNgo') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or (isSuperuser and ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS):
            governmentArea.canManageNgo = changeTo
            success = True

    if success:
        governmentArea.save()
    return success


def changeNgoRight(request : HttpRequest, area :  Area, changeTo : bool) -> bool:
    """
    Processes the new rights for an ngo of the request & area into the 'changeTo' type
    This method only changes one permisson at time
    It does permission handeling via .areaAuth
    :author: Jasper
    :param request: The HTTP request which contains the new rights, build via GovernmentAreaForm
    :param area: The Area for which the rights should be changed
    :param changeTo: A boolean which determines whether a to upgrade or downgrade the rights
    :return: Boolean depending on success
    """
    profile = request.user.profile # Profile.objects.get(user=user).prefetch_related('ngomember_set__ngo__areas', 'governmentmember_set__government__areas') # TODO query optimization
    form = NgoAreaForm(request.POST)
    success = False
    if not form.is_valid():
        return False
    ngoArea = form.cleaned_data.get('ngoArea')
    area = ngoArea.area

    if request.POST.get('isFullAdmin') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS:
            ngoArea.isFullAdmin = changeTo
            success = True
    if request.POST.get('canDeleteElements') and not success:
        if isAreaAdmin(profile, area) or isCatastropheAdminByArea(profile, area) or __canChangeNgoDeleteElements(profile, ngoArea) or ALLOW_SUPERUSER_TO_CHANGE_AREA_RIGHTS:
            ngoArea.canDeleteElements = changeTo
            success = True


def __canChangeNgoDeleteElements(profile : Profile, ngoArea : NgoArea) -> bool:
    """
    Determinens wheter a user is allowed to change the canChangeNgoDeleteElements by 'manageNgo'
    :author: Jasper
    :param ngoArea: The Area for which the rights should be changed
    :param changeTo: A boolean which determines whether a to upgrade or downgrade the rights
    :return: Boolean depending on success
    """
    area = ngoArea.area
    for placeholder in Profile.objects.governmentmember_set.filter(isareaadmin=True).governments.governmentarea_set.filter(canmanagengo = True, area=area):
        return True