from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama
from services.vision import vision_engine

router = APIRouter(prefix="/api", tags=["Phase 5 - Directives"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/directives")
async def directives_endpoint(req: AgentRequest):
    system_msg = (
        "You are the 7SS Action Directives Engine. Formulate strict, actionable step-by-step commands. "
        "If you need to click a button on screen, include a command in your response formatted as: [CLICK: ButtonName]"
    )
    
    response_text = await query_ollama(system_msg, req.prompt)
    
    # Example automation trigger: scan response for a click command
    action_result = None
    if "[CLICK:" in response_text:
        # Extract target text between [CLICK: and ]
        start = response_text.find("[CLICK:") + 7
        end = response_text.find("]", start)
        target = response_text[start:end].strip()
        
        # Execute vision-guided click
        action_result = vision_engine.execute_click_on_text(target)

    return {
        "success": True, 
        "phase": "Blue (Directives)", 
        "response": response_text,
        "action_execution": action_result
    }