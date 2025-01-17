from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Employer
from .forms import EditProfileForm
from jobposts.models import JobPost
from jobposts.forms import JobPostForm


@login_required
def employer_profile(request):
    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        return render(request, 'employer_profiles/no_profile.html')

    context = {'employer': employer}
    return render(request, 'employer_profiles/employer_profile.html', context)

@login_required
def edit_employer_profile(request):
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
    return render(request, 'employer_profiles/edit_employer_profile.html', context)

@login_required
def delete_employer_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile and account have been deleted successfully.")
        return redirect('home')

@login_required
def my_jobs(request):
    jobs = JobPost.objects.filter(author=request.user).order_by('-created_on')
    context = {'jobs': jobs}
    return render(request, 'employer_profiles/my_jobs.html', context)

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.author = request.user
            job_post.save()
            return redirect('employer_jobs')
    else:
        form = JobPostForm()
    return render(request, 'employer_profiles/create_job.html', {'form': form})