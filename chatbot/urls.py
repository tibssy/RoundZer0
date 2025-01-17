from django.urls import path
from .views import ChatbotIndexView, ChatbotInterviewView, ChatbotInterviewEndView


urlpatterns = [
    path('index/', ChatbotIndexView.as_view(), name='chatbot-index'),
    path('interview/', ChatbotInterviewView.as_view(), name='chatbot-interview'),
    path('interview/end/', ChatbotInterviewEndView.as_view(), name='chatbot-interview-end'),
]