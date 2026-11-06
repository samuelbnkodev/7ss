from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 2 - Decomposer"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/decompose")
async def decompose_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Segment & Sequence Decomposer. Break inputs into Segment A, Segment B, and Key Milestones."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Orange (Decomposer)", "response": response_text}