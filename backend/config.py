from pathlib import Path

# Backend folder
BASE_DIR = Path(__file__).resolve().parent

# Project folder
PROJECT_DIR = BASE_DIR.parent

# Dataset Folder
DATASET_DIR = PROJECT_DIR / "datasets"

QUESTIONNAIRE_DATASET = DATASET_DIR / "questionaire"

# Model Folder
MODEL_DIR = BASE_DIR / "models"

# Reports
REPORT_DIR = BASE_DIR / "reports"

# Uploads
UPLOAD_DIR = BASE_DIR / "uploads"

# Create folders automatically
MODEL_DIR.mkdir(exist_ok=True)

REPORT_DIR.mkdir(exist_ok=True)

UPLOAD_DIR.mkdir(exist_ok=True)