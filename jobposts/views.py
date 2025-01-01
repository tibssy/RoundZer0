from django.shortcuts import render
from django.views import generic
from .models import JobPost

# Create your views here.
# def jobs_index(request):
#     return render(request, 'jobposts/index.html')


class JobList(generic.ListView):
    # model = JobPost
    queryset = JobPost.objects.all().order_by("created_on")
    template_name = "jobposts/index.html"