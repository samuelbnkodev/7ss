from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama
from services.vision import vision_engine

router = APIRouter(prefix="/api", tags=["Phase 4 - Transformation"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/transform")
async def transformation_endpoint(req: AgentRequest):
    # 1. Capture local screen state and run OCR text extraction
    vision_data = vision_engine.extract_text_from_region()
    ocr_text = vision_data.get('extracted_text', '')
    
    # 2. Build system directive enriched with the actual OCR text read from the screen
    system_msg = (
        "You are the 7SS Structural Transformation Engine. Reshape and restructure input workflows "
        "into optimal execution formats. You have direct access to the user's active workstation screen via OCR. "
        "Here is the live text currently extracted from the user's screen:\n\n"
        f"--- SCREEN OCR DATA ---\n{ocr_text}\n-----------------------\n\n"
        "Analyze this screen content in relation to the user's prompt and provide a structured transformation report."
    )
    
    # 3. Query local Ollama model with full visual awareness
    response_text = await query_ollama(system_msg, req.prompt)
    
    return {
        "success": True, 
        "phase": "Green (Transformation)", 
        "response": response_text,
        "vision_context": vision_data
    }