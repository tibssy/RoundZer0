from django.shortcuts import render
from django.views import generic
from .models import JobPost


class JobList(generic.ListView):
    queryset = JobPost.objects.all().order_by("created_on")
    template_name = "jobposts/index.html"
    paginate_by = 6


class JobDetailView(generic.DetailView):
    model = JobPost
    template_name = 'jobposts/job_detail.html'