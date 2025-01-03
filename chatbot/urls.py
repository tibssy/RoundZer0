from django.urls import path
from .views import ChatbotIndexView, ChatbotInterviewView


urlpatterns = [
    path('index/', ChatbotIndexView.as_view(), name='chatbot-index'),
    path('interview/', ChatbotInterviewView.as_view(), name='chatbot-interview'),
]