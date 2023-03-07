from django.urls import path

from notifications.api import viewsets

app_name = "notifications"
urlpatterns = [
    path("push/send/", viewsets.PushNotificationView.as_view()),
]
