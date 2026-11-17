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
    ocr_text = vision_data.get('extracted_text', 'No text extracted')
    
    # 2. Build system directive explicitly embedding the OCR content
    system_msg = (
        "You are the 7SS Structural Transformation Engine. Reshape and restructure input workflows "
        "into optimal execution formats. You have direct access to the user's active workstation screen via OCR. "
        "Here is the raw text currently extracted from the user's screen:\n\n"
        f"--- START SCREEN OCR ---\n{ocr_text}\n--- END SCREEN OCR ---\n\n"
        "Analyze the above screen OCR data to answer the user's prompt and formulate your transformation report."
    )
    
    # 3. Query local Ollama model
    response_text = await query_ollama(system_msg, req.prompt)
    
    return {
        "success": True, 
        "phase": "Green (Transformation)", 
        "response": response_text,
        "vision_context": vision_data
    }