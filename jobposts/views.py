"""
Views for the JobPost application.

This module contains class-based and function-based views for managing
job posts, including listing, viewing details, and redirecting to a chatbot
for specific job posts. The views implement search, sorting, and context
customization for enhanced user experience.
"""

from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from employer_profiles.models import InterviewFeedback
from .models import JobPost


class JobList(generic.ListView):
    """
    Displays a paginated list of job posts with optional search and sorting.

    Attributes:
        template_name (str): Path to the template for rendering the job list.
        paginate_by (int): Number of job posts to display per page.
    """

    template_name = "jobposts/job_index.html"
    paginate_by = 6

    def get_queryset(self):
        """
        Retrieves and filters the job posts based on search query and sorting.

        Returns:
            QuerySet: Filtered and sorted job posts.
        """

        queryset = JobPost.objects.all()
        search_query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(company_name__icontains=search_query) |
                Q(location__icontains=search_query)
            )

        if sort_by == 'created_on_asc':
            queryset = queryset.order_by('created_on')
        elif sort_by == 'created_on_desc':
            queryset = queryset.order_by('-created_on')
        elif sort_by == 'company_name_asc':
            queryset = queryset.order_by('company_name')
        elif sort_by == 'company_name_desc':
            queryset = queryset.order_by('-company_name')
        elif sort_by == 'location_asc':
            queryset = queryset.order_by('location')
        elif sort_by == 'location_desc':
            queryset = queryset.order_by('-location')
        else:
            # Default sorting
            queryset = queryset.order_by('-created_on')

        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds the current sorting option to the template context.

        Args:
            **kwargs: Additional context data.

        Returns:
            dict: Updated context data.
        """

        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort')
        return context


class JobDetailView(generic.DetailView):
    """
    Displays detailed information about a single job post.

    Attributes:
        model (Model): The JobPost model.
        template_name (str): Path to the template for rendering job details.
    """

    model = JobPost
    template_name = 'jobposts/job_detail.html'

    def split_text(self, text: str) -> list:
        """
        Splits a given text into a list of sentences.

        Args:
            text (str): The input text to split.

        Returns:
            list: A list of cleaned sentences.
        """

        prepared_text = (
            text.replace('. ', '.|')
            .replace('.\r\n', '.|')
            .split('|')
        )
        return [clean for item in prepared_text if (clean := item.strip())]

    def get_context_data(self, **kwargs):
        """
        Adds additional context data for rendering job details.

        Args:
            **kwargs: Additional context data.

        Returns:
            dict: Updated context data.
        """

        context = super().get_context_data(**kwargs)
        job_post = self.get_object()
        context['responsibilities_list'] = self.split_text(
            job_post.responsibilities
        )
        context['requirements_list'] = self.split_text(job_post.requirements)
        context['benefits_list'] = self.split_text(job_post.benefits)

        if self.request.user.is_authenticated:
            context['group'] = self.request.user.groups.all()[0].name

            if context['group'] == 'Candidate':
                candidate = self.request.user.candidate_profile
                has_interviewed = InterviewFeedback.objects.filter(
                    job_post=job_post,
                    candidate=candidate
                ).exists()
                context['has_interviewed'] = has_interviewed
            elif context['group'] == 'Employer':
                context['is_owner'] = job_post.author == self.request.user

        return context


def redirect_to_chatbot_index(request, job_post_id):
    """
    Redirects to the chatbot index page with the specified job post ID.

    Args:
        request (HttpRequest): The HTTP request object.
        job_post_id (int): The ID of the job post to pass as a parameter.

    Returns:
        HttpResponseRedirect: A redirect to the chatbot index page.
    """

    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    job_post = get_object_or_404(JobPost, id=job_post_id)
    return redirect(reverse('chatbot-index') + f'?job_post_id={job_post.id}')
