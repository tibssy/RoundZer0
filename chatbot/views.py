from django.shortcuts import render

# Create your views here.
def chatbot_index(request):
    job_post_id = request.GET.get('job_post_id')
    context = {'job_post_id': job_post_id}
    return render(request, 'chatbot/index.html', context)

def chatbot_interview(request):
    return render(request, 'chatbot/interview.html')
