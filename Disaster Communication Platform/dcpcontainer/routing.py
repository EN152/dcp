# In routing.py
from channels.routing import route, include
from dcp.consumers import *

chat_routing = [
    route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect)
]
notifications_routing = [
    route("websocket.connect",notifier_ws_connect),
    route("websocket.disconnect",notifier_ws_disconnect)
]
'''
notify_all_routing =[
    route("websocket.connect",public_notifier_ws_connect),
    route("websocket.disconnect",public_notifier_ws_disconnect)
]'''

channel_routing = [
    include(chat_routing, path=r"^/chat/(?P<userid>\d+)/$"),
    route("chat-messages",msg_consumer),
    include(notifications_routing,path=r"^/notifications/$"),
    route("notification-messages",notify_msg_consumer)
    #include(notify_all_routing,path=r"^/notify_all/$"),
    #route("notificaty-all",public_notifier_msg_consumer)
]
