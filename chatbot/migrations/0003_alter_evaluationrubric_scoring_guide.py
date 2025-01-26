"""
This migration modifies the EvaluationRubric model, specifically
updating the 'scoring_guide' field's help text to a more clear
and descriptive string.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Represents the database migration for updating the 'scoring_guide'
    field of the 'EvaluationRubric' model.
    This class changes the help text to be more illustrative.
    """

    dependencies = [
        ("chatbot", "0002_interviewpreparation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evaluationrubric",
            name="scoring_guide",
            field=models.TextField(
                help_text='Guide for scoring based on this criterion (e.g., "Excellent: Clear and concise answer").'
            ),
        ),
    ]
