from fastapi import APIRouter, Request
from typing import Dict, Any
import json
import os

router = APIRouter(prefix="/api", tags=["Phase 7 - Dispatch"])

@router.post("/dispatch")
async def dispatch_endpoint(request: Request):
    body = await request.json()
    
    # Handle both wrapped {"package": {...}} and raw dictionary payloads
    audit_entry = body.get("package", body)
    
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/execution_audit.json"
    
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