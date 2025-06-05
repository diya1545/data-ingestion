from typing import Dict
from app.models import IngestionJob
from typing import List

class IngestionStore:
    def __init__(self):
        self.ingestions: Dict[str, IngestionJob] = {}

    def create_ingestion(self, ingestion_id: str, ids: List[int], priority):
        job = IngestionJob(ingestion_id, ids, priority)
        self.ingestions[ingestion_id] = job

    def get_ingestion(self, ingestion_id: str) -> IngestionJob:
        return self.ingestions.get(ingestion_id)

    def get_status(self, ingestion_id: str):
        job = self.get_ingestion(ingestion_id)
        if not job:
            return None
        return job.to_status_response()

ingestion_store = IngestionStore()
