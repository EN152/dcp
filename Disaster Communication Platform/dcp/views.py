# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

class Register(View):
    def post(self, request):
        if not request.user.is_authenticated():
            if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect("/login/")

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
               return render(request, self.template, {'notVaild': valid})
       return render(request, self.template, {})




class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect("../login/")



class Index(View):
    template = 'dcp/index.html'
    def get(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, 'dcp/index.html', params)
        else:
            return HttpResponseRedirect("login/")

    def post(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, 'dcp/index.html', params)
        else:
            return HttpResponseRedirect("login/")

class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'


    def get(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, self.template, params)
   
   
class Suchen_Materielles(View):
    template = 'dcp/content/suchen/materielles.html'

    def get(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, self.template, params)

    def post(self, request):
        params = {}
        return render(request, self.template, params)

class Suchen_Immaterielles(View):
    template = 'dcp/content/suchen/immaterielles.html'


    def get(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, self.template, params)


class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'

    def get(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, self.template, params)
