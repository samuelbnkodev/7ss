import httpx
from fastapi import HTTPException
from config import OLLAMA_URL, MODEL_NAME, TIMEOUT_SECONDS

async def query_ollama(system_prompt: str, user_prompt: str) -> str:
    """Central helper to handle all local LLM interaction."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        try:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "").strip()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Local Ollama connection error: {exc}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Bridge processing error: {exc}")