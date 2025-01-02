from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class JobPost(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES)
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    application_deadline = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='job_posts')

    class Meta:
        ordering = ['-created_on', 'author']

    def __str__(self):
        return f'{self.title} at {self.company_name} ({self.location})'
