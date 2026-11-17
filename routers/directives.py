import time
import re
import pyautogui
from fastapi import APIRouter
from pydantic import BaseModel
from services.ollama import query_ollama
from services.vision import vision_engine

router = APIRouter(prefix="/api", tags=["Phase 5 - Directives"])

class AgentRequest(BaseModel):
    prompt: str

@router.post("/directives")
async def directives_endpoint(req: AgentRequest):
    # 1. Instruct the local LLM to output structured execution tags alongside its rationale
    system_msg = (
        "You are the 7SS Action Directives Engine. Formulate strict, actionable step-by-step commands. "
        "You can control the user's workstation by including specific execution tags in your response:\n"
        "- Click an element: [CLICK: ExactTextOrButton]\n"
        "- Press a keyboard key: [KEY: enter], [KEY: tab], [KEY: space]\n"
        "- Pause execution: [WAIT: 1]\n"
        "Include these tags naturally when workflow automation is required."
    )
    
    # 2. Query local Ollama model
    response_text = await query_ollama(system_msg, req.prompt)
    
    # 3. Parse and Execute Action Directives
    executed_actions = []
    
    # Extract all command tags in order of appearance
    # Matches patterns like [CLICK: Target], [KEY: enter], [WAIT: 2]
    pattern = r'\[(CLICK|KEY|WAIT):\s*([^\]]+)\]'
    commands = re.findall(pattern, response_text)
    
    for cmd_type, value in commands:
        value = value.strip()
        action_log = {"command": cmd_type, "target": value, "success": False}
        
        try:
            if cmd_type == "CLICK":
                # Execute vision-guided click via our vision engine
                result = vision_engine.execute_click_on_text(value)
                action_log.update(result)
                
            elif cmd_type == "KEY":
                # Execute keyboard shortcut/key press
                pyautogui.press(value.lower())
                action_log.update({"success": True, "details": f"Pressed key: {value}"})
                
            elif cmd_type == "WAIT":
                # Pause for specified seconds
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