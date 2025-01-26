"""
Initial migration for the chatbot app, setting up the EvaluationRubric model.
This migration creates the necessary database table for storing evaluation
rubrics and their relation to job posts.
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Represents the initial database migration for creating the
    EvaluationRubric model. This class sets up the basic structure of the
    'evaluation_rubric' table, including fields for the evaluation criteria,
    their weight, scoring guide, creation timestamp, and an optional
    foreign key relationship to a job post.
    """

    initial = True

    dependencies = [
        ("jobposts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationRubric",
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
                ("criterion", models.TextField(help_text="The evaluation criterion.")),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Weight of this criterion in the overall evaluation (e.g., 20.00 for 20%).",
                        max_digits=5,
                    ),
                ),
                (
                    "scoring_guide",
                    models.TextField(
                        help_text="Guide for scoring based on this criterion (e.g., 'Excellent: Clear and concise answer')."
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "job_post",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional: Tie this rubric to a specific job post.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_rubrics",
                        to="jobposts.jobpost",
                    ),
                ),
            ],
        ),
    ]
