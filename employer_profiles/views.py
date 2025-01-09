from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Employer
from .forms import EditProfileForm

@login_required
def employer_profile(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        return render(request, 'employer_profiles/no_profile.html')

    context = {'employer': employer}
    return render(request, 'employer_profiles/employer_profile.html', context)

@login_required
def edit_profile(request):
    employer = get_object_or_404(Employer, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('employer_profile')
        else:
            messages.error(request, 'There were errors in your form.')
    else:
        form = EditProfileForm(instance=employer)
    context = {'form': form}
    return render(request, 'employer_profiles/edit_profile.html', context)


@login_required
def delete_profile_and_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile and account have been deleted successfully.")
        return redirect('home')