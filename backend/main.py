from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.jobs.routes import router as jobs_router
from app.optimization.routes import router as optimization_router
from app.resume.routes import router as resume_router

app = FastAPI(
    title="Arete API",
    description="AI-powered resume optimizer for tech professionals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(optimization_router)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Arete API - AI Resume Optimizer", "version": "1.0.0"}

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "app": settings.app_name}
