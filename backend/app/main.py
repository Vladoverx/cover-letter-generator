from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import models to ensure they are registered
from .models import User, CVProfile, CoverLetter
from .api import api_router
from .core.config import get_settings

# Get settings instance at startup
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A web application that generates personalized cover letters by analyzing user CVs and job descriptions",
    version="1.0.0",
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    return {"message": "CV Generator API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 