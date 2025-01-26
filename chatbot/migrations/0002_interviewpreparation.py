"""
This migration adds the InterviewPreparation model to the chatbot app.
It is responsible for storing technical questions, interview duration
and the connection to specific job posts.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Represents the database migration for the InterviewPreparation model.
    This class sets up the 'interview_preparation' table and fields for the
    technical questions, interview duration, a timestamp, and an optional
    foreign key relationship to a job post.
    """

    dependencies = [
        ("chatbot", "0001_initial"),
        ("jobposts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InterviewPreparation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "questions",
                    models.JSONField(
                        default=list, help_text="A list of technical questions."
                    ),
                ),
                (
                    "interview_duration",
                    models.PositiveIntegerField(
                        help_text="Duration of the interview in minutes."
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "job_post",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional: Tie this preparation to a specific job post.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_preparations",
                        to="jobposts.jobpost",
                    ),
                ),
            ],
        ),
    ]
