# bridge.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import intent, decompose, foresight, transformation, directives, assembly, dispatch

app = FastAPI(title="7SS Full Rainbow Modular Engine", version="3.5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all 7 rainbow phase routers
app.include_router(intent.router)         # Phase 1: Red
app.include_router(decompose.router)      # Phase 2: Orange
app.include_router(foresight.router)      # Phase 3: Yellow
app.include_router(transformation.router) # Phase 4: Green
app.include_router(directives.router)     # Phase 5: Blue
app.include_router(assembly.router)       # Phase 6: Indigo
app.include_router(dispatch.router)       # Phase 7: Violet

@app.get("/")
def health_check():
    return {"status": "online", "system": "7SS Full Rainbow Engine v3.5"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)