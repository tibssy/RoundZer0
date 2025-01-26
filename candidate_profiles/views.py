"""
Views for handling candidate profiles, interview history, and related actions.

This module contains view functions that enable candidates to manage their
profiles, view their interview history, edit their details, and delete
records securely.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from .models import Candidate, InterviewHistory
from .forms import EditProfileForm


@login_required
def candidate_profile(request):
    """
    Display the candidate's profile if the user is in the 'Candidate' group.

    Redirects to the home page if the user does not belong to the 'Candidate'
    group. If the candidate profile does not exist, renders a 'no profile'
    page.
    """

    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('home'))

    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        return render(
            request,
            'candidate_profiles/no_profile.html'
        )

    context = {'candidate': candidate}
    return render(
        request,
        'candidate_profiles/candidate_profile.html',
        context
    )


@login_required
def candidate_profile_view(request, candidate_id):
    """
    Display the profile of a specific candidate.

    Fetches the candidate by their ID. If the candidate does not exist,
    raises a 404 error.
    """

    candidate = get_object_or_404(Candidate, pk=candidate_id)
    context = {'candidate': candidate}
    return render(
        request,
        'candidate_profiles/candidate_profile.html',
        context
    )


@login_required
def candidate_history(request):
    """
    Display the interview history for the logged-in candidate.

    Redirects to the home page if the user is not in the 'Candidate' group.
    If the candidate profile does not exist, renders a 'no profile' page.
    """

    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('home'))

    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        return render(
            request,
            'candidate_profiles/no_profile.html'
        )

    interviews = candidate.interviews.order_by('-interview_date')
    context = {'candidate': candidate, 'interviews': interviews}
    return render(
        request,
        'candidate_profiles/candidate_history.html',
        context
    )


@login_required
def edit_candidate_profile(request):
    """
    Allow candidates to edit their profile information.

    Validates the form and updates the candidate's details, including their
    first name, last name, and profile fields. Redirects to the candidate
    profile upon success.
    """

    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('home'))

    candidate = get_object_or_404(Candidate, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=candidate)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('candidate_profile')
        messages.error(
            request,
            'There were errors in your form.'
        )

    form = EditProfileForm(instance=candidate)
    context = {'form': form}
    return render(
        request,
        'candidate_profiles/edit_candidate_profile.html',
        context
    )


@login_required
def delete_candidate_profile(request):
    """
    Allow candidates to delete their profile and account.

    Logs out the user and deletes their account upon confirmation.
    Redirects to the home page with a success message.
    """

    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(
            request,
            'Your profile and account have been deleted successfully.'
        )
        return redirect('home')

    return HttpResponseRedirect(reverse('home'))


@login_required
def delete_interview(request, interview_id):
    """
    Allow candidates to delete an interview history record.

    Ensures that the logged-in user is authorized to delete the specified
    interview record. Redirects to the interview history upon success or
    failure.
    """

    if not request.user.groups.filter(name='Candidate').exists():
        return HttpResponseRedirect(reverse('home'))

    interview = get_object_or_404(InterviewHistory, id=interview_id)
    if interview.candidate.user == request.user:
        if request.method == 'POST':
            interview.delete()
            messages.success(
                request,
                'Interview history deleted successfully.'
            )
            return redirect('candidate_history')
        return redirect('candidate_history')

    messages.error(
        request,
        'You are not authorized to delete this interview history.'
    )
    return redirect('candidate_history')
