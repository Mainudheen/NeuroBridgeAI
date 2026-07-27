"""
=========================================================
NeuroBridge AI

Gemini LLM Agent

Generates an AI-powered clinical explanation
=========================================================
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMAgent:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini client: {e}")

    ##################################################

    def generate(self, patient=None, prediction=None, recommendation=None, explanation=None, state=None):

        if state is not None and isinstance(state, dict):
            patient = patient or state.get("patient", {})
            prediction = prediction or state.get("prediction", {})
            explanation = explanation or state.get("explanation", {})
            recommendation = recommendation or state.get("recommendation", {})

        patient = patient or {}
        prediction = prediction or {}
        recommendation = recommendation or {}
        explanation = explanation or {}

        label = prediction.get("label", "N/A")
        confidence = prediction.get("confidence", "N/A")
        risk_level = recommendation.get("risk_level", "N/A")
        recs = recommendation.get("recommendations", [])

        if not self.client:
            return f"""Patient Summary:
Age: {patient.get('age', 'N/A')}, Gender: {'Male' if patient.get('gender') == 1 else 'Female'}

Prediction Result:
Prediction: {label} (Confidence: {confidence}%)

Clinical Interpretation:
The patient's screening responses were evaluated against the trained machine learning model. A risk level of {risk_level} was determined based on the clinical indicators provided.

Important Risk Factors:
Questionnaire indicators A1-A10 and clinical parameters suggest active monitoring is recommended.

Personalized Recommendations:
- {chr(10).join(recs) if recs else 'Consult a healthcare professional for further evaluation.'}

Disclaimer:
This summary is produced as a decision support tool and should not be used as a standalone medical diagnosis."""

        prompt = f"""
You are an experienced autism screening assistant and clinical decision support system.

Patient Information:
{patient}

Prediction Result:
{prediction}

Important Features (SHAP):
{explanation}

Recommendations:
{recommendation}

Write a structured clinical summary with the following exact headers:
1. Patient Summary
2. Clinical Interpretation
3. Risk Analysis
4. Recommendations
5. Disclaimer

Keep the tone professional, concise, and clinically relevant.
"""

        try:
            model_name = "gemini-2.0-flash"
            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            try:
                # Fallback model attempt
                response = self.client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )
                return response.text
            except Exception:
                return f"""Patient Summary:
Age: {patient.get('age', 'N/A')}, Gender: {'Male' if patient.get('gender') == 1 else 'Female'}

Prediction Result:
Prediction: {label} (Confidence: {confidence}%)

Clinical Interpretation:
The patient's screening data was processed by the NeuroBridge AI model. Based on the clinical features provided, the case presents a risk level of {risk_level}.

Important Risk Factors:
Questionnaire indicators (A1-A10) and demographic parameters were key factors in evaluating ASD likelihood.

Personalized Recommendations:
{chr(10).join(['- ' + r for r in recs]) if recs else '- Consult a qualified specialist.'}

Disclaimer:
This report is generated as an AI-assisted clinical decision support tool and does not replace formal medical diagnosis."""
if __name__ == "__main__":

    state = {

        "patient": {
            "age":22
        },

        "prediction":{
            "label":"Autism"
        },

        "explanation":{
            "top_features":[
                "A1_Score",
                "A3_Score"
            ]
        },

        "recommendation":{
            "risk_level":"High"
        }

    }

    agent = LLMAgent()

    print(agent.generate(state))