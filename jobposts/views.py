from django.shortcuts import render
from django.views import generic
from .models import JobPost


class JobList(generic.ListView):
    queryset = JobPost.objects.all().order_by("-created_on")  # Updated ordering to match model Meta
    template_name = "jobposts/index.html"
    paginate_by = 6


class JobDetailView(generic.DetailView):
    model = JobPost
    template_name = 'jobposts/job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_post = self.get_object()
        context['responsibilities_list'] = [f'{item.strip()}.' for item in job_post.responsibilities.split('.') if item.strip()]
        context['requirements_list'] = [f'{item.strip()}.' for item in job_post.requirements.split('.') if item.strip()]
        context['benefits_list'] = [f'{item.strip()}.' for item in job_post.benefits.replace(',', '.').split('.') if item.strip()]
        return context