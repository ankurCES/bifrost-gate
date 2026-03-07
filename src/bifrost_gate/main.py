from fastapi import FastAPI, Request
import httpx
import os

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
