from django.contrib.auth.models import User
from django.db import models


class Candidate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="candidate_profile"
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username


class InterviewHistory(models.Model):
    candidate = models.ForeignKey(
        Candidate, related_name="interviews", on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=255)
    feedback = models.TextField(blank=True, null=True)
    interview_date = models.DateField()

    def __str__(self):
        return f"{self.company_name} - {self.candidate.user.first_name} {self.candidate.user.last_name}"
