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
def edit_profile(request):
    candidate = get_object_or_404(Candidate, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=candidate, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('candidate_profile')
        else:
            messages.error(request, 'There were errors in your form.')
    else:
        form = EditProfileForm(instance=candidate, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
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

    return render(request, 'candidate_profiles/delete_profile_confirm.html')