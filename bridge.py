from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import intent, decompose, dispatch

app = FastAPI(title="7SS Modular Local Bridge", version="3.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach phase routers
app.include_router(intent.router)
app.include_router(decompose.router)
app.include_router(dispatch.router)

@app.get("/")
def health_check():
    return {"status": "online", "system": "7SS Modular Engine v3.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)