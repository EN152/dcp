# -*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from collections import defaultdict
from django.utils.http import urlencode
from braces import views
from dcp.models import *
from django.template import loader
from dcp.forms import *
from django.template.context_processors import request
from .forms import UserForm
from .models import Message
from .models import Catastrophe
from .forms import sendMessage # in Benutzung?
from django.core.urlresolvers import reverse,reverse_lazy
from django.db import IntegrityError
from dcp.customclasses.categorys import *
from dcp.customclasses import  Helpers
from django.http import HttpResponseForbidden


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
        catChoiceForm = CatastropheChoice
        return render(request, self.template, context={'catChoiceForm':catChoiceForm})
        
    def post(self, request):
       if request.method == "POST":
           username = request.POST['username']
           password = request.POST['password']
           catId = request.POST['catastrophe']

           valid = bool(False)
           user = authenticate(username=username, password=password)
           if user is not None:
               if user.is_active:
                   login(request, user)
                   Profile.get_profile_or_create(user).setCatastropheById(catId)
                   next = request.GET.get('next')
                   if next==None:
                       return HttpResponseRedirect("/")
                   else:
                       return HttpResponseRedirect(next)
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
                email = request.POST.get('email')
                password = request.POST.get('password')
                if email != None: # Der Nutzer will die Email ändern
                    user.email = email
                    user.save()
                if password != None:
                    User.set_password(request.user,password)
                    user.save()
                    return HttpResponseRedirect("/profil/")


class Logout(View):
    def get(self, request):
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


class TimelineView(View):
    def getCreateNew(self, request, good_typ, show_radius, create_new_glyphicon, page_title):
        templatePath = 'dcp/content/createNewGood.html'
        goods_list = sorted(Goods.getAllGoods(), key=lambda g: g.created_date, reverse=True)
        category_glyphicon_list = Categorys.getCategoryListAsGlyphiconString()
        category_name_list = Categorys.getCategoryListAsNameString()

        category_list = zip(category_glyphicon_list, category_name_list)
            
        template = loader.get_template(templatePath)
        context = {
            'goods_list': goods_list,
            'category_list' : category_list,
            'show_radius' : show_radius,
            'create_new_good_typ' : good_typ,
            'create_new_glyphicon': create_new_glyphicon,
            'page_title': page_title
        }

        return HttpResponse(template.render(context,request))

    def get_good_or_404(self, request):
        good = Goods.getGood(request.POST['good_type'], request.POST['good_id'])
        #if good is None:
         #   raise Http404
        return good

    def post(self, request):
        user = request.user
        if user.is_authenticated() and user.is_active:
            postIdentifier = request.POST.get('post_identifier')
            if postIdentifier == 'comment':
                form = Comment_Form(request.POST)
                if form.is_valid():
                    text = request.POST['text']
                    good = self.get_good_or_404(request)
                    if good.comments is None:
                        good.comments = Comment_Relation.objects.create()
                        good.save()
                    relation = good.comments
                    Comment.objects.create(text=text,user=user,relation=relation)
                    return HttpResponseRedirect('')

            if postIdentifier == 'contact_form':
                good = self.get_good_or_404(request)
                creatingUser =  good.user
                requestingUser = request.user
                # Schaue nach, ob schon eine Conv besteht..
                conv = Conversation.getConversationOrNone(userOne=self.currentUser, userTwo=self.otherUser)
                if conv is None: # Wenn noch keine Conversation da ist
                    Conversation.objects.create(Starter=creatingUser,Receiver=requestingUser)
                # Jetzt: Redirect
                url = url_with_querystring(reverse('dcp:Chat'), userid=creatingUser.id)
                return HttpResponseRedirect(url)

            if postIdentifier == 'create':
                # TODO form.vaild oder eine art der Sicherung, dass die Daten korrekt sind
                radius = None
                if radius in request.POST:
                    radiusSplit = request.POST['radius'].split(' ')
                    radius = radiusSplit[0]
                good_type = Goods.stringToGoodClass(request.POST.get('good_typ', None))
                if good_type is None :
                    return HttpResponse(status=404)
                title = request.POST['title']
                description = request.POST['description']
                catastrophe = get_object_or_404(Catastrophe, id=request.POST['catastrophe'])
                location_x = request.POST['location_x']
                location_y = request.POST['location_y']
                categoryString = request.POST['category']
                if categoryString == '':
                    return HttpResponse(code=400) # TODO Einen Fehler zurueckgeben, der makiert, dass eine Option gewählt werden muss
                category = Categorys.stringToCategoryTypeAsNumber(categoryString)
                if radius is not None:
                    good_type.objects.create(title=title, description=description, radius=radius, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=user)
                else:
                    good_type.objects.create(title=title, description=description, catastrophe=catastrophe, location_x=location_x, location_y=location_y, category=category, user=user)
                return HttpResponseRedirect('')
                # else:
                    # return HttpResponse(status=500)

            if postIdentifier == 'delete':
                good = self.get_good_or_404(request)
                if user.is_superuser or user == good.user:
                    if good.comments is not None:
                        good.comments.delete()
                    if good.bumps is not None:
                        good.bumps.delete()
                    if good.reports is not None:
                        good.reports.delete()
                    good.delete()
                    return HttpResponseRedirect('')

            if postIdentifier == 'bump':
                good = self.get_good_or_404(request)
                if good.bumps is None:
                    good.bumps = Bump_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Bump.objects.filter(relation = good.bumps, user = user)
                    if already_exists:
                        return HttpResponseRedirect('')
                relation = good.bumps
                Bump.objects.create(user=user,relation=relation)
                return HttpResponseRedirect('')

            if postIdentifier == 'report':
                good = self.get_good_or_404(request)
                if user == good.user:
                    return HttpResponse(status=403)
                relation = None
                if good.reports is None:
                    good.reports = Report_Relation.objects.create()
                    good.save()
                else:
                    already_exists = Report.objects.filter(relation = good.reports, user = user)
                    if already_exists:
                        return HttpResponseRedirect('')
                relation = good.reports
                Report.objects.create(user=user,relation=relation)
                return HttpResponseRedirect('')

        return HttpResponse(status=403)

