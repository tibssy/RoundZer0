"""
This module contains unit tests for the 'home' app's views.

It includes test cases for verifying the status code, template used,
and content of the home page.  These tests use Django's testing
framework to simulate HTTP requests to the 'home' view and assert
expected responses.
"""

from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    """
    Test case for the 'home' view of the 'home' app.

    This test case includes tests to verify the status code,
    template used, and content of the home page.
    """

    def test_home_page_status_code(self):
        """
        Test that the home page returns a 200 OK status code.

        Verifies that a GET request to the 'home' URL returns
        a 200 status code, indicating a successful response.

        :return: None
        :rtype: None
        """

        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_used(self):
        """
        Test that the home page uses the correct template.

        Verifies that the 'home/index.html' template is used when
        rendering the home page.

        :return: None
        :rtype: None
        """

        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_home_page_content(self):
        """
        Test that the home page contains specific content.

        Verifies that the home page contains specific text, such as the
        welcome message, explore jobs link, and how it works section heading.

        :return: None
        :rtype: None
        """

        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, "Welcome to RoundZer0")
        self.assertContains(response, "Explore Jobs")
        self.assertContains(response, "How It Works")

    def test_home_page_no_jobs_available(self):
        """
        Test the home page content when there are no job openings available.

        Verifies that a specific message is displayed when there are
        no job openings.

        :return: None
        :rtype: None
        """

        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, "No job openings currently available.")
