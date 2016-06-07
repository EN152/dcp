from dcp.forms import CatastropheChoice

def catForm(request):
    """
    http://stackoverflow.com/questions/6166055/show-a-form-in-my-template-base-using-django
    :param request:
    :return:
    """
    return {
        'catChoiceForm':CatastropheChoice()
    }