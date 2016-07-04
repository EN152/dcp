# In consumers.py
from channels import  Group,Channel
from channels.sessions import channel_session
from django.utils import timezone
import locale

from dcp.customclasses.Helpers import get_object_or_none, get_user_display_name
from .models import Message, Conversation,User,Notification
from .models.notifications import *

from channels.auth import channel_session_user_from_http,http_session_user,channel_session_user
import json
# Connected to chat-messages
def msg_consumer(message):
    print("msg_consuumer called")
    conv_id = message['conversation']
    ownuser = get_object_or_none(User,id=message['user']) #type:User
    currentconv = get_object_or_none(Conversation,id=conv_id) #type:Conversation
    if currentconv is None:
        print("None")
        return
    if currentconv.Starter == ownuser:
        otheruser = currentconv.Receiver
    else:
        otheruser = currentconv.Starter
    sendTime = timezone.now()
    locale.setlocale(locale.LC_ALL,''   )
    Message.objects.create(From=ownuser,To=otheruser,Text=message.content['message'],Conversation=currentconv,SendTime=sendTime)
    fromusername = get_user_display_name(ownuser)
    tousername = get_user_display_name(otheruser)
    dict = {"message":message.content['message'],"From":ownuser.id,"To":otheruser.id,"Fromname":fromusername,"Toname":tousername,"sendTime":sendTime.strftime("%d. %B %Y %H:%M")}
    Group("chat-%s" % conv_id).send({
        "text": json.dumps(dict)
    })
    #Channel("notification-messages").send({"title":"Neue Nachricht","text":"Neue Nachricht","userid":otheruser.id})
    add_new_notification(title="Neue Nachricht",text="Neue Nachricht von "+otheruser.username,toUser=otheruser)
   # print("sended")


@channel_session
def ws_message(message,userid):
    # Stick the message onto the processing queue
    print("ws_message", message)
    print("Hier bin ich!")
    Channel("chat-messages").send({
        "conversation": message.channel_session['conversation'],
        "message": message['text'],
        "user":message.channel_session['user']
    })
# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message,userid):
    try:
        otherid = int(userid)
    except:
        return
    convobj = Conversation.getConversationOrNone(get_object_or_none(User,id=otherid),message.user)
    message.channel_session['conversation'] = convobj.id
    message.channel_session['user'] = message.user.id
    print("conversation: ", message.channel_session['conversation'])
    Group("chat-%s" % message.channel_session['conversation']).add(message.reply_channel)#

@channel_session
def ws_disconnect(message,userid):
    Group('chat-%s' % channel_session['conversation']).discard(message.reply_channel)
    return
#@#channel_session_user_from_http
#def ws_disconnect(message,userid):
   # conv=

def notify_msg_consumer(message):
    if message.get('userid') is None:
        group = "notifiy-all"
        user = None
        noticed = None
    else:
        user_id = message['userid']
        group = "notifier-%s" % user_id
        user = get_object_or_none(User,id=user_id) #type:User
        if user is None:
            return
        else:
            noticed = False
    #user_id = message['userid']
    #user = get_object_or_none(User,id=user_id) #type:User
    pubdate = timezone.now()
    Notification.objects.create(title=message['title'],text=message['text'],toUser=user,noticed=noticed,pubdate=pubdate,url=message.get('url'))
    url = message['url']
    if url is None:
        url = ""
    dict = {'title':message['title'],'text':message['text'],'pubdate':pubdate.strftime("%d. %B %Y %H:%M"),'url':url}
    Group(group).send({
        "text": json.dumps(dict)
    })

@channel_session_user_from_http
def notifier_ws_connect(message):
    message.channel_session['user'] = message.user.id
    Group("notifier-%s" % message.channel_session['user']).add(message.reply_channel)
    Group("notify-all").add(message.reply_channel)
@channel_session
def notifier_ws_disconnect(message):
    Group('notifier-%s' % message.channel_session['user']).discard(message.reply_channel)
    Group("notify-all").discard(message.reply_channel)
#def public_notifier_ws_connect(message):
#def public_notifier_ws_disconnect(message):
'''
def public_notifier_msg_consumer(message):
    #user_id = message['userid']
    #user = get_object_or_none(User,id=user_id) #type:User
    pubdate = timezone.now()
    Notification.objects.create(title=message['title'],text=message['text'],pubdate=pubdate)
    dict = {'title':message['title'],'text':message['text'],'pubdate':pubdate.strftime("%d. %B %Y %H:%M")}
    Group("notify-all").send({
        "text": json.dumps(dict)
    })'''