from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Candidate

@login_required
def candidate_profile(request):
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        # Handle the case where a logged-in user doesn't have a Candidate profile
        # You might want to redirect them to create a profile or show an error message
        return render(request, 'candidate_profiles/no_profile.html')  # You'll need to create this template

    context = {'candidate': candidate}
    return render(request, 'candidate_profiles/candidate_profile.html', context)