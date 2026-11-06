from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="7SS Local Bridge & Agent Orchestrator", version="3.0")

# Enable CORS for local and web UI preview access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production preview
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3.5:4b"
TIMEOUT_SECONDS = 120.0  # Extended timeout for 4B local model stability

class AgentRequest(BaseModel):
    prompt: str

async def query_ollama(system_prompt: str, user_prompt: str) -> str:
    """Helper function to communicate with local Ollama runtime."""
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

@app.get("/")
def health_check():
    return {"status": "online", "system": "7SS Local Bridge", "model": MODEL_NAME}

@app.post("/api/agent")
async def general_agent_endpoint(req: AgentRequest):
    """General agent endpoint for open text execution."""
    system_msg = "You are the 7SS local organizing intelligence. Keep responses clear, structured, and focused on organization."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "response": response_text}

@app.post("/api/intent")
async def intent_hub_endpoint(req: AgentRequest):
    """Phase 1 (Red): Ingests raw inputs and categorizes organizational intent."""
    system_msg = "You are the 7SS Intent & State Hub. Analyze the incoming user input and categorize its core domain, priority, and objective in a concise format."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Red (Intent)", "response": response_text}

@app.post("/api/decompose")
async def decompose_endpoint(req: AgentRequest):
    """Phase 2 (Orange): Breaks unstructured notes into structured segments and sequences."""
    system_msg = "You are the 7SS Segment & Sequence Decomposer. Take the input and break it down into clean structural components: Segment A, Segment B, and Key Milestones."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Orange (Decomposer)", "response": response_text}

@app.post("/api/dispatch")
async def dispatch_endpoint(req: AgentRequest):
    """Phase 7 (Violet): Formulates final execution payloads and dispatch confirmations."""
    system_msg = "You are the 7SS Omni-Destination Dispatcher. Summarize the final execution package and confirm readiness for local action dispatch."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Violet (Dispatcher)", "response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)