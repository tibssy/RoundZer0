# Generated by Django 5.1.4 on 2025-01-01 02:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JobPost",
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
                ("title", models.CharField(max_length=255)),
                ("company_name", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("FT", "Full-time"),
                            ("PT", "Part-time"),
                            ("CT", "Contract"),
                            ("IN", "Internship"),
                        ],
                        max_length=2,
                    ),
                ),
                ("description", models.TextField()),
                ("requirements", models.TextField()),
                ("posted_date", models.DateField(auto_now_add=True)),
                ("application_deadline", models.DateField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
