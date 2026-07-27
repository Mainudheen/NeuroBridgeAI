from fastapi import APIRouter

from backend.graph.workflow import graph
from backend.api.schemas import PatientData

router = APIRouter()


@router.post("/analyze")
def analyze(patient: PatientData):

    state = {

        "patient": patient.model_dump(),

        "validation": {},

        "prediction": {},

        "recommendation": {},

        "llm_report": "",

        "pdf_path": ""

    }

    result = graph.invoke(state)

    return {

        "prediction": result["prediction"],

        "recommendation": result["recommendation"],

        "llm_report": result["llm_report"],

        "pdf_path": result["pdf_path"]

    }