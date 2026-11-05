from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
pydantic_import_ok = True
try:
    from pydantic import BaseModel
except ImportError:
    pydantic_import_ok = False

import requests

app = FastAPI(title="7SS Local Bridge", version="1.1")

# Enable CORS so your web frontend can talk to localhost:8000 securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
# Automatically detect or default to your downloaded model tag
MODEL_NAME = "qwen3.5:4b" 

class PromptRequest(BaseModel if pydantic_import_ok else object):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "online", "system": "7SS Local Bridge Active", "model": MODEL_NAME}

@app.post("/api/agent")
def run_agent_prompt(req: PromptRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": req.prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048,      # Strict context window cap to prevent memory bloat/freezing
            "temperature": 0.3    # Lower temperature for reliable, structured output
        }
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
        
        result = response.json()
        return {
            "success": True,
            "response": result.get("response", "No response generated.")
        }
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Local model timed out. Try a shorter prompt.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)