from . import views
from django.urls import path


urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
]