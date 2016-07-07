from dcp.customForms.catastropheForms import CatastropheChoiceFrom
from dcp.models.notifications import *


def catForm(request):
    """
    Creates a catastrophe choice form for a user
    :author Jasper:
    :param request: Standard HTTP Request to process the catastrophe choice for
    :return: The catastrophe choice for a user
    """
    user = request.user
    notificationcount = None
    if user.is_authenticated():
        catastrophe = user.profile.currentCatastrophe
        if catastrophe is not None:
            return {'catChoiceForm': CatastropheChoiceFrom(initial={'catastrophe':catastrophe.id})}
        notificationcount = get_notifications(user).count()
        print(notificationcount)
        if notificationcount is None:
            notificationcount = 0
    return {'catChoiceForm': CatastropheChoiceFrom(),'notificationCount':notificationcount}
        