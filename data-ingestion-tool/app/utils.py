import asyncio
from typing import Dict

async def fetch_external_api(id: int) -> Dict:
    # Simulate network delay, e.g., 1 second
    await asyncio.sleep(1)
    return {"id": id, "data": "processed"}

