from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from .models import Employer, InterviewFeedback
from .forms import EditProfileForm
from jobposts.models import JobPost
from jobposts.forms import JobPostForm
from chatbot.models import InterviewPreparation


@login_required
def employer_profile(request):
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    try:
        employer = request.user.employer_profile
    except Employer.DoesNotExist:
        return render(request, 'employer_profiles/no_profile.html')

    context = {'employer': employer}
    return render(request, 'employer_profiles/employer_profile.html', context)

@login_required
def edit_employer_profile(request):
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

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
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your profile and account have been deleted successfully.")
        return redirect('home')

@login_required
def my_jobs(request):
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    jobs = JobPost.objects.filter(author=request.user).order_by('-created_on')
    context = {'jobs': jobs}
    return render(request, 'employer_profiles/my_jobs.html', context)

@login_required
def create_job(request):
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
    return render(request, 'employer_profiles/create_job.html', {'form': form})

@login_required
def edit_my_jobs(request, job_id):
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

            messages.success(request, 'Your job posting has been updated successfully.')
            return redirect('employer_jobs')
        else:
            messages.error(request, 'There were errors in your form.')
    else:
        form = JobPostForm(instance=job)

    context = {'form': form, 'job': job, 'interview_prep': interview_prep or InterviewPreparation()}
    return render(request, 'employer_profiles/edit_my_jobs.html', context)

@login_required
def delete_my_job(request, job_id):
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    job = get_object_or_404(JobPost, id=job_id, author=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job posting deleted successfully.")
        return redirect('employer_jobs')

@login_required
def job_applications(request, job_id):
    if not request.user.groups.filter(name='Employer').exists():
        return HttpResponseRedirect(reverse('home'))

    job = get_object_or_404(JobPost, id=job_id, author=request.user)
    interview_feedbacks = InterviewFeedback.objects.filter(job_post=job).select_related('candidate__user').order_by('-overall_score')

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
                processed_feedback_text.append(f'<strong>- {key} {value.get("score")}%: </strong>{value.get("comment")}')
            else:
                processed_feedback_text.append(value)

        processed_feedbacks.append({
            'feedback': feedback,
            'processed_feedback_text': processed_feedback_text
        })

    context = {'job': job, 'processed_feedbacks': processed_feedbacks}
    return render(request, 'employer_profiles/job_applications.html', context)