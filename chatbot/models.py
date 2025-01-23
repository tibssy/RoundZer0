"""
This module defines the data models for evaluation rubrics and interview
preparation materials.

These models are used to standardize and improve the hiring process by
providing structured tools for evaluating candidates and preparing for
interviews.
"""

from django.db import models


class EvaluationRubric(models.Model):
    """
    Represents an evaluation rubric used to assess candidates.

    Attributes:
        job_post (:class:`jobposts.JobPost`, optional):  A foreign key to
            the JobPost model. Links this rubric to a specific job posting.
            Can be null and blank. Related name is 'evaluation_rubrics'.
            Help text: "Optional: Tie this rubric to a specific job post."
        criterion (str): The evaluation criterion.
        Help text: "The evaluation criterion."
        weight (decimal.Decimal):
            Weight of this criterion in the overall evaluation.
            Expressed as a percentage (e.g., 20.00 for 20%).
            Max digits: 5, Decimal places: 2.
            Help text: "Weight of this criterion in the overall evaluation
            (e.g., 20.00 for 20%)."
        scoring_guide (str): A guide for scoring based on this criterion.
            Example: 'Excellent: Clear and concise answer'.
            Help text: "Guide for scoring based on this criterion
            (e.g., 'Excellent: Clear and concise answer')."
        created_on (datetime.datetime): Timestamp indicating when the
            rubric was created. Auto-populated on creation.

    Methods:
        __str__:  Returns a string representation of the rubric.
    """

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
        help_text=(
            "Weight of this criterion in the overall evaluation "
            "(e.g., 20.00 for 20%)."
        )
    )
    scoring_guide = models.TextField(
        help_text=(
            "Guide for scoring based on this criterion "
            "(e.g., 'Excellent: Clear and concise answer')."
        )
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the rubric.

        The string includes the job post title (if applicable) and the
        first 50 characters of the criterion.

        Returns:
            str:  A formatted string representing the rubric.
        """

        return (
            f"Rubric for "
            f"{self.job_post.title if self.job_post else 'General'}: "
            f"{self.criterion[:50]}..."
        )


class InterviewPreparation(models.Model):
    """
    Represents interview preparation material,
    including questions and duration.

    Attributes:
        job_post (:class:`jobposts.JobPost`, optional):
            A foreign key to the JobPost model.
            Links this preparation to a specific job posting.
            Can be null and blank.
            Related name is 'interview_preparations'.
            Help text: "Optional: Tie this preparation to a specific job post."
        questions (list):
            A JSON field containing a list of technical questions for the
            interview.
            Defaults to an empty list. Help text: "A list of
            technical questions."
        interview_duration (int):  The duration of the interview in minutes.
            Help text: "Duration of the interview in minutes."
        created_on (datetime.datetime): Timestamp indicating when the
            preparation material was created. Auto-populated on creation.

    Methods:
        __str__:  Returns a string representation of the interview preparation.
    """

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
        """
        Returns a string representation of the interview preparation.

        The string includes the job post title (if applicable) and the
        number of questions.

        Returns:
            str:  A formatted string representing the interview preparation.
        """

        return (
            f"{self.job_post.title if self.job_post else 'General'} - "
            f"{len(self.questions)} questions"
        )
