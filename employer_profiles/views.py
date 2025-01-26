"""
Django views for handling employer-related actions.

This module contains views that handle employer profile management,
job postings, job applications, and interview feedback.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from jobposts.models import JobPost
from jobposts.forms import JobPostForm
from chatbot.models import InterviewPreparation
from .models import Employer, InterviewFeedback
from .forms import EditProfileForm


@login_required
def employer_profile(request):
    """
    Displays the employer's profile.

    This view renders the employer's profile if it exists. If the employer
    does not have a profile, it redirects to a 'no profile' page.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        return render(
            request,
            'employer_profiles/no_profile.html'
        )

    context = {'employer': employer}
    return render(
        request,
        'employer_profiles/employer_profile.html',
        context
    )

@login_required
def edit_employer_profile(request):
    """
    Edits the employer's profile.

    This view allows the employer to update their profile. Upon successful form
    submission, the profile is saved, and a success message is displayed.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    employer = get_object_or_404(Employer, user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully.'
            )
            return redirect('employer_profile')

        messages.error(
            request,
            'There were errors in your form.'
        )

    form = EditProfileForm(instance=employer)
    context = {'form': form}
    return render(
        request,
        'employer_profiles/edit_employer_profile.html',
        context
    )

@login_required
def delete_employer_profile(request):
    """
    Deletes the employer's profile and account.

    This view allows the employer to delete their profile and account from
    the system. After deletion, the user is logged out, and a success message
    is displayed.
    """

    if not request.user.groups.filter(name='Employer').exists():
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

    return redirect('home')

@login_required
def my_jobs(request):
    """
    Displays the employer's job postings.

    This view renders a list of job postings created by the employer.
    The job postings are ordered by creation date.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    jobs = JobPost.objects.filter(author=request.user).order_by('-created_on')
    context = {'jobs': jobs}
    return render(
        request,
        'employer_profiles/my_jobs.html',
        context
    )

@login_required
def create_job(request):
    """
    Creates a new job posting.

    This view allows the employer to create a new job posting. If the form is
    valid, the job posting is saved, and interview preparation details (if any)
    are associated with the job posting.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.author = request.user
            job_post.save()

            questions = request.POST.getlist('questions')

            interview_duration = request.POST.get('interview_duration')
            if interview_duration:
                try:
                    interview_duration = int(interview_duration)
                except ValueError:
                    interview_duration = None

            if questions or interview_duration:
                interview_preparation = InterviewPreparation(
                    job_post=job_post,
                    questions=questions,
                    interview_duration=interview_duration
                )
                interview_preparation.save()

            return redirect('employer_jobs')
    else:
        form = JobPostForm()
    return render(
        request,
        'employer_profiles/create_job.html',
        {'form': form}
    )

@login_required
def edit_my_jobs(request, job_id):
    """
    Edits an existing job posting.

    This view allows the employer to edit a job posting. If the form is valid,
    the job posting is updated, and any interview preparation details are also
    updated or created if necessary.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    job = get_object_or_404(JobPost, id=job_id, author=request.user)
    interview_prep = InterviewPreparation.objects.filter(job_post=job).first()

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            job_post = form.save()

            questions = request.POST.getlist('questions')
            interview_duration = request.POST.get('interview_duration')
            if interview_duration:
                try:
                    interview_duration = int(interview_duration)
                except ValueError:
                    interview_duration = None

            if interview_prep:
                interview_prep.questions = questions
                interview_prep.interview_duration = interview_duration
                interview_prep.save()
            elif questions or interview_duration:
                InterviewPreparation.objects.create(
                    job_post=job_post,
                    questions=questions,
                    interview_duration=interview_duration
                )

            messages.success(
                request,
                'Your job posting has been updated successfully.'
            )
            return redirect('employer_jobs')

        messages.error(
            request,
            'There were errors in your form.'
        )
    else:
        form = JobPostForm(instance=job)

    context = {
        'form': form,
        'job': job,
        'interview_prep': interview_prep or InterviewPreparation()
    }
    return render(
        request,
        'employer_profiles/edit_my_jobs.html',
        context
    )

@login_required
def delete_my_job(request, job_id):
    """
    Deletes an existing job posting.

    This view allows the employer to delete a job posting. After deletion,
    a success message is displayed, and the employer is redirected to the
    list of their job postings.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    job = get_object_or_404(JobPost, id=job_id, author=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(
            request,
            'Job posting deleted successfully.'
        )
        return redirect('employer_jobs')

    return HttpResponseRedirect(reverse('employer_jobs'))

@login_required
def job_applications(request, job_id):
    """
    Displays job applications and interview feedback.

    This view shows the interview feedback for candidates who applied for a job
    posting. Employers can filter the feedback by top candidates and view
    feedback details.
    """

    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    job = get_object_or_404(JobPost, id=job_id, author=request.user)
    interview_feedbacks = (
        InterviewFeedback.objects.filter(job_post=job)
        .select_related('candidate__user')
        .order_by('-overall_score')
    )

    top_candidates = request.GET.get('top_candidates')
    if top_candidates:
        try:
            limit = int(top_candidates)
            interview_feedbacks = interview_feedbacks[:limit]
        except ValueError:
            pass

    processed_feedbacks = []
    for feedback in interview_feedbacks:
        processed_feedback_text = []
        for key, value in feedback.feedback_text.items():
            if key in ('overall_score', 'recommendation'):
                continue

            if isinstance(value, dict):
                key = ' '.join(key.split('_')).title()
                processed_feedback_text.append(
                    f'<strong>- {key} {value.get("score")}%: </strong>'
                    f'{value.get("comment")}'
                )
            else:
                processed_feedback_text.append(value)

        processed_feedbacks.append({
            'feedback': feedback,
            'processed_feedback_text': processed_feedback_text
        })

    context = {
        'job': job,
        'processed_feedbacks': processed_feedbacks
    }
    return render(
        request,
        'employer_profiles/job_applications.html',
        context
    )
