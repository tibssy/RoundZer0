from django.shortcuts import render
from jobposts.models import JobPost


def home(request):
    # Fetch the three newest job posts
    newest_jobs = JobPost.objects.order_by('-created_on')[:3]
    return render(request, 'home/index.html', {'newest_jobs': newest_jobs})