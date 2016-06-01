# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.models import User
from dcp.models import *
from django.template import loader
from dcp.forms import * # in Benutzung?
from django.template.context_processors import request
from .forms import UserForm # in Benutzung?
from .models import Message
from .forms import sendMessage # in Benutzung?
from django.core.urlresolvers import reverse,reverse_lazy
from django.db import IntegrityError


def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("/anmelden/")

class Register(View):
    def post(self, request):
        if not request.user.is_authenticated():
            if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                email = request.POST['email']
                user = User.objects.create_user(username, email, password)
                user.save()
                return HttpResponseRedirect("/anmelden/")

class Login(View):
    template = 'dcp/content/spezial/anmelden.html'

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
   
class MyProfile(View):
    template = 'dcp/content/spezial/profil.html'
    
    def get(self, request):
        return getPageAuthenticated(request, self.template)
        
class EditProfile(View):
    template = 'dcp/content/spezial/profilBearbeiten.html'
    
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        form = UserForm(initial={'email' : user.email})
        return getPageAuthenticated(request, self.template, {'form': form})

    # Bugfixing nötig!
    def post(self,request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                if request.POST['email'] != None or request.POST['password'] != None:
                    mail = request.POST['email']
                    password = request.POST['password']
                    User.set_password(request.user, password)
                    user.save()
                    return HttpResponseRedirect("/profil/")


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect("../anmelden/")


class Karten(View):
    template = 'dcp/content/orte/karten.html'

    def get(self, request):
        listOfGoods = []
        for oneGood in Search_Material.objects.all():
            listOfGoods.append((oneGood.location_x,oneGood.location_y))
        for oneGood in Offer_Immaterial.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y))
        for oneGood in Offer_Material.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y))
        for oneGood in Search_Immaterial.objects.all():
            listOfGoods.append((oneGood.location_x, oneGood.location_y))
        if request.user.is_authenticated():
            return render(request, self.template, {'goods': listOfGoods})


class Index(View):
    template = 'dcp/index.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

    def post(self, request):
        if request.user.is_authenticated():
            params = {}
            return render(request, 'dcp/index.html', params)
        else:
            return HttpResponseRedirect("anmelden/")


class Suchen(View):
    template = 'dcp/content/suchen/suchen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)


class Suchen_Materielles(View):
    templatePath = 'dcp/content/suchen/materielles.html'

    def get(self, request):
        search_materials_list = Search_Material.objects.order_by('created_date').reverse()
        glyphicon_string_list = []
        category_type_string_list = []
        comment_list = []
        
        for s in search_materials_list:
            g_string = s.getGlyphiconString()
            c_string = s.getCategoryTypeAsString()
            glyphicon_string_list.append(g_string)
            category_type_string_list.append(c_string)
            comment_list.append(s.getComments())

        context_list = zip(search_materials_list, glyphicon_string_list, category_type_string_list, comment_list)
            
        template = loader.get_template(self.templatePath)
        context = {
            'context_list': context_list,
            'search_materials_list': search_materials_list,
            'glyphicon_string_list': glyphicon_string_list,
            'category_type_string_list': category_type_string_list,
            'comment_list': comment_list,
            'comment_form': Comment_Form
        }

        return HttpResponse(template.render(context,request))

    def post(self, request):
        user = request.user
        if user.is_authenticated():
            form = Comment_Form(request.POST)
            if form.is_valid():
                text = request.POST['text']
                search_material_id = request.POST['search_material_id']
                search_material = Search_Material.objects.get(id=search_material_id)
                relation = search_material.comments
                Comment.objects.create(text=text,user=user,relation=relation)
                return HttpResponseRedirect('/suchen/materielles/')

        else:
            return HttpResponse(status=403)

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


class Chat(View):
    form_class = sendMessage
    template = 'dcp/content/chat/chat.html'
    initial = {'Text': 'Bitte Nachricht eingeben'}
    def get(self,request):
        # Hole die "andere" User Id
        otherId = request.GET['userid']
        currentUser = request.user
        otherUser = get_object_or_404(User, id=otherId) # TODO Exception
        # Ok, fremdschlüssel sind da, nun die Liste holen:
        chats = (Message.objects.filter(From=otherUser.id,To=currentUser) | Message.objects.filter(From=currentUser,To=otherUser)).order_by('SendTime') # Filtern und Sortieren
        form = self.form_class()
        return render(request,self.template,context={'message_list':chats,'otherUser':otherUser,'currentUser':currentUser,'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.cleaned_data['Text']
            otherId = request.GET['userid']
            currentUser = request.user
            otherUser = get_object_or_404(User, id=otherId)  # TODO Exception
            Message.objects.create(Text=message,From=currentUser,To=otherUser)
            url = url_with_querystring(reverse('dcp:Chat'),userid=otherUser.id)
            return HttpResponseRedirect(url)
            #Neuer Eintrag in der Datenbank:

def url_with_querystring(path, **kwargs):
    return path + '?' + urlencode(kwargs)

class Overview(View):
    template = 'dcp/content/chat/chat_overview.html'
    def get(self,request):
        # Hole von allen Chats die der User hatte jeweils die letzte Nachricht
        # Also From=currentUser oder To=currentUser -> Das sind alle Nachrichten
        messageDict = defaultdict(list)
        currentUser = request.user
        all_chats = Message.objects.filter(From=currentUser) | Message.objects.filter(To=currentUser)
        # Jetzt teile die Listen jeweils auf in Chat Gruppen
        for m in all_chats:
            chatPatner = m.To if m.From.id == currentUser.id else m.From
            messageDict[chatPatner].append(m)
        #tmpList = map[lambda mList: mList.sort(key=lambda message: message.SendTime), messageDict.items()]
        tmpList = list()
        for key,value in messageDict.items():
            value.sort(key=lambda message: message.SendTime,reverse=True)
            tmpList.append(value)
        mList = list()
        for x in tmpList:
            mList.append(x[0])
        return render(request,self.template,context={'last_message_list':mList,'currentUser':request.user})