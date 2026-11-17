from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama
from services.vision import vision_engine
import time
import re
import pyautogui

router = APIRouter(prefix="/api", tags=["Phase 5 - Directives"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/directives")
async def directives_endpoint(req: AgentRequest):
    system_msg = (
        "You are the 7SS Action Directives Engine. Formulate strict, actionable commands. "
        "You MUST include at least one executable tag in your response to fulfill automation requests. "
        "Use ONLY these exact tag formats:\n"
        "- [WAIT: seconds] (e.g., [WAIT: 1])\n"
        "- [KEY: keyname] (e.g., [KEY: enter])\n"
        "- [CLICK: TargetText] (e.g., [CLICK: Dashboard])\n"
        "Do not invent other tag names."
    )
    
    response_text = await query_ollama(system_msg, req.prompt)
    
    # Parse and Execute Action Directives
    executed_actions = []
    pattern = r'\[(CLICK|KEY|WAIT):\s*([^\]]+)\]'
    commands = re.findall(pattern, response_text)
    
    for cmd_type, value in commands:
        value = value.strip()
        action_log = {"command": cmd_type, "target": value, "success": False}
        
        try:
            if cmd_type == "CLICK":
                result = vision_engine.execute_click_on_text(value)
                action_log.update(result)
            elif cmd_type == "KEY":
                pyautogui.press(value.lower())
                action_log.update({"success": True, "details": f"Pressed key: {value}"})
            elif cmd_type == "WAIT":
                secs = float(value)
                time.sleep(secs)
                action_log.update({"success": True, "details": f"Waited {secs} seconds"})
        except Exception as e:
            action_log.update({"success": False, "error": str(e)})
            
        executed_actions.append(action_log)

    return {
        "success": True, 
        "phase": "Blue (Directives)", 
        "response": response_text,
        "executed_actions": executed_actions
    }