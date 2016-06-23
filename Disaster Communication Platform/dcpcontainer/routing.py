# In routing.py
from channels.routing import route
from dcp.consumers import ws_message

channel_routing = [
    route("websocket.receive", ws_message),
]