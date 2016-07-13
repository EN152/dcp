# -*- coding: utf-8 -*-

from dcp.importUrls import *
from dcp.customclasses.Helpers import  *
class Chat(View):
    form_class = sendMessage
    template = 'dcp/content/chat/chat.html'
    initial = {'Text': PleaseEnterMessageString}
    otherUser = None
    otherId = None
    currentUser = None
    conversation = None
    def dispatch(self, request, *args, **kwargs):
        """
        Überschreibe die dispatch Methode um direkt zur
        Chat-Überseite zu redirecten, falls der Chat bisher nicht existiert

        """
        if request.method != 'GET' and request.method != 'POST':
            return
        self.otherId = request.GET.get('userid')
        # Checke ob userid wirklich Integer ist
        try:
            int(self.otherId)
        except ValueError: # Der get Parameter war gar kein int..
            return HttpResponseRedirect(reverse('dcp:ChatOverview'))
        if self.otherId==None:
            return HttpResponseRedirect(reverse('dcp:ChatOverview'))
        self.otherUser = get_object_or_none(User,id=self.otherId)
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
        messages = Message.objects.filter(Conversation=self.conversation).order_by('SendTime')
        form = self.form_class()
        return dcp.viewerClasses.authentication.getPageAuthenticated(request, self.template,params={'message_list':messages,'otherUser':self.otherUser,'currentUser':self.currentUser,'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.cleaned_data['Text']
            # Neuer Eintrag in der Datenbank:
            Message.objects.create(Text=message,From=self.currentUser,To=self.otherUser,Conversation=self.conversation)
            url = url_with_querystring(reverse('dcp:Chat'),userid=self.otherUser.id)
            return HttpResponseRedirect(url)




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
        currentUser = request.user
        allConversations = Conversation.objects.filter(Starter=currentUser) | Conversation.objects.filter(Receiver=currentUser)
        initial_user = request.GET.get('userid')
        if initial_user is not None: # Nochmal abfragen, ob die angegebene Userid auch wirklich existiert
            # Das eingebundene Frame kontrolliert zusätzlcih, ob bereits ein konversation existiert
            user = get_object_or_none(User,id=initial_user) #type:user
            if user is None:
                initial_user = None
        mList = list()
        for conv in allConversations: #type:Conversation
            try:
                lastMessage = Message.objects.filter(Conversation=conv).latest('SendTime')
                mList.append(lastMessage)
            except:
                templatemessage = Message(From=conv.Starter,To=conv.Receiver,Text="Noch keine Nachricht",SendTime=conv.created_at,Conversation=conv)
                mList.append(templatemessage)
        return render(request,self.template,context={'last_message_list':mList,'initial_user':initial_user,'currentUser':request.user})
