from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 7 - Dispatcher"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/dispatch")
async def dispatch_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Omni-Destination Dispatcher. Summarize final execution payload and confirm dispatch readiness."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Violet (Dispatcher)", "response": response_text}