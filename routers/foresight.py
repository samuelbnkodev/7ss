from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 3 - Foresight"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/foresight")
async def foresight_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Foresight & Constraints Engine. Analyze potential bottlenecks, risks, and hidden dependencies."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Yellow (Foresight)", "response": response_text}