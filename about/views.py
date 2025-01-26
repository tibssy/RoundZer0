"""
This module defines the view functions for the 'about' app.

It includes the 'about' view, which renders the about page.
"""

from django.shortcuts import render


def about(request):
    """
    Renders the 'About' page.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: An HTTP response rendering the 'about/about_index.html' template.
    :rtype: django.http.HttpResponse
    """

    return render(request, 'about/about_index.html')
