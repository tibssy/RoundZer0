from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from jobposts.models import JobPost
from .models import EvaluationRubric, InterviewPreparation
from candidate_profiles.models import Candidate, InterviewHistory
from datetime import datetime


class DatabaseManager:
    def __init__(self, scope):
        self.scope = scope
        self.job_post_id = self.scope["session"].get("job_post_id")
        self.user_id = self._get_user_id()

    def _get_user_id(self):
        """Get the current user's ID from the scope."""
        user = self.scope.get('user')
        return user.id if user and user.is_authenticated else None

    @database_sync_to_async
    def get_user_profile(self):
        """Fetch the user profile of a candidate based on the user ID."""
        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
        except Candidate.DoesNotExist:
            return None
        else:
            return {
                'name': f'{candidate.user.first_name} {candidate.user.last_name}',
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
        """Fetch evaluation criteria for a specific job post."""
        return list(EvaluationRubric.objects.filter(job_post_id=self.job_post_id).values(
            'criterion', 'weight', 'scoring_guide'
        ))

    @database_sync_to_async
    def get_interview_preparation(self):
        """Fetch interview preparation details for a specific job post."""
        return InterviewPreparation.objects.filter(job_post_id=self.job_post_id).values(
            'questions', 'interview_duration'
        ).first()

    @database_sync_to_async
    def send_feedback_to_user(self, job_title, company_name, feedback):
        """Sends interview feedback to a user's interview history."""
        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
            InterviewHistory.objects.create(
                candidate=candidate,
                job_title=job_title,
                company_name=company_name,
                feedback=feedback,
                interview_date=datetime.now()
            )
            print(f"Interview history saved for candidate {candidate} with company '{company_name}'.")
        except Candidate.DoesNotExist:
            print(f"Candidate with user ID {self.user_id} not found.")