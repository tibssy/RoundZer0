# Generated by Django 5.1.4 on 2025-01-26 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("candidate_profiles", "0003_alter_interviewhistory_interview_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="key_skills",
            field=models.TextField(
                blank=True,
                help_text="Separate skills with commas (e.g., Python, Django, Java).",
                null=True,
            ),
        ),
    ]
