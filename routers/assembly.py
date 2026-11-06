from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 6 - Assembly"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/assemble")
async def assembly_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Synthesis & Assembly Engine. Consolidate all preceding phase outputs into a unified package."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Indigo (Assembly)", "response": response_text}