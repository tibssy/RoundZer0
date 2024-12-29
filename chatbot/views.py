from django.shortcuts import render

# Create your views here.
def chatbot_index(request):
    return render(request, 'chatbot/index.html')

def chatbot_interview(request):
    return render(request, 'chatbot/interview.html')