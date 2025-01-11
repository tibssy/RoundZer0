from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from jobposts.models import JobPost
from .random_assistant import get_assistant


class BaseChatbotView(TemplateView):
    def get_job_post(self):
        job_post_id = self.request.GET.get('job_post_id')
        if job_post_id:
            return get_object_or_404(JobPost, pk=job_post_id)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_post = self.get_job_post()
        context['job_post_id'] = self.request.GET.get('job_post_id')
        context['job_title'] = job_post.title if job_post else None
        context['company_name'] = job_post.company_name if job_post else None
        return context


class ChatbotIndexView(BaseChatbotView):
    template_name = 'chatbot/index.html'


class ChatbotInterviewView(BaseChatbotView):
    template_name = 'chatbot/interview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name, voice = get_assistant()
        self.request.session['speaker'] = {'name': name, 'voice': voice}
        context['video_filename'] = f'videos/{name}.webm'
        return context