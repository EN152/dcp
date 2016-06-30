from dcp.customForms.catastropheForms import CatastropheChoiceFrom

def catForm(request):
    """
    Creates a catastrophe choice form for a user
    :author Jasper:
    :param request: Standard HTTP Request to process the catastrophe choice for
    :return: The catastrophe choice for a user
    """
    user = request.user
    if user.is_authenticated():
        catastrophe = user.profile.currentCatastrophe
        if catastrophe is not None:
            return {'catChoiceForm': CatastropheChoiceFrom(initial={'catastrophe':catastrophe.id})}
    return {'catChoiceForm': CatastropheChoiceFrom()}
        