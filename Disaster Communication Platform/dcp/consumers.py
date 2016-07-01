# In consumers.py
from channels import  Group,Channel
from channels.sessions import channel_session

from dcp.customclasses.Helpers import get_object_or_none
from .models import Message, Conversation, User
from channels.auth import channel_session_user_from_http,http_session_user,channel_session_user

# Connected to chat-messages
def msg_consumer(message,userid):
    print("msg_consuumer called")
    conv_id = message['conversation']
    ownuser = message.user
    currentconv = get_object_or_none(Conversation,id=conv_id) #type:Conversation
    if currentconv is None:
        print("None")
        return
    if currentconv.Starter == ownuser:
        otheruser = currentconv.Receiver
    else:
        otheruser = currentconv.Starter
    Message.objects.create(From=ownuser,To=otheruser,Text=message.content['text'],Conversation=currentconv)
    Group("chat-%s" % conv_id).send({
        "text": message.content['text'],
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
    print("conversation: ", message.channel_session['conversation'])
    Group("chat-%s" % message.channel_session['conversation']).add(message.reply_channel)#

@channel_session
def ws_disconnect(message,userid):
    Group('chat-%s' % str(1)).discard(message.reply_channel)
    return
#@#channel_session_user_from_http
#def ws_disconnect(message,userid):
   # conv=
 #