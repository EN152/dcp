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
    route("websocket.disconnect",notifier_ws_disconnect),
    route("websocket.receive",notifier_ws_message)
]
notifications_count_routing = [
    # Kein Receive!
    route("websocket.connect",ws_notifier_count_connect),
    route("websocket.disconnect",ws_notifier_count_disconnect)
]
channel_routing = [
    include(chat_routing, path=r"^/chat/(?P<userid>\d+)/$"),
    route("chat-messages",msg_consumer),
    include(notifications_routing,path=r"^/notifications/$"),
    route("notification-messages",notify_msg_consumer),
    include(notifications_count_routing,path="^/notifications_count/$"),
    #include(notify_all_routing,path=r"^/notify_all/$"),
    #route("notificaty-all",public_notifier_msg_consumer)
]
