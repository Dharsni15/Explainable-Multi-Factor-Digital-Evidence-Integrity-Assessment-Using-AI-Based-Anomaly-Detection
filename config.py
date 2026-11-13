import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
UPLOADS_DIR = BASE_DIR / "uploads"
EVIDENCE_VAULT_DIR = UPLOADS_DIR / "vault"
VERIFICATION_DIR = UPLOADS_DIR / "verification"
REPORTS_DIR = BASE_DIR / "reports"
DATASET_DIR = BASE_DIR / "dataset"
SAVED_MODELS_DIR = BASE_DIR / "saved_models"

# Ensure runtime directories exist
for folder in [UPLOADS_DIR, EVIDENCE_VAULT_DIR, VERIFICATION_DIR, REPORTS_DIR, DATASET_DIR, SAVED_MODELS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_PATH = BASE_DIR / "forensics_evidence.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Security & JWT Configuration
SECRET_KEY = os.getenv("FORENSICS_SECRET_KEY", "academic_super_secure_forensics_xai_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

# Upload Limits & Allowed Formats
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {
    # Images
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff",
    # Documents
    ".pdf", ".docx", ".doc", ".txt", ".rtf", ".csv", ".json", ".log",
    # Audio / Video
    ".mp3", ".wav", ".aac", ".ogg", ".mp4", ".avi", ".mov", ".mkv"
}

# Operational Risk Thresholds
RISK_THRESHOLD_LOW_MAX = 30
RISK_THRESHOLD_MEDIUM_MAX = 60
# 61 - 100 = HIGH

# Academic & Legal Disclaimer
SYSTEM_DISCLAIMER = (
    "DISCLAIMER: This system is an academic research prototype designed for digital forensics decision-support "
    "and anomaly detection. It does NOT generate legally binding evidence admissibility certificates or establish guilt/innocence. "
    "All AI results indicate potential operational risk or anomalies and require qualified human forensic examiner review."
)
