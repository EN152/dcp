from dcp.forms import CatastropheChoice
from dcp.customclasses import  Helpers
from dcp.models import Catastrophe

def catForm(request):
    """
    http://stackoverflow.com/questions/6166055/show-a-form-in-my-template-base-using-django
    :param request:
    :return:
    """
    currentCatId = request.session.get(Helpers.sessionStringCatastrophe)
    currentCat = Helpers.get_object_or_none(Catastrophe,id=currentCatId)
    if currentCat!=None:
        return {
            'catChoiceForm':CatastropheChoice(initial={'catastrophe':currentCat.pk})
        }
    else:
        return {'catChoiceForm':CatastropheChoice()}