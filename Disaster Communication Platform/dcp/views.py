from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dcpcontainer import settings
from .models import Catastrophe


# The authentification for the login of the user

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        valid = bool(False)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Inactive user.")
        else:
            return render(request, 'dcp/design/login.html', {'notVaild': valid})
    return render(request, "dcp/design/login.html", {})



def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
    return render(request, "dcp/design/login.html", {})



@login_required
def index(request):
    return render(request, 'dcp/index.html', {})

def imprint(request):
    return render(request, 'dcp/content/imprint.html', {})
