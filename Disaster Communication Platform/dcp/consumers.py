# In consumers.py
from channels import  Group,Channel
from channels.sessions import channel_session
from django.utils import timezone
import locale

from dcp.customclasses.Helpers import get_object_or_none, get_user_display_name
from .models import Message, Conversation, User
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
    print("sended")


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
 #