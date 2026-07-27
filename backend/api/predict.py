import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

try:
    from backend.graph.workflow import graph
except ImportError:
    from graph.workflow import graph

router = APIRouter()


class PredictionInput(BaseModel):

    A1_Score: int
    A2_Score: int
    A3_Score: int
    A4_Score: int
    A5_Score: int
    A6_Score: int
    A7_Score: int
    A8_Score: int
    A9_Score: int
    A10_Score: int

    age: int
    gender: int
    ethnicity: int

    jundice: int
    austim: int
    contry_of_res: int

    used_app_before: int

    age_desc: int

    relation: int


@router.post("/predict")
def predict(data: PredictionInput):

    try:

        state = {

            "patient": data.model_dump(),

            "validation": {},

            "prediction": {},

            "explanation": {},

            "recommendation": {},

            "llm_report": "",

            "pdf_path": ""

        }

        result = graph.invoke(state)

        if not result.get("validation", {}).get("valid", True):
            return {
                "status": "error",
                "validation": result.get("validation", {}),
                "prediction": {},
                "explanation": {},
                "recommendation": {},
                "llm_report": "",
                "pdf_path": ""
            }

        return {

            "status": "success",

            "validation": result["validation"],

            "prediction": result["prediction"],

            "explanation": result["explanation"],

            "recommendation": result["recommendation"],

            "llm_report": result["llm_report"],

            "pdf_path": result["pdf_path"]

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )