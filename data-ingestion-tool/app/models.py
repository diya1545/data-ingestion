# from enum import Enum
# from typing import List
# from uuid import uuid4
# from app.schema import Priority, BatchStatus

# class Batch:
#     def __init__(self, ids: List[int]):
#         self.batch_id = str(uuid4())
#         self.ids = ids
#         self.status = BatchStatus.YET_TO_START

# class IngestionJob:
#     def __init__(self, ingestion_id: str, ids: List[int], priority: Priority):
#         self.ingestion_id = ingestion_id
#         self.priority = priority
#         self.batches = self.create_batches(ids)
    
#     def create_batches(self, ids: List[int], batch_size: int = 3) -> List[Batch]:
#         batches = []
#         for i in range(0, len(ids), batch_size):
#             batch_ids = ids[i:i+batch_size]
#             batches.append(Batch(batch_ids))
#         return batches
    
#     def is_completed(self):
#         return all(batch.status == BatchStatus.COMPLETED for batch in self.batches)
    
#     def get_overall_status(self):
#         statuses = {batch.status for batch in self.batches}
#         if statuses == {BatchStatus.YET_TO_START}:
#             return BatchStatus.YET_TO_START
#         if BatchStatus.TRIGGERED in statuses:
#             return BatchStatus.TRIGGERED
#         if statuses == {BatchStatus.COMPLETED}:
#             return BatchStatus.COMPLETED
#         # Default to triggered if mixed statuses
#         return BatchStatus.TRIGGERED
    
#     def add_batch(self, batch_ids: List[int]):
#         batch = Batch(batch_ids)       # Use singular 'batch', not 'batches'
#         self.batches.append(batch)



from typing import List
from app.schema import BatchStatus

class Batch:
    def __init__(self, batch_id: str, ids: List[int]):
        self.batch_id = batch_id
        self.ids = ids
        self.status = BatchStatus.TRIGGERED

class IngestionJob:
    def __init__(self, ingestion_id: str, ids: List[int], priority):
        self.ingestion_id = ingestion_id
        self.priority = priority
        self.batches: List[Batch] = []

    def add_batch(self, batch_ids: List[int], batch_id: str):
        batch = Batch(batch_id, batch_ids)
        self.batches.append(batch)

    def get_status(self):
        statuses = {batch.status for batch in self.batches}
        if statuses == {BatchStatus.YET_TO_START}:
            return BatchStatus.YET_TO_START
        if BatchStatus.TRIGGERED in statuses:
            return BatchStatus.TRIGGERED
        if statuses == {BatchStatus.COMPLETED}:
            return BatchStatus.COMPLETED
        return BatchStatus.TRIGGERED  # default fallback

    def to_status_response(self):
        from app.schema import StatusResponse, BatchResponse
        batches_response = [
            BatchResponse(batch_id=batch.batch_id, ids=batch.ids, status=batch.status)
            for batch in self.batches
        ]
        return StatusResponse(
            ingestion_id=self.ingestion_id,
            status=self.get_status(),
            batches=batches_response
        )

