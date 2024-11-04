from .consumers import EmailConsumer
from django.urls import path

websocket_urlpatterns = [
    path("ws/email/", EmailConsumer.as_asgi()),
]
