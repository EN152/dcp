# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dcpcontainer import settings
from .models import Catastrophe


# The authentification for the login of the user
# Beispiel-View. Bitte beim Erstellen einer Seite selbstständig hinzufügen!  
#   
#class Login(View):
#    template = 'dcp/login.html'
#   
#    def get(self, request):
#        params = {}
#        return render(request, self.template, params)
#   
#   def post ist analog

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

class Login(View):
   template = 'dcp/content/spezial/login.html'
   
   def get(self, request):
        params = {}
        return render(request, self.template, params)   
        
   def post(self, request):
       params = {}
       return render(request, self.template, params)  
       #doSomething


class Index(View):
    template = 'dcp/index.html'
   
    def get(self, request):
        params = {}
        return render(request, self.template, params)
        
        
class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'
   
    def get(self, request):
        params = {}
        return render(request, self.template, params)        
   
   
class Suchen_Materielles(View):
    template = 'dcp/content/suchen/materielles.html'
   
    def get(self, request):
        params = {}
        return render(request, self.template, params)


class Suchen_Immaterielles(View):
    template = 'dcp/content/suchen/immaterielles.html'
   
    def get(self, request):
        params = {}
        return render(request, self.template, params)


class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'
   
    def get(self, request):
        params = {}
        return render(request, self.template, params)
