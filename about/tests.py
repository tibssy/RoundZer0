"""
This module contains unit tests for the 'about' app's views.

It includes test cases for verifying the status code,
template used, and content of the about page. The tests use
Django's testing framework and simulate HTTP requests to the
'about' view.
"""

from django.test import TestCase
from django.urls import reverse


class AboutViewTest(TestCase):
    """
    Test case for the 'about' view of the 'about' app.

    This test case includes tests to verify the status code,
    template used, and content of the about page.
    """

    def test_about_page_status_code(self):
        """
        Test that the about page returns a 200 OK status code.

        :return: None
        :rtype: None
        """
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_about_page_template_used(self):
        """
        Test that the about page uses the correct template.

        :return: None
        :rtype: None
        """
        url = reverse('about')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, 'about/about_index.html')

    def test_about_page_content(self):
        """
        Test that the about page contains specific content.

        :return: None
        :rtype: None
        """
        url = reverse('about')
        response = self.client.get(url)
        self.assertContains(response, "About RoundZer0")
        self.assertContains(
            response, "Welcome to <strong>RoundZer0</strong>")
