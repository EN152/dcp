from dcp.forms import CatastropheChoice
from dcp.customclasses import  Helpers
from dcp.models import Catastrophe,Profile

def catForm(request):
    """
    http://stackoverflow.com/questions/6166055/show-a-form-in-my-template-base-using-django
    :param request:
    :return:
    """
    if request.method == 'GET':
        if request.user.is_anonymous():
            return {'catChoiceForm': CatastropheChoice()}
        currentProfile= Profile.get_profile_or_create(request.user)
        currentCat = currentProfile.currentCatastrophe
        if currentCat!=None:
            return {
                'catChoiceForm':CatastropheChoice(initial={'catastrophe':currentCat.pk})
            }
        else:
            return {'catChoiceForm':CatastropheChoice()}
    elif request.method == 'POST':
        if request.user.is_anonymous():
            return {'catChoiceForm': CatastropheChoice()}
        newCatId = request.POST.get('catastrophe')
        p = Profile.get_profile_or_create(request.user)
        if request.user.is_anonymous():
            return {'catChoiceForm': CatastropheChoice()}
        result = p.setCatastropheById(newCatId)

        if result == True: # Valid Katastrophen ID
            return {
                'catChoiceForm': CatastropheChoice(initial={'catastrophe': request.user.profile.currentCatastrophe.pk})
            }
        else: # Komische id, mache nichts
            return {'catChoiceForm': CatastropheChoice()}