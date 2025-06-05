# from fastapi import FastAPI, HTTPException
# from fastapi.responses import JSONResponse
# from uuid import uuid4
# from typing import List
# import time

# from app.schema import IngestionRequest, Priority
# from app.state import ingestion_store
# from app.models import BatchStatus
# from app.background_worker import enqueue_batches

# app = FastAPI()

# MAX_BATCH_SIZE = 3

# def split_into_batches(ids: List[int], batch_size: int = MAX_BATCH_SIZE) -> List[List[int]]:
#     """Split the list of ids into batches of max batch_size"""
#     return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

# @app.post("/ingest")
# async def ingest_data(request: IngestionRequest):
#     # Validate priority
#     priority = request.priority
#     if priority not in Priority:
#         raise HTTPException(status_code=400, detail="Invalid priority value")

#     # Generate a unique ingestion_id
#     ingestion_id = str(uuid4())

#     # Split IDs into batches of max 3
#     batches = split_into_batches(request.ids)

#     # Prepare ingestion job data structure
#     ingestion_store.create_ingestion(ingestion_id, request.ids, priority)

#     # Create batches with IDs and default status
#     job = ingestion_store.get_ingestion(ingestion_id)
#     for batch_ids in batches:
#         job.add_batch(batch_ids)

#     # Enqueue batches for processing asynchronously
#     await enqueue_batches(ingestion_id)

#     return JSONResponse(content={"ingestion_id": ingestion_id})

# @app.get("/status/{ingestion_id}")
# def get_status(ingestion_id: str):
#     status_response = ingestion_store.get_status(ingestion_id)
#     if not status_response:
#         raise HTTPException(status_code=404, detail="Ingestion ID not found")
#     return status_response.dict()



from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from typing import List

from app.schema import IngestionRequest, Priority
from app.state import ingestion_store

app = FastAPI()

MAX_BATCH_SIZE = 3

def split_into_batches(ids: List[int], batch_size: int = MAX_BATCH_SIZE) -> List[List[int]]:
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]

@app.post("/ingest")
async def ingest_data(request: IngestionRequest):
    ingestion_id = str(uuid4())

    # Create ingestion job in store
    ingestion_store.create_ingestion(ingestion_id, request.ids, request.priority)

    # Split ids into batches
    batches = split_into_batches(request.ids)

    job = ingestion_store.get_ingestion(ingestion_id)

    # Add batches with batch_id as incremental integers (as strings)
    batch_counter = 1
    for batch_ids in batches:
        job.add_batch(batch_ids, batch_id=str(batch_counter))
        batch_counter += 1

    # Normally you would enqueue processing here and update status later
    # For demo, just assume batches are triggered

    return JSONResponse(content={"ingestion_id": ingestion_id})

@app.get("/status/{ingestion_id}")
def get_status(ingestion_id: str):
    status_response = ingestion_store.get_status(ingestion_id)
    if not status_response:
        raise HTTPException(status_code=404, detail="Ingestion ID not found")
    return status_response.dict()