class SearchMaterialView(TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Material', True, 'glyphicon-search', 'Suchen: Materielles')
    def post(self, request):
        return super().post(request)

class SearchImmaterialView(TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Search_Immaterial', True, 'glyphicon-search', 'Suchen: Immaterielles')
    def post(self, request):
        return super().post(request)

class OfferMaterialView(TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Material', False, 'glyphicon-transfer', 'Bieten: Materielles')
    def post(self, request):
        return super().post(request)

class OfferImmaterialView(TimelineView):
    def get(self, request):
        return super().getCreateNew(request, 'Offer_Immaterial', False, 'glyphicon-transfer', 'Bieten: Immaterielles')
    def post(self, request):
        return super().post(request)

class Suchen_Personen(View):
    template = 'dcp/content/suchen/personen.html'

    def get(self, request):
        return getPageAuthenticated(request, self.template)

class Bieten(LoginRequiredMixin,View):
    templatePath = 'dcp/content/bieten/bieten.html'


    def get(self, request):
        form = Offer_Form

class Chat(View):
    form_class = sendMessage
    template = 'dcp/content/chat/chat.html'
    initial = {'Text': dcp.customclasses.Helpers.PleaseEnterMessageString}
    otherUser = None
    otherId = None
    currentUser = None
    conversation = None
    def dispatch(self, request, *args, **kwargs):
        """
        Überschreibe die dispatch Methode um direkt zur
        Chat-Überseite zu redirecten, falls der Chat bisher nicht existiert

        """
        self.otherId = request.GET.get('userid')
        # Checke ob userid wirklich Integer ist
        try:
            int(self.otherId)
        except ValueError: # Der get Parameter war gar kein int..
            return HttpResponseRedirect(reverse('dcp:ChatOverview'))
        if self.otherId==None:
            return HttpResponseRedirect(reverse('dcp:ChatOverview'))
        self.otherUser = dcp.customclasses.Helpers.get_object_or_none(User,id=self.otherId)
        if self.otherUser == None: # User existiert nicht -> redirect
            return HttpResponseRedirect(reverse('dcp:ChatOverview'))
        self.currentUser = request.user
        # Hole die "andere" User Id
        # Existiert schon eine Conversation:
        self.conversation = Conversation.getConversationOrNone(userOne=self.currentUser,userTwo=self.otherUser)
        if self.conversation is None:
                return HttpResponseRedirect(reverse('dcp:ChatOverview'))  # Bisher keine Konversation
        return super(Chat, self).dispatch(request, *args, **kwargs)
    def get(self,request):
        """
        Zeigt entweder den bisherigen Nachrichtenverlauf an oder aber
        geht zurück zur Nachrichtenüberseite, falls bisher kein mit der bisherigen Person existiert
        :param request:
        :return: Gerendertes Template
        """
        messages = Message.objects.filter(Conversation=self.conversation)
        form = self.form_class()
        return render(request,self.template,context={'message_list':messages,'otherUser':self.otherUser,'currentUser':self.currentUser,'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.cleaned_data['Text']
            # Neuer Eintrag in der Datenbank:
            Message.objects.create(Text=message,From=self.currentUser,To=self.otherUser,Conversation=self.conversation)
            url = url_with_querystring(reverse('dcp:Chat'),userid=self.otherUser.id)
            return HttpResponseRedirect(url)

def url_with_querystring(path, **kwargs): #TODO: Refactor nach Helpers.
    return path + '?' + urlencode(kwargs)

class ChatOverview(View):
    template = 'dcp/content/chat/chat_overview.html'
    def get(self,request):
        """
        :author: Vincent
        Hole von allen Chats die der User hatte jeweils die letzte Nachricht
        Also From=currentUser oder To=currentUser -> Das sind alle Nachrichten
        TODO: Folgendes Verhalten klären? Was ist wenn ein User einen anderen
        kontaktiert, aber dann doch keine Nachricht schreibt? Soll er diesen Chat dann sehen oder nicht?
        Falls ja -> noch zu implementieren
        """
        messageDict = defaultdict(list)
        currentUser = request.user
        allConversations = Conversation.objects.filter(Starter=currentUser) | Conversation.objects.filter(Receiver=currentUser)
        all_chats = Message.objects.filter(Conversation__in = allConversations)
        # Jetzt teile die Listen jeweils auf in Chat Gruppen
        for m in all_chats:
            chatPatner = m.To if m.From.id == currentUser.id else m.From
            messageDict[chatPatner].append(m)
        tmpList = list()
        for key,value in messageDict.items():
            value.sort(key=lambda message: message.SendTime,reverse=True)
            tmpList.append(value)
        mList = list()
        for x in tmpList:
            mList.append(x[0])
        return render(request,self.template,context={'last_message_list':mList,'currentUser':request.user})
class UserAdminOverview(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/nutzer.html'
    def get(self,request):
        """
        :author: Vincent
        Zeigt - falls der User  ein Admin ist - alle Benutzer an und ermöglicht es dem Admin, Nutzer zu löschen
        """
        userList = User.objects.all()
        return render(request,self.template,context={'users': userList})

class CatastropheOverview(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/catastropheOverview.html'
    def get(self,request):
        """
        :author Vincent
        Gibt eine Liste an Katastrohpen aus, mit der Möglichkeit Einträge zu löschen, Namen zu editieren und Katastrophen
        hinzuzufügen
        :param request:
        :return:
        """
        catastropheList = Catastrophe.objects.all()
        return render(request,self.template,context={'catastrophes':catastropheList})

class CreateOrEditCatastrophe(views.SuperuserRequiredMixin,View):
    template = 'dcp/content/adminstrator/createOrEditCatastrophe.html'
    nextUrl = reverse_lazy('dcp:CatastropheOverview')
    def get(self,request):
        # Hat jemand die Id eine Katastrophe übergeben?
        inputId = request.GET.get('catid')
        if inputId  == None:
            form = CatastropheForm()
            return render(request, self.template, context={
                'form': form,
            })
        else:
            catastrophe = dcp.customclasses.Helpers.get_object_or_none(Catastrophe,id=inputId)
            if not catastrophe.isAbleToEdit(request.user):
                return HttpResponseForbidden(render(request,'dcp/content/spezial/403.html'))
            if catastrophe == None:
                return HttpResponseRedirect(self.nextUrl)
            else:
                form = CatastropheForm(instance=catastrophe)
                return render(request,self.template,context={'form':form})
    def post(self,request):
        form = CatastropheForm(request.POST)
        inputId = request.GET.get('catid')
        if form.is_valid():
            title = form.cleaned_data["Title"]
            location = form.cleaned_data["Location"]
            if inputId is None: # Keine Inputid -> Erstelle die Katastrophe direkt
                Catastrophe.objects.create(Title=title, Location=location)
                return HttpResponseRedirect(self.nextUrl)
            else: # Doch eine bereits bestehende Katastrophe?
                catastrophe = dcp.customclasses.Helpers.get_object_or_none(Catastrophe, id=inputId)
                if catastrophe is None:
                    return HttpResponseRedirect(self.nextUrl)
                else:
                    if not catastrophe.isAbleToEdit(request.user):
                        return HttpResponseForbidden(render(request, 'dcp/content/spezial/403.html'))
                    catastrophe.Title = title
                    catastrophe.location = location
                    catastrophe.PubDate = timezone.now()
                    catastrophe.save()
                    return HttpResponseRedirect(self.nextUrl)
        else: # Falls Form nicht valid
            return render(request, self.template, context={'form': form})


