"""
=========================================================
NeuroBridge AI

Orchestrator Agent

Coordinates all AI Agents

=========================================================
"""

from agents.validation_agent import ValidationAgent
from agents.prediction_agent import PredictionAgent
from agents.explanation_agent import ExplanationAgent
from agents.recommendation_agent import RecommendationAgent
from agents.report_agent import ReportAgent

class OrchestratorAgent:

    def __init__(self):

        self.validator = ValidationAgent()

        self.predictor = PredictionAgent(
            r"D:\AUTISM\backend\models\autism_model.pkl"
        )

        self.explainer = ExplanationAgent(
            r"D:\AUTISM\backend\models\autism_model.pkl"
        )

        self.recommender = RecommendationAgent()
        self.reporter = ReportAgent()
    ######################################################

    def process(self, patient):

        ##################################################
        # Validation
        ##################################################

        validation = self.validator.validate(patient)

        if not validation["valid"]:

            return {

                "status": "Validation Failed",

                "validation": validation

            }

        ##################################################
        # Prediction
        ##################################################

        prediction = self.predictor.predict(patient)

        ##################################################
        # Explanation
        ##################################################

        explanation = self.explainer.explain(patient)

        ##################################################
        # Recommendation
        ##################################################

        recommendation = self.recommender.recommend(
            prediction
        )
        report = self.reporter.generate(

            patient,

            prediction,

            explanation,

            recommendation,

             r"D:\AUTISM\backend\reports\patient_report.pdf"

        )
        ##################################################

        return {

            "status": "Success",

            "prediction": prediction,

            "explanation": explanation,

            "recommendation": recommendation,
            "report":report
        }


############################################################

if __name__ == "__main__":

    patient = {

        "A1_Score":1,
        "A2_Score":0,
        "A3_Score":1,
        "A4_Score":1,
        "A5_Score":0,
        "A6_Score":1,
        "A7_Score":1,
        "A8_Score":0,
        "A9_Score":1,
        "A10_Score":0,

        "age":22,

        "gender":1,

        "ethnicity":3,

        "jundice":0,

        "austim":0,

        "contry_of_res":12,

        "used_app_before":1,

        "age_desc":0,

        "relation":5

    }

    agent = OrchestratorAgent()

    result = agent.process(patient)

    from pprint import pprint

    pprint(result)