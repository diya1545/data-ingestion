# from typing import Dict, Optional
# from app.models import IngestionJob
# from app.schema import BatchStatus, BatchResponse, StatusResponse

# class IngestionStore:
#     def __init__(self):
#         # ingestion_id -> IngestionJob
#         self.store: Dict[str, IngestionJob] = {}

#     def create_ingestion(self, ingestion_id: str, ids: list[int], priority):
#         job = IngestionJob(ingestion_id, ids, priority)
#         self.store[ingestion_id] = job

#     def get_ingestion(self, ingestion_id: str) -> Optional[IngestionJob]:
#         return self.store.get(ingestion_id)

#     def update_batch_status(self, ingestion_id: str, batch_id: str, status: BatchStatus):
#         job = self.get_ingestion(ingestion_id)
#         if not job:
#             return
#         for batch in job.batches:
#             if batch.batch_id == batch_id:
#                 batch.status = status
#                 break

#     def get_status(self, ingestion_id: str) -> Optional[StatusResponse]:
#         job = self.get_ingestion(ingestion_id)
#         if not job:
#             return None
        
#         batches_response = [
#             BatchResponse(
#                 batch_id=batch.batch_id,
#                 ids=batch.ids,
#                 status=batch.status
#             )
#             for batch in job.batches
#         ]

#         overall_status = job.get_overall_status()
#         return StatusResponse(
#             ingestion_id=job.ingestion_id,
#             status=overall_status,
#             batches=batches_response
#         )

# # Singleton store instance
# ingestion_store = IngestionStore()
 


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
