# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.decorators import login_required


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


class Login(View):
   template = 'dcp/content/spezial/login.html'
   
   def get(self, request):
        params = {}
        return render(request, self.template, params)   
        
   def post(self, request):
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
