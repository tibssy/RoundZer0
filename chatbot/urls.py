from . import views
from django.urls import path


urlpatterns = [
    path('', views.chatbot_index, name='chatbot-index'),
    path('interview/', views.chatbot_interview, name='chatbot-interview')
]
