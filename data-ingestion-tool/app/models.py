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

