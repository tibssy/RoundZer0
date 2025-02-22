"""
Django models for employer-related data in the application.

This module contains the Employer and InterviewFeedback models,
which handle employer profiles and feedback on interviews.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from candidate_profiles.models import Candidate
from jobposts.models import JobPost


class Employer(models.Model):
    """
    Represents an employer's profile in the system.

    This model stores information about an employer, including their
    user account, company name, company description, and phone number.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employer_profile'
    )
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class InterviewFeedback(models.Model):
    """
    Stores feedback given by an employer for a candidate's interview.

    This model includes feedback text, an overall score, and any recommendation
    made by the employer regarding the candidate.
    """

    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name='interview_feedbacks'
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name='employer_feedbacks'
    )
    feedback_text = models.JSONField()
    overall_score = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Overall score between 0 and 100.'
    )
    recommendation = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.candidate} on {self.job_post.title}"
