from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from jobposts.models import JobPost
from .models import EvaluationRubric


class DatabaseManager:
    def __init__(self, scope):
        self.scope = scope
        self.job_post_id = self.get_job_id()

    def get_job_id(self):
        """Extract the job_post_id from the WebSocket query string."""
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        job_post_id_list = query_params.get('job_post_id', [])
        return job_post_id_list[0] if job_post_id_list else None

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
