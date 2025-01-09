from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Candidate
from .forms import EditProfileForm

@login_required
def candidate_profile(request):
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        return render(request, 'candidate_profiles/no_profile.html')

    context = {'candidate': candidate}
    return render(request, 'candidate_profiles/candidate_profile.html', context)

@login_required
def candidate_history(request):
    try:
        candidate = request.user.candidate_profile
    except Candidate.DoesNotExist:
        return render(request, 'candidate_profiles/no_profile.html')

    interviews = candidate.interviews.order_by('-interview_date')
    context = {'candidate': candidate, 'interviews': interviews}
    return render(request, 'candidate_profiles/candidate_history.html', context)

@login_required
def edit_profile(request):
    candidate = get_object_or_404(Candidate, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=candidate)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('candidate_profile')
        else:
            messages.error(request, 'There were errors in your form.')
    else:
        form = EditProfileForm(instance=candidate)
    context = {'form': form}
    return render(request, 'candidate_profiles/edit_profile.html', context)

@login_required
def delete_profile_and_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile and account have been deleted successfully.")
        return redirect('home')