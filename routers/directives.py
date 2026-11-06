from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix=" /api", tags=["Phase 5 - Directives"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/directives")
async def directives_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Action Directives Engine. Formulate strict, actionable step-by-step commands and parameters."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Blue (Directives)", "response": response_text}