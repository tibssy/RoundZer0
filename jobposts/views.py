from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
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
        context['responsibilities_list'] = [item.strip() for item in job_post.responsibilities.split('. ') if item.strip()]
        context['requirements_list'] = [item.strip() for item in job_post.requirements.split('. ') if item.strip()]
        context['benefits_list'] = [item.strip() for item in job_post.benefits.replace(',', '.').split('. ') if item.strip()]
        return context


def redirect_to_chatbot_index(request, job_post_id):
    """Redirects to the chatbot index page, passing the job_post_id."""
    return redirect(reverse('chatbot-index') + f'?job_post_id={job_post_id}')