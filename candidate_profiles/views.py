from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Candidate


@login_required
def candidate_profile(request):
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        return render(request, 'candidate_profiles/no_profile.html')

    context = {'candidate': candidate}
    return render(request, 'candidate_profiles/candidate_profile.html', context)


@login_required
def edit_profile(request):
    pass


@login_required
def delete_profile_and_account(request):
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        messages.error(request, "Candidate profile not found.")
        return redirect('home')

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile and account have been deleted successfully.")
        return redirect('home')  # Redirect to the homepage

    return render(request, 'candidate_profiles/delete_profile_confirm.html')