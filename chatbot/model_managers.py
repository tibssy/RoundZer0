from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from jobposts.models import JobPost
from .models import EvaluationRubric, InterviewPreparation
from candidate_profiles.models import Candidate, InterviewHistory
from datetime import date


class DatabaseManager:
    def __init__(self, scope):
        self.scope = scope
        self.job_post_id = self.get_job_id()
        self.user_id = self.get_user_id()

    def get_job_id(self):
        """Extract the job_post_id from the WebSocket query string."""
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        job_post_id_list = query_params.get('job_post_id', [])
        return job_post_id_list[0] if job_post_id_list else None

    def get_user_id(self):
        """Get the current user's ID from the scope."""
        if self.scope and 'user' in self.scope and self.scope['user'].is_authenticated:
            return self.scope['user'].id
        return None

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
        criteria = EvaluationRubric.objects.filter(job_post_id=self.job_post_id).values(
            'criterion', 'weight', 'scoring_guide'
        )
        return list(criteria)

    @database_sync_to_async
    def get_interview_preparation(self):
        """Fetch interview preparation details for a specific job post."""
        preparation = InterviewPreparation.objects.filter(job_post_id=self.job_post_id).values(
            'questions', 'interview_duration'
        ).first()
        return preparation

    @database_sync_to_async
    def send_feedback_to_user(self, company_name, feedback):
        """Sends interview feedback to a user's interview history."""
        try:
            candidate = Candidate.objects.get(user_id=self.user_id)
            interview_history_entry = InterviewHistory(
                candidate=candidate,
                company_name=company_name,
                feedback=feedback,
                interview_date=date.today()
            )
            interview_history_entry.save()
            print(f"Interview history saved for candidate {candidate} with company '{company_name}'.")
        except Candidate.DoesNotExist:
            print(f"Candidate with user ID {self.user_id} not found.")