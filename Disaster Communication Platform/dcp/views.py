from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.shortcuts import redirect

from .models import Catastrophe

def index(request):
    return render(request, 'dcp/index.html', {})

def imprint(request):
    return render(request, 'dcp/content/imprint.html', {})