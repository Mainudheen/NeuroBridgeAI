"""
=========================================================
NeuroBridge AI

Prediction Agent

Loads trained ML model and predicts
Autism Spectrum Disorder (ASD).

Author : NeuroBridge AI
=========================================================
"""

import joblib
import pandas as pd
from pathlib import Path


class PredictionAgent:

    def __init__(self, model_path):

        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        self.model = joblib.load(model_path)

    ########################################################

    def predict(self, patient):

        patient_df = pd.DataFrame([patient])

        prediction = self.model.predict(patient_df)[0]

        probability = None

        if hasattr(self.model, "predict_proba"):

            probability = float(
                self.model.predict_proba(patient_df)[0][1]
            )

        elif hasattr(self.model, "decision_function"):

            score = float(
                self.model.decision_function(patient_df)[0]
            )

            probability = round(score, 4)

        result = {

            "prediction": int(prediction),

            "label":
                "Autism Detected"
                if prediction == 1
                else "No Autism",

            "confidence":
                round(probability * 100, 2)
                if probability is not None
                else None

        }

        return result


############################################################

if __name__ == "__main__":

    patient = {

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

    "jundice": 0,          # ✅ spelling matches training data

    "austim": 0,           # ✅ spelling matches training data

    "contry_of_res": 12,   # ✅ spelling matches training data

    "used_app_before": 1,

    "age_desc": 0,         # ✅ required column

    "relation": 5
}
    agent = PredictionAgent(
        r"D:\AUTISM\backend\models\autism_model.pkl"
    )

    result = agent.predict(patient)

    print("\nPrediction Result")
    print("=================")
    print(result)