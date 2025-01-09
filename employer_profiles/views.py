from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employer


@login_required
def employer_profile(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        return render(request, 'employer_profiles/no_profile.html')

    context = {'employer': employer}
    return render(request, 'employer_profiles/employer_profile.html', context)