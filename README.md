# Data-ingestion

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate the virtual environment (Windows using cmd): venv\Scripts\activate
3. Install requirements: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload --port 5000`

### POST /ingest
URL: http://localhost:5000/ingest
Headers: Content-Type: application/json

Body (raw → JSON):

{

  "ids": [1, 2, 3],
  
  "priority": "HIGH"
  
}

Response:

{

  "ingestion_id": "abc123-uuid"
  
}



### GET /status
After getting the ingestion_id from the above POST response, test the status:
URL: http://localhost:5000/status/<your_ingestion_id>

Response: 

{
  "ingestion_id": "abc123-uuid",
  "status": "triggered",
  "batches": [
    {
      "batch_id": "batch1-uuid",
      "ids": [1, 2, 3],
      "status": "triggered"
    },
    {
      "batch_id": "batch2-uuid",
      "ids": [4, 5],
      "status": "triggered"
    }
  ]
}

## 📸 Test Run Screenshot

I have added the successful screenshots of the running application under the assets folder. You can access them directly from there:

![Test Results](assets/get_testing.png)
![Test Results](assets/post_testing.png)
![Test Results](assets/cmd_status.png)

