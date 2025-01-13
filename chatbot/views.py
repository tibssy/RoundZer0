from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from jobposts.models import JobPost
from .random_assistant import get_assistant


class BaseChatbotView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_post_id = self.request.GET.get('job_post_id')
        job_post = get_object_or_404(JobPost, pk=job_post_id) if job_post_id else None

        context.update({
            'job_post_id': job_post_id,
            'job_title': job_post.title if job_post else None,
            'company_name': job_post.company_name if job_post else None
        })

        self.request.session['job_post_id'] = job_post_id
        return context


class ChatbotIndexView(BaseChatbotView):
    template_name = 'chatbot/interview_welcome.html'


class ChatbotInterviewView(BaseChatbotView):
    template_name = 'chatbot/interview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name, voice = get_assistant()

        self.request.session['speaker'] = {'name': name, 'voice': voice}
        context['video_filename'] = f'videos/{name}.webm'

        return context
