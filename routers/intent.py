from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 1 - Intent"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/intent")
async def intent_hub_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Intent & State Hub. Analyze incoming input and categorize core domain, priority, and objective."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Red (Intent)", "response": response_text}