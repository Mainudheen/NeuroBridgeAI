"""
=========================================================
NeuroBridge AI

LangGraph Workflow

=========================================================
"""

from langgraph.graph import StateGraph, END

from backend.graph.state import AutismState

from backend.agents.validation_agent import ValidationAgent
from backend.agents.prediction_agent import PredictionAgent
from backend.agents.explanation_agent import ExplanationAgent
from backend.agents.recommendation_agent import RecommendationAgent
from backend.agents.llm_agent import LLMAgent
from backend.agents.report_agent import ReportAgent


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "autism_model.pkl"
BACKGROUND_PATH = BASE_DIR / "models" / "background.pkl"
REPORT_PATH = BASE_DIR / "reports" / "autism_report.pdf"

#########################################################
# Initialize Agents
#########################################################

validator = ValidationAgent()

predictor = PredictionAgent(MODEL_PATH)

explainer = ExplanationAgent(MODEL_PATH, BACKGROUND_PATH)

recommender = RecommendationAgent()

llm = LLMAgent()

report = ReportAgent()


#########################################################
# Validation Node
#########################################################

def validation_node(state: AutismState):

    state["validation"] = validator.validate(
        state["patient"]
    )

    return state


#########################################################
# Validation Router
#########################################################

def validation_router(state: AutismState):

    if state["validation"]["valid"]:
        return "Prediction"

    return "END"


#########################################################
# Prediction Node
#########################################################

def prediction_node(state: AutismState):

    state["prediction"] = predictor.predict(
        state["patient"]
    )

    return state


#########################################################
# Explanation Node
#########################################################

def explanation_node(state: AutismState):

    state["explanation"] = explainer.explain(
        state["patient"]
    )

    return state


#########################################################
# Recommendation Node
#########################################################

def recommendation_node(state: AutismState):

    state["recommendation"] = recommender.recommend(
        state["prediction"]
    )

    return state


#########################################################
# LLM Node
#########################################################

def llm_node(state: AutismState):

    state["llm_report"] = llm.generate(
        state["patient"],
        state["prediction"],
        state["recommendation"]
    )

    return state


#########################################################
# Report Node
#########################################################

def report_node(state: AutismState):

    result = report.generate(

        patient=state["patient"],

        prediction=state["prediction"],

        explanation=state["explanation"],

        recommendation=state["recommendation"],

        llm_report=state["llm_report"],

        output_file=str(REPORT_PATH)

    )

    state["pdf_path"] = result["pdf_path"]

    return state


#########################################################
# Build Workflow
#########################################################

workflow = StateGraph(AutismState)

workflow.add_node(
    "Validation",
    validation_node
)

workflow.add_node(
    "Prediction",
    prediction_node
)

workflow.add_node(
    "Explanation",
    explanation_node
)

workflow.add_node(
    "Recommendation",
    recommendation_node
)

workflow.add_node(
    "LLM",
    llm_node
)

workflow.add_node(
    "Report",
    report_node
)

workflow.set_entry_point("Validation")

workflow.add_conditional_edges(

    "Validation",

    validation_router,

    {
        "Prediction": "Prediction",
        "END": END
    }

)

workflow.add_edge(
    "Prediction",
    "Explanation"
)

workflow.add_edge(
    "Explanation",
    "Recommendation"
)

workflow.add_edge(
    "Recommendation",
    "LLM"
)

workflow.add_edge(
    "LLM",
    "Report"
)

workflow.add_edge(
    "Report",
    END
)

graph = workflow.compile()


#########################################################
# Testing
#########################################################

if __name__ == "__main__":

    state = {

        "patient": {

            "A1_Score": 1,
            "A2_Score": 0,
            "A3_Score": 1,
            "A4_Score": 1,
            "A5_Score": 0,
            "A6_Score": 1,
            "A7_Score": 1,
            "A8_Score": 0,
            "A9_Score": 1,
            "A10_Score": 0,

            "age": 22,

            "gender": 1,

            "ethnicity": 3,

            "jundice": 0,

            "austim": 0,

            "contry_of_res": 12,

            "used_app_before": 1,

            "age_desc": 0,

            "relation": 5

        },

        "validation": {},

        "prediction": {},

        "explanation": {},

        "recommendation": {},

        "llm_report": "",

        "pdf_path": ""

    }

    result = graph.invoke(state)

    from pprint import pprint

    pprint(result)