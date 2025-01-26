"""
DatabaseManager class for handling database operations related to candidates,
job posts, evaluation criteria, and interview preparation.

This class encapsulates various methods to interact with the database in an
asynchronous context using Channels, including fetching user profiles,
evaluation rubrics, interview preparation details, and sending feedback to
both candidates and employers. It also checks if the user belongs to the
'candidates' group or has staff privileges.

Methods:
    get_user_profile: Fetches the profile details of the authenticated
    candidate. get_job_post: Fetches the job post details using the
    job post ID. get_evaluation_criteria: Fetches the evaluation criteria for
    a job post. get_interview_preparation: Fetches interview preparation
    details for a job post. send_feedback_to_user: Sends feedback to a
    candidate's interview history. send_feedback_to_employer: Saves feedback
    data to the InterviewFeedback model. is_candidate: Checks if the current
    user is a candidate. is_staff: Checks if the current user is a
    staff member.
"""

from datetime import datetime
from channels.db import database_sync_to_async
from django.contrib.auth.models import Group
from jobposts.models import JobPost
from candidate_profiles.models import Candidate, InterviewHistory
from employer_profiles.models import InterviewFeedback
from .models import EvaluationRubric, InterviewPreparation


class DatabaseManager:
    """
    A manager for handling asynchronous database queries related to job posts,
    candidate profiles, evaluation rubrics, interview preparation,
    and feedback.

    This class is designed to manage and interact with database models in
    the context of an interview process, including fetching relevant
    information and saving feedback.
    """

    def __init__(self, scope):
        """
        Initializes the DatabaseManager instance with the given WebSocket scope
        and retrieves the job post and user IDs from the session.

        Args:
            scope (dict): The scope passed from the WebSocket consumer.
        """

        self.scope = scope
        self.job_post_id = self.scope['session'].get('job_post_id')
        self.user_id = self._get_user_id()

    def _get_user_id(self):
        """
        Retrieve the ID of the currently authenticated user from
        the WebSocket scope.

        This method checks the 'user' field in the scope dictionary to
        determine if the user is authenticated. If the user is authenticated,
        their ID is returned. Otherwise, it returns None, indicating
        no valid user is available.

        Returns:
            int or None: The ID of the authenticated user, or None if the user
            is not authenticated.
        """

        user = self.scope.get('user')
        return user.id if user and user.is_authenticated else None

    @database_sync_to_async
    def get_user_profile(self):
        """
        Fetch and return the user profile of a candidate associated with the
        current user ID.

        This method retrieves the candidate profile details such as the full
        name, email address, executive summary, and key skills. If the
        candidate is not found in the database, it returns None.

        The candidate is identified by their user ID, which is retrieved
        from the WebSocket scope.

        Returns:
            dict or None: A dictionary containing the candidate's profile
            details ('name', 'email', 'executive_summary', 'key_skills'), or
            None if the candidate does not exist.
        """

        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
        except Candidate.DoesNotExist:
            return None

        first_name = candidate.user.first_name
        last_name = candidate.user.last_name
        return {
            'name': f'{first_name} {last_name}',
            'email': candidate.user.email,
            'executive_summary': candidate.executive_summary,
            'key_skills': candidate.key_skills,
        }

    @database_sync_to_async
    def get_job_post(self):
        """Fetch a JobPost instance by its ID."""
        return JobPost.objects.get(pk=self.job_post_id)

    @database_sync_to_async
    def get_evaluation_criteria(self):
        """
        Fetch the evaluation criteria for a specific job post.

        This method retrieves the evaluation criteria associated with the
        job post, including the criterion, its weight, and the scoring guide.
        The criteria are returned as a list of dictionaries, each containing
        the relevant data.

        Returns:
            list: A list of dictionaries containing the evaluation criteria
            details (criterion, weight, and scoring guide).
        """

        return list(EvaluationRubric.objects.filter(
            job_post_id=self.job_post_id
        ).values('criterion', 'weight', 'scoring_guide'))

    @database_sync_to_async
    def get_interview_preparation(self):
        """
        Fetch interview preparation details for a specific job post.

        This method retrieves the interview questions and duration for a
        given job post. It returns the first available interview preparation
        entry for the job post, or None if no preparation details are found.

        Returns:
            dict or None: A dictionary containing the interview questions
            and duration for the job post, or None if no details are available.
        """

        return InterviewPreparation.objects.filter(
            job_post_id=self.job_post_id
        ).values('questions', 'interview_duration').first()

    @database_sync_to_async
    def send_feedback_to_user(self, job_title, company_name, feedback):
        """
        Save interview feedback to the candidate's interview history.

        This method records the feedback for a candidate's interview,
        associating it with the relevant job title, company name, and feedback
        text. The feedback is saved along with the interview
        date (the current time).

        Args:
            job_title (str): The job title of the interview.
            company_name (str): The name of the company conducting
            the interview.
            feedback (str): The feedback text to be recorded.

        If the candidate is not found, no action is taken.
        """

        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
            InterviewHistory.objects.create(
                candidate=candidate,
                job_title=job_title,
                company_name=company_name,
                feedback=feedback,
                interview_date=datetime.now()
            )
        except Candidate.DoesNotExist:
            pass

    @database_sync_to_async
    def send_feedback_to_employer(self, feedback_data):
        """
        Save the generated feedback to the InterviewFeedback model for an
        employer.

        This method takes a dictionary of feedback data, including the
        overall score and recommendation, and stores it in the
        `InterviewFeedback` model, associating it with the candidate and
        job post. The overall score is rounded and converted to an integer
        if valid; otherwise, it is set to None.

        Args:
            feedback_data (dict): A dictionary containing feedback information,
            including 'overall_score' and 'recommendation'.

        If the candidate or job post is not found, no action is taken.
        """

        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
            job_post = JobPost.objects.get(pk=self.job_post_id)
            overall_score = feedback_data.get('overall_score')

            if isinstance(overall_score, (int, float)):
                overall_score = int(round(overall_score))
            else:
                overall_score = None

            InterviewFeedback.objects.create(
                job_post=job_post,
                candidate=candidate,
                feedback_text=feedback_data,
                overall_score=overall_score,
                recommendation=feedback_data.get('recommendation')
            )
        except Candidate.DoesNotExist:
            pass
        except JobPost.DoesNotExist:
            pass

    @database_sync_to_async
    def is_candidate(self):
        """
        Check if the current user is a member of the 'candidates' group.

        This method checks if the current authenticated user belongs to the
        'Candidate' group by querying the user's groups. If the user is in the
        'Candidate' group, it returns True; otherwise, it returns False.

        Returns:
            bool: True if the user is a candidate, otherwise False.
        """

        if not self.user_id:
            return False
        try:
            user = self.scope['user']
            candidates_group = Group.objects.get(name='Candidate')
            return candidates_group in user.groups.all()
        except Group.DoesNotExist:
            return False

    @database_sync_to_async
    def is_staff(self):
        """
        Check if the current user has staff privileges.

        This method checks if the current user is marked as a staff member
        in the Django authentication system. It returns True if the user is a
        staff member, otherwise False.

        Returns:
            bool: True if the user is a staff member, otherwise False.
        """

        if not self.user_id:
            return False

        user = self.scope.get('user')
        return user.is_staff if user else False
