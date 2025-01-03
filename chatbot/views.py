from django.shortcuts import render, get_object_or_404
from jobposts.models import JobPost


# Create your views here.
def chatbot_index(request):
    job_post_id = request.GET.get('job_post_id')
    job_post = None
    if job_post_id:
        job_post = get_object_or_404(JobPost, pk=job_post_id)
    context = {
        'job_post_id': job_post_id,
        'job_title': job_post.title if job_post else None,
        'company_name': job_post.company_name if job_post else None,
    }
    return render(request, 'chatbot/index.html', context)

def chatbot_interview(request):
    return render(request, 'chatbot/interview.html')
