"""
Models for managing candidate profiles and interview history.

This module defines the models for storing candidate information
and tracking interview history.
"""

from django.contrib.auth.models import User
from django.db import models


class Candidate(models.Model):
    """
    Represents a candidate profile.

    Attributes:
        user (User): The user associated with the candidate.
        phone (str): The candidate's phone number.
        created_on (datetime): Timestamp of when the profile was created.
        updated_on (datetime): Timestamp of the last profile update.
        executive_summary (str): A brief overview of the candidate's
        professional background and goals.
        key_skills (str): Comma-separated skills of the candidate.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='candidate_profile'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    executive_summary = models.TextField(
        blank=True,
        null=True,
        help_text='A brief overview of your professional background and goals.'
    )
    key_skills = models.TextField(
        blank=True,
        null=True,
        help_text='Separate skills with commas (e.g., Python, Django, Java).'
    )

    def __str__(self):
        """
        Returns a string representation of the candidate.

        Returns:
            str: The candidate's full name if available; otherwise,
            their username.
        """

        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return self.user.username


class InterviewHistory(models.Model):
    """
    Represents the interview history of a candidate.

    Attributes:
        candidate (Candidate): The candidate associated with the interview.
        company_name (str): The name of the company where the interview
        was held.
        job_title (str): The job title for which the candidate interviewed.
        feedback (str): Feedback from the interview.
        interview_date (datetime): The date and time of the interview.
    """

    candidate = models.ForeignKey(
        Candidate, related_name='interviews', on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    interview_date = models.DateTimeField()

    def __str__(self):
        """
        Returns a string representation of the interview history.

        Returns:
            str: A string combining the company name and candidate's full name.
        """

        return (
            f'{self.company_name} - {self.candidate.user.first_name} '
            f'{self.candidate.user.last_name}'
        )
