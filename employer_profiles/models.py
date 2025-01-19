from django.db import models
from django.contrib.auth.models import User
from candidate_profiles.models import Candidate
from jobposts.models import JobPost


class Employer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employer_profile"
    )
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class InterviewFeedback(models.Model):
    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name='interview_feedbacks'
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name='employer_feedbacks'
    )
    feedback_text = models.JSONField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.candidate} on {self.job_post.title}"