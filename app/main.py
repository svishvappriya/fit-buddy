import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app.routes import router

# Resolve base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Ensure required static and template directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager to create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Full-stack AI Fitness Planner powered by Google Gemini 1.5 Pro and Gemini Flash",
    version="1.0.0",
    lifespan=lifespan,
)


@app.on_event("startup")
def startup_event():
    """Startup event ensuring all SQLite tables exist."""
    Base.metadata.create_all(bind=engine)


# Mount static assets directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Configure Jinja2 templates directory
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Register route handlers
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
