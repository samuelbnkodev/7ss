from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
import json
import os

router = APIRouter(prefix="/api", tags=["Phase 7 - Dispatch"])

class DispatchRequest(BaseModel):
    package: Dict[str, Any]

@router.post("/dispatch")
async def dispatch_endpoint(req: DispatchRequest):
    # Ensure local logs directory exists
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/execution_audit.json"
    
    audit_entry = req.package
    dispatch_success = True
    
    try:
        logs = []
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                logs = json.load(f)
        logs.append(audit_entry)
        with open(log_path, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        dispatch_success = False
        
    return {
        "success": dispatch_success,
        "phase": "Violet (Dispatch)",
        "dispatch_destination": "Local Audit Log & Frontend UI Stream",
        "audit_path": log_path,
        "dispatched_package": audit_entry
    }