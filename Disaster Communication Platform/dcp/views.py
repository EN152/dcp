# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required
from dcpcontainer import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.context_processors import request
from .forms import UserForm
from .models import Message
from .forms import sendMessage
from django.core.urlresolvers import reverse,reverse_lazy
from .models import *
from django.db import IntegrityError

def getPageAuthenticated(request, template, params={}):
    if request.user.is_authenticated():
        return render(request, template, params)
    else:
        return HttpResponseRedirect("anmelden/")

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
    template = 'dcp/content/suchen/materielles.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

    def post(self, request):
        params = {}
        return render(request, self.template, params)

class Suchen_Immaterielles(View):
    template = 'dcp/content/suchen/immaterielles.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)


class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

class Chat(View):
    form_class = sendMessage
    template = 'dcp/content/chat/chat.html'
    initial = {'Text': 'Bitte Nachricht eingeben'}
    def get(self,request):
        # Hole die "andere" User Id
        otherId = request.GET['userid']
        currentUser = request.user
        otherUser = User.objects.get(id=otherId) #TODO: Exception einbauen!!!!
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
            otherUser = User.objects.get(id=otherId)  # TODO: Exception einbauen!!!!
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
