from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import os
import asyncio
import json

app = FastAPI(title="Bifrost-Gate Gateway", version="0.1.0")

GUNGNIR_CORE_URL = os.getenv("GUNGNIR_CORE_URL", "http://localhost:8000")

@app.get("/")
async def root():
    return {"message": "Bifrost-Gate is standing watch. The Bridge is open."}

@app.post("/v1/query")
async def proxy_query(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{GUNGNIR_CORE_URL}/query", json=body)
        return response.json()

@app.get("/v1/stream")
async def stream_query(q: str):
    """SSE Streaming endpoint for real-time tokens."""
    async def event_generator():
        # Simulate streaming from Gungnir-Core
        tokens = ["Initializing...", "Accessing Mjolnir-Fabric...", "Analyzing...", "Result:", "The", "Spear", "is", "true."]
        for token in tokens:
            yield f"data: {json.dumps({'token': token})}\n\n"
            await asyncio.sleep(0.5)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
