import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from backend.api.predict import router as predict_router
except ImportError:
    from api.predict import router as predict_router

app = FastAPI(
    title="NeuroBridge AI",
    version="1.0"
)
origins = [
    "http://localhost:5173",                 # Local React development
    "https://neuro-bridge-ai-three.vercel.app",  # Production frontend
]
# CORS Middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR)), name="reports")


@app.get("/")
def home():
    return {
        "project": "NeuroBridge AI",
        "status": "Running"
    }


@app.get("/download-report")
def download_report():
    pdf_file = REPORTS_DIR / "autism_report.pdf"
    if not pdf_file.exists():
        raise HTTPException(status_code=404, detail="Report not found. Please run a prediction first.")
    return FileResponse(
        path=str(pdf_file),
        filename="Autism_Report.pdf",
        media_type="application/pdf"
    )

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "NeuroBridgeAI Backend is Running 🚀"
    }