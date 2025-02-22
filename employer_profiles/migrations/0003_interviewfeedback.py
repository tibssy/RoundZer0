# Generated by Django 5.1.4 on 2025-01-19 00:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidate_profiles", "0003_alter_interviewhistory_interview_date"),
        ("employer_profiles", "0002_employer_company_description"),
        ("jobposts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InterviewFeedback",
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
                ("feedback_text", models.JSONField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employer_feedbacks",
                        to="candidate_profiles.candidate",
                    ),
                ),
                (
                    "job_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_feedbacks",
                        to="jobposts.jobpost",
                    ),
                ),
            ],
        ),
    ]
