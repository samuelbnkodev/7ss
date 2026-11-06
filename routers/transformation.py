from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama

router = APIRouter(prefix="/api", tags=["Phase 4 - Transformation"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/transform")
async def transformation_endpoint(req: AgentRequest):
    system_msg = "You are the 7SS Structural Transformation Engine. Reshape and restructure input workflows into optimal execution formats."
    response_text = await query_ollama(system_msg, req.prompt)
    return {"success": True, "phase": "Green (Transformation)", "response": response_text}