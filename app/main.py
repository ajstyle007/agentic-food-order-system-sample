from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.order import router as order_router


app = FastAPI(
    title="Agentic Food Ordering API",
    description="Multi-Agent AI Powered Food Ordering System",
    version="1.0"
)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_router)

@app.get("/")
async def root():
    return {
        "message": "🤖 Agentic Food Ordering API is Running Successfully!",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Agentic Food AI"}

