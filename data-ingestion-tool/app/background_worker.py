# import asyncio
# import heapq
# from typing import List, Tuple
# from app.state import ingestion_store
# from app.models import BatchStatus
# from app.schema import Priority
# from app.utils import fetch_external_api
# import time

# # Priority mapping for sorting: HIGH=0, MEDIUM=1, LOW=2 (lower is higher priority)
# priority_map = {
#     Priority.HIGH: 0,
#     Priority.MEDIUM: 1,
#     Priority.LOW: 2,
# }

# # A global priority queue for batches: items are tuples
# # (priority_value, created_time, ingestion_id, batch_index)
# batch_queue: List[Tuple[int, float, str, int]] = []

# # Track if the processor is running
# processor_running = False

# async def enqueue_batches(ingestion_id: str):
#     """
#     Enqueue all batches of an ingestion job into the global batch_queue,
#     respecting priority and created_time.
#     """
#     job = ingestion_store.get_ingestion(ingestion_id)
#     if not job:
#         return

#     created_time = time.time()

#     for idx, batch in enumerate(job.batches):
#         heapq.heappush(batch_queue, (
#             priority_map[job.priority],
#             created_time,
#             ingestion_id,
#             idx
#         ))

#     global processor_running
#     if not processor_running:
#         processor_running = True
#         asyncio.create_task(process_batches())

# async def process_batches():
#     """
#     Process batches one at a time with a 5 second rate limit.
#     """
#     global processor_running

#     while batch_queue:
#         priority_value, created_time, ingestion_id, batch_idx = heapq.heappop(batch_queue)
#         job = ingestion_store.get_ingestion(ingestion_id)
#         if not job:
#             continue
#         batch = job.batches[batch_idx]

#         # Skip if already completed
#         if batch.status == BatchStatus.COMPLETED:
#             continue

#         # Mark batch triggered
#         batch.status = BatchStatus.TRIGGERED

#         # Process each ID in the batch (simulate external API call)
#         for id_ in batch.ids:
#             await fetch_external_api(id_)

#         # Mark batch completed
#         batch.status = BatchStatus.COMPLETED

#         # Wait 5 seconds to respect rate limit
#         await asyncio.sleep(5)

#     processor_running = False



async def enqueue_batches(ingestion_id: str):
    # Simulate async processing of batches here
    # You can update batch status to COMPLETED after some processing
    pass
