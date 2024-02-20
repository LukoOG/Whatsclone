from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [ 
    path('dm/<str:dm>', consumers.Chatconsumer.as_asgi()),
    path('new/<str:user>', consumers.Newchatconsumer.as_asgi())
]
