from django.db import models

# Create your models here.
class EvaluationRubric(models.Model):
    job_post = models.ForeignKey(
        'jobposts.JobPost',
        on_delete=models.CASCADE,
        related_name='evaluation_rubrics',
        null=True,
        blank=True,
        help_text="Optional: Tie this rubric to a specific job post."
    )
    criterion = models.TextField(help_text="The evaluation criterion.")
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Weight of this criterion in the overall evaluation (e.g., 20.00 for 20%)."
    )
    scoring_guide = models.TextField(
        help_text="Guide for scoring based on this criterion (e.g., 'Excellent: Clear and concise answer')."
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rubric for {self.job_post.title if self.job_post else 'General'}: {self.criterion[:50]}..."


class InterviewPreparation(models.Model):
    job_post = models.ForeignKey(
        'jobposts.JobPost',
        on_delete=models.CASCADE,
        related_name='interview_preparations',
        null=True,
        blank=True,
        help_text="Optional: Tie this preparation to a specific job post."
    )
    questions = models.JSONField(
        help_text="A list of technical questions.",
        default=list
    )
    interview_duration = models.PositiveIntegerField(
        help_text="Duration of the interview in minutes."
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_post.title if self.job_post else 'General'} - {len(self.questions)} questions"
