# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dcp.models import *
from django.template import loader
from dcp.forms import *
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

def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("login/")

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
        return getPageAuthenticated(request, self.template)

    def post(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, 'dcp/index.html', params)
        else:
            return HttpResponseRedirect("login/")

class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)
   
   
class Suchen_Materielles(View):
    templatePath = 'dcp/content/suchen/materielles.html'

    def get(self, request):
        search_materials_list = Search_Material.objects.order_by('created_date')
        glyphicon_string_list = []
        category_type_string_list = []
        

        
        for s in search_materials_list:
            g_string = s.getGlyphiconString()
            c_string = s.getCategoryTypeAsString()
            glyphicon_string_list.append(g_string)
            category_type_string_list.append(c_string)

        context_list = zip(search_materials_list, glyphicon_string_list, category_type_string_list)
            

        template = loader.get_template(self.templatePath)
        context = {
            'context_list': context_list,
            'search_materials_list': search_materials_list,
            'glyphicon_string_list': glyphicon_string_list,
            'category_type_string_list': category_type_string_list
        }

        return HttpResponse(template.render(context,request))

    def post(self, request):
        params = {}
        return render(request, self.template, params)

class Suchen_Immaterielles(View):
    templatePath = 'dcp/content/suchen/immaterielles.html'

    def get(self, request):
        search_immaterials_list = Search_Immaterial.objects.order_by('created_date')
        template = loader.get_template(self.templatePath)
        context = {
            'search_immaterials_list': search_immaterials_list,
        }

        return HttpResponse(template.render(context,request))


class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

class Bieten(View):
    templatePath = 'dcp/content/bieten/bieten.html'

    def get(self, request):
        form = Offer_Form
        return render(request, self.templatePath, {
          'form' : form,
        })

    def post(self, request):
      form = Offer_Form(request.POST)
      if form.is_valid():
          title = form.cleaned_data['title']
          description = form.cleaned_data['description']
          return render(request, self.templatePath, {
          'form' : form,
          })

          '''
    if request.method=='GET':
            form = Offer_Form()
    else:
        form = Offer_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            #TodoItem.objects.create(description=description,deadline=deadline,progress=progress)
            #return django.http.HttpResponseRedirect(reverse_lazy('views.Bieten'))

    return render(request, 'dcp/content/bieten/bieten.html', {
        'form': form,
    })
  '''

class Bieten_Materielles(View):
    templatePath = 'dcp/content/bieten/materielles.html'

    def get(self, request):
        offer_materials_list = Offer_Material.objects.order_by('created_date')
        glyphicon_string_list = []
        category_type_string_list = []
        

        
        for o in offer_materials_list:
            g_string = o.getGlyphiconString()
            c_string = o.getCategoryTypeAsString()
            glyphicon_string_list.append(g_string)
            category_type_string_list.append(c_string)

        context_list = zip(offer_materials_list, glyphicon_string_list, category_type_string_list)
            

        template = loader.get_template(self.templatePath)
        context = {
            'context_list': context_list,
        }

        return HttpResponse(template.render(context,request))

    def post(self, request):
        params = {}
        return render(request, self.template, params)

class Bieten_Immaterielles(View):
    templatePath = 'dcp/content/bieten/immaterielles.html'

    def get(self, request):
        offer_immaterials_list = Offer_Immaterial.objects.order_by('created_date')
        template = loader.get_template(self.templatePath)
        context = {
            'offer_immaterials_list': offer_immaterials_list,
        }

        return HttpResponse(template.render(context,request))