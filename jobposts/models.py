"""
Models for the job posts application.

Defines the database structure for job postings, including fields for job
details, employer information, and application deadlines.
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class JobPost(models.Model):
    """
    Represents a job posting created by an employer.

    Attributes:
        EMPLOYMENT_TYPE_CHOICES (list): A list of choices for employment types.
        title (str): The title of the job.
        company_name (str): The name of the company offering the job.
        location (str): The job's location.
        employment_type (str): The type of employment
        (e.g., full-time, part-time).
        description (str): A detailed description of the job.
        responsibilities (str): The main responsibilities associated
        with the job.
        requirements (str): The qualifications and skills required for the job.
        benefits (str): The benefits provided by the employer
        for this position.
        created_on (datetime): The date and time when the job post was created.
        updated_on (datetime): The date and time when the job post was
        last updated.
        application_deadline (date): The last date to apply for the job.
        author (User): The user who created the job post.

    Meta:
        ordering: Default ordering by creation date (newest first) and author.

    Methods:
        __str__: Returns a string representation of the job post, including
                the title, company name, and location.
    """

    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(
        max_length=2,
        choices=EMPLOYMENT_TYPE_CHOICES
    )
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    application_deadline = models.DateField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_posts'
    )

    class Meta:
        ordering = ['-created_on', 'author']

    def __str__(self):
        """
        Returns a human-readable string representation of the job post.

        Returns:
            str: A string containing the job title, company name, and location.
        """

        return f'{self.title} at {self.company_name} ({self.location})'
