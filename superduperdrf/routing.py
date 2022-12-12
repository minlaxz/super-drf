from django.urls import path, re_path
from supervalve.comsumers import SuperConsumer

websocket_urlpatterns = [
    path("", SuperConsumer.as_asgi()),
    # re_path(r"^ws/(?P<room_name>[^/]+)/$", SuperConsumer.as_asgi()),
]
