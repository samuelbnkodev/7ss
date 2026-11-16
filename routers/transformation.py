from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama
from services.vision import vision_engine

router = APIRouter(prefix="/api", tags=["Phase 4 - Transformation"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/transform")
async def transformation_endpoint(req: AgentRequest):
    # 1. Capture local screen state / vision context for environmental transformation
    vision_data = vision_engine.extract_text_from_region()
    
    # 2. Build system directive enriched with local CV metrics
    system_msg = (
        "You are the 7SS Structural Transformation Engine. Reshape and restructure input workflows "
        "into optimal execution formats. Integrate active workstation visual context: "
        f"Resolution {vision_data.get('resolution', 'N/A')}."
    )
    
    # 3. Query local Ollama model
    response_text = await query_ollama(system_msg, req.prompt)
    
    return {
        "success": True, 
        "phase": "Green (Transformation)", 
        "response": response_text,
        "vision_context": vision_data
    }