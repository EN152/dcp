# In routing.py
from channels.routing import route, include
from dcp.consumers import ws_message, ws_connect, ws_disconnect,msg_consumer

chat_routing = [
    route("websocket.receive", ws_message),
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect)
]
channel_routing = [
    include(chat_routing, path=r"^/chat/(?P<userid>\d+)/$"),
    route("chat-messages",msg_consumer)
]
