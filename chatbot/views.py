from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from jobposts.models import JobPost
from .random_assistant import get_assistant


@method_decorator(login_required, name='dispatch')
class BaseChatbotView(TemplateView):
    """
    Base view for handling chatbot-related pages, providing common
    context data for all chatbot views, including job post details.

    :param kwargs: Additional keyword arguments.
    :return: A dictionary with context data for rendering templates.
    """

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for rendering the chatbot-related pages,
        including the job post details if available.

        :param kwargs: Additional keyword arguments.
        :return: A dictionary containing context data for the template.
        """

        context = super().get_context_data(**kwargs)
        job_post_id = self.request.GET.get('job_post_id')
        job_post = (
            get_object_or_404(JobPost, pk=job_post_id) if job_post_id else None
        )

        context.update({
            'job_post_id': job_post_id,
            'job_title': job_post.title if job_post else None,
            'company_name': job_post.company_name if job_post else None
        })

        self.request.session['job_post_id'] = job_post_id
        return context


@method_decorator(login_required, name='dispatch')
class ChatbotIndexView(BaseChatbotView):
    """
    View for displaying the chatbot index page, which serves as a welcome
    page for the interview.

    :param kwargs: Additional keyword arguments.
    :return: A rendered template for the welcome page.
    """

    template_name = 'chatbot/interview_welcome.html'


@method_decorator(login_required, name='dispatch')
class ChatbotInterviewView(BaseChatbotView):
    """
    View for conducting the chatbot interview, where the chatbot interacts
    with the user during the interview process.

    :param kwargs: Additional keyword arguments.
    :return: A rendered template for the interview page with context data.
    """

    template_name = 'chatbot/interview.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves context data for the chatbot interview page, including
        details about the assistant and video file for the interview.

        :param kwargs: Additional keyword arguments.
        :return: A dictionary with context data for the interview template.
        """

        context = super().get_context_data(**kwargs)
        name, voice = get_assistant()

        self.request.session['speaker'] = {'name': name, 'voice': voice}
        context['video_filename'] = f'videos/{name}.webm'

        return context


@method_decorator(login_required, name='dispatch')
class ChatbotInterviewEndView(BaseChatbotView):
    """
    View for displaying the end of the interview, providing a conclusion
    to the chatbot interview.

    :param kwargs: Additional keyword arguments.
    :return: A rendered template for the interview end page.
    """

    template_name = 'chatbot/interview_end.html'
