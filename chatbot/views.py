from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def my_chatbot(request):
    return HttpResponse("Hello, chatbot!")