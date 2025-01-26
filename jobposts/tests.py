"""
This module contains unit tests for the 'jobposts' application.

Tests include:
- JobList view: Verifying status codes, templates, search, and sorting
  functionality.
- JobDetail view: Testing status codes, templates, and context data.

Dependencies:
- Django's built-in TestCase and Client classes.
- Models from the 'jobposts' application.
- Django's User model for creating test users.

The tests ensure the proper functionality of the job posting views and
validate that the application behaves as expected for various scenarios.
"""


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import JobPost


class JobPostViewTest(TestCase):
    """
    Test case for the 'jobposts' app's views.

    This test case includes tests to verify the status code, template used,
    context data, and search/sort functionality for JobList and JobDetailView.
    """

    def setUp(self):
        """Set up initial data for tests."""

        self.job_post1 = JobPost.objects.create(
            title='Software Engineer',
            company_name='Test Company',
            location='Test Location',
            employment_type='FT',
            description='Test Description 1',
            responsibilities='Test Responsibilities 1',
            requirements='Test Requirements 1',
            benefits='Test Benefits 1',
            application_deadline='2024-12-31',
            author=User.objects.create_user(
                username='testuser_author',
                password='testpassword'
            ),
        )
        self.job_post2 = JobPost.objects.create(
            title='Frontend Developer',
            company_name='Another Company',
            location='Another Location',
            employment_type='PT',
            description='Test Description 2',
            responsibilities='Test Responsibilities 2',
            requirements='Test Requirements 2',
            benefits='Test Benefits 2',
            application_deadline='2025-01-15',
            author=User.objects.create_user(
                username='testuser_author2',
                password='testpassword'
            ),
        )

        self.client = Client()

    def test_job_list_status_code(self):
        """Test that JobList view returns a 200 OK status code."""
        url = reverse('jobs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_job_list_template_used(self):
        """Test that JobList view uses the correct template."""
        url = reverse('jobs')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response,
            'jobposts/job_index.html'
        )

    def test_job_list_default_sorting(self):
        """Test that JobList view returns jobs sorted by newest by default."""
        url = reverse('jobs')
        response = self.client.get(url)
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post2, self.job_post1]
        )

    def test_job_list_search_functionality(self):
        """Test that JobList view filters job posts by search query."""
        url = reverse('jobs')
        response = self.client.get(url, {'q': 'Software'})
        job_list = response.context['object_list']
        self.assertEqual(list(job_list), [self.job_post1])

        response = self.client.get(url, {'q': 'Another Company'})
        job_list = response.context['object_list']
        self.assertEqual(list(job_list), [self.job_post2])

    def test_job_list_sorting_functionality(self):
        """Test that JobList view sorts job posts based on sort parameter."""
        url = reverse('jobs')

        # Oldest
        response = self.client.get(url, {'sort': 'created_on_asc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post1, self.job_post2]
        )

        # Newest
        response = self.client.get(url, {'sort': 'created_on_desc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post2, self.job_post1]
        )

        # Company name A-Z
        response = self.client.get(url, {'sort': 'company_name_asc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post2, self.job_post1]
        )

        # Company name Z-A
        response = self.client.get(url, {'sort': 'company_name_desc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post1, self.job_post2]
        )

        # Location A-Z
        response = self.client.get(url, {'sort': 'location_asc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post2, self.job_post1]
        )

        # Location Z-A
        response = self.client.get(url, {'sort': 'location_desc'})
        job_list = response.context['object_list']
        self.assertEqual(
            list(job_list),
            [self.job_post1, self.job_post2]
        )

    def test_job_detail_status_code(self):
        """Test that JobDetailView returns a 200 OK status code."""
        url = reverse('job_detail', kwargs={'pk': self.job_post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_job_detail_template_used(self):
        """Test that JobDetailView uses the correct template."""
        url = reverse('job_detail', kwargs={'pk': self.job_post1.pk})
        response = self.client.get(url)
        self.assertTemplateUsed(
            response,
            'jobposts/job_detail.html'
        )

    def test_job_detail_context_data(self):
        """Test that JobDetailView provides correct context data."""
        url = reverse('job_detail', kwargs={'pk': self.job_post1.pk})
        response = self.client.get(url)
        self.assertEqual(response.context['object'], self.job_post1)
        self.assertEqual(response.context['responsibilities_list'],
                         ['Test Responsibilities 1'])
        self.assertEqual(response.context['requirements_list'],
                         ['Test Requirements 1'])
        self.assertEqual(response.context['benefits_list'],
                         ['Test Benefits 1'])
