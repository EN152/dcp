from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def handler404(request):
    """
    Die eigene 404 view von django, aufgerufen von ein 404 eror kommt oder aus den views geschmissen wird.
    :author Vincent
    :param request:
    :return:
    """
    return render_to_response('dcp/content/spezial/404.html')