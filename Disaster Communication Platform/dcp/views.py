# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render

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
   template = 'dcp/login.html'
   
   def get(self, request):
        params = {}
        return render(request, self.template, params)   


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
