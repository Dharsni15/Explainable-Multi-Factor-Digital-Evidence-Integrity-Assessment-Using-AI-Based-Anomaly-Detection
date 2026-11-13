import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import engine, Base, ensure_database_schema
from backend.models import *  # Ensure all models are registered with Base
from backend.config import FRONTEND_DIR, REPORTS_DIR, UPLOADS_DIR
from backend.routes import (
    auth_router,
    evidence_router,
    custody_router,
    verification_router,
    analysis_router,
    reports_router,
    dashboard_router
)

# Initialize Database Schema
Base.metadata.create_all(bind=engine)
ensure_database_schema()

app = FastAPI(
    title="Explainable AI-Driven Digital Evidence Integrity Verification System",
    description=(
        "An integrated multi-factor forensic integrity assessment and anomaly detection framework "
        "correlating cryptographic hashing, metadata structure, timestamp logic, chain-of-custody continuity, "
        "and provenance lineage with Machine Learning and Explainable AI (SHAP)."
    ),
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router)
app.include_router(evidence_router)
app.include_router(custody_router)
app.include_router(verification_router)
app.include_router(analysis_router)
app.include_router(reports_router)
app.include_router(dashboard_router)

# Mount Static Folders
if REPORTS_DIR.exists():
    app.mount("/reports-vault", StaticFiles(directory=str(REPORTS_DIR)), name="reports")

if FRONTEND_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")

@app.get("/")
def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "AI-Driven Digital Evidence Integrity Verification API Running. Access /docs for Swagger UI."}

@app.get("/login")
def serve_login():
    login_path = FRONTEND_DIR / "login.html"
    if login_path.exists():
        return FileResponse(str(login_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "system": "Explainable AI Multi-Factor Digital Evidence Framework",
        "version": "1.0.0",
        "db_connected": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8005, reload=True)
