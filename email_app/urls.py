from django.urls import path

from email_app.apps import EmailAppConfig
from email_app.views import message_list

app_name = EmailAppConfig.name

urlpatterns = [
    path("", message_list, name="message_list"),
]
