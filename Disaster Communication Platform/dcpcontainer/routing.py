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
channel_routing = [
    include(chat_routing, path=r"^/chat/(?P<userid>\d+)/$"),
    route("chat-messages",msg_consumer),
    include(notifications_routing,path=r"^/notifications/$"),
    route("notification-messages",notify_msg_consumer)
]
