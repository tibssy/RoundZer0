from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse
from .models import JobPost
from django.db.models import Q


class JobList(generic.ListView):
    template_name = "jobposts/job_index.html"
    paginate_by = 6

    def get_queryset(self):
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
            queryset = queryset.order_by('-created_on')  # Default sorting

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort')
        return context


class JobDetailView(generic.DetailView):
    model = JobPost
    template_name = 'jobposts/job_detail.html'

    def split_text(self, text: str) -> list:
        prepared_text = text.replace('. ', '.|').split('|')
        return [clean for item in prepared_text if (clean := item.strip())]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_post = self.get_object()
        context['responsibilities_list'] = self.split_text(job_post.responsibilities)
        context['requirements_list'] = self.split_text(job_post.requirements)
        context['benefits_list'] = self.split_text(job_post.benefits)
        return context


def redirect_to_chatbot_index(request, job_post_id):
    """Redirects to the chatbot index page, passing the job_post_id."""
    return redirect(reverse('chatbot-index') + f'?job_post_id={job_post_id}')