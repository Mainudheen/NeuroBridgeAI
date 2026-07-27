"""
=========================================================
NeuroBridge AI

Shared State

Every LangGraph node reads and updates this state.
=========================================================
"""

from typing import TypedDict


class AutismState(TypedDict):

    patient: dict

    validation: dict

    prediction: dict

    explanation: dict

    recommendation: dict

    llm_report: str

    pdf_path: str