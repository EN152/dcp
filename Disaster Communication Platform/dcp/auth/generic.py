from dcp.models.profile import Profile
from dcp.models.catastrophe import Catastrophe
from dcp.auth.catastropheAuth import isCatastropheAdmin
from dcp.customclasses.distance.distance import getAreasForElement
from dcp.auth.areaAuth import canDeleteElementsByArea

def isAllowedToDelete(catastrophe : Catastrophe, profile : Profile, location_x : float = None, location_y : float = None) -> bool:
    """
    Method to determine if a profile(user) is allowed delete an element in the catastrophe
    Optionaly it will check if a user has the permissons via a government or a ngo in any area based on the location data (location_x, location_y)
    :author: Jasper
    :param catastrophe: The catastrophe associated with the examined object
    :param profile: The profile to check the rights for
    :param location_x: (Optional) The object location_x (lat) data as float
    :param location_y: (Optional) The object location_y (lng) data as float
    :return: Boolean whether a user is an AreaAdmin
    """
    if profile.user.is_superuser:
        return True
    if isCatastropheAdmin(profile, catastrophe):
        return True
    if location_x and location_y:
        areas = getAreasForElement(location_x, location_y)
        for area in areas:
            if canDeleteElementsByArea(profile, area):
                return True
    
    return False