"""
=========================================================
NeuroBridge AI
Explanation Agent
=========================================================
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.linear_model import LogisticRegression

try:
    import shap
except ImportError:
    shap = None


class ExplanationAgent:

    def __init__(
        self,
        model_path,
        background_path=None
    ):

        model_path = Path(model_path)
        if background_path is None:
            background_path = model_path.parent / "background.pkl"
        background_path = Path(background_path)

        self.pipeline = joblib.load(model_path)

        self.background = joblib.load(background_path)

        # Extract scaler and classifier
        if hasattr(self.pipeline, "named_steps"):

            self.scaler = self.pipeline.named_steps["scaler"]

            self.classifier = self.pipeline.named_steps["classifier"]

        else:

            self.scaler = None

            self.classifier = self.pipeline

        # Scale background data
        if self.scaler is not None:

            self.background_scaled = self.scaler.transform(
                self.background
            )

        else:

            self.background_scaled = self.background

    def explain(self, patient, save_path=None):

        try:
            patient_df = pd.DataFrame([patient])

            # Scale patient
            if self.scaler is not None:
                patient_scaled = self.scaler.transform(patient_df)
            else:
                patient_scaled = patient_df.values

            if shap is None:
                raise RuntimeError("SHAP is not installed in this environment.")

            # Create SHAP explainer
            explainer = shap.LinearExplainer(
                self.classifier,
                self.background_scaled
            )

            # Calculate SHAP values
            shap_values = explainer.shap_values(patient_scaled)

            # Convert to 1D array
            if hasattr(shap_values, "flatten"):
                shap_values = shap_values.flatten()

            # Separate positive and negative SHAP features
            top_positive = []
            top_negative = []

            for feat, val in zip(patient_df.columns, shap_values):
                val_float = float(val)
                item = {"feature": str(feat), "value": round(val_float, 4)}
                if val_float > 0:
                    top_positive.append(item)
                elif val_float < 0:
                    top_negative.append(item)

            top_positive = sorted(top_positive, key=lambda x: x["value"], reverse=True)
            top_negative = sorted(top_negative, key=lambda x: x["value"])

            # Feature Importance
            feature_importance = pd.DataFrame({
                "Feature": patient_df.columns,
                "SHAP Value": shap_values,
                "Importance": abs(shap_values)
            })

            feature_importance = feature_importance.sort_values(
                by="Importance",
                ascending=False
            )

            # Save chart if requested
            if save_path:

                save_path = Path(save_path)
                save_path.parent.mkdir(parents=True, exist_ok=True)

                plt.figure(figsize=(10, 6))

                plt.barh(
                    feature_importance["Feature"][:10],
                    feature_importance["Importance"][:10]
                )

                plt.gca().invert_yaxis()

                plt.xlabel("Importance")
                plt.title("Top SHAP Features")

                plt.tight_layout()

                plt.savefig(save_path)

                plt.close()

            return {
                "status": "success",
                "top_features": feature_importance.head(10).to_dict(orient="records"),
                "top_positive": top_positive[:5],
                "top_negative": top_negative[:5]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Explanation Not Available: {str(e)}",
                "top_features": [],
                "top_positive": [],
                "top_negative": []
            }
if __name__ == "__main__":

    patient = {
        "A1_Score": 1,
        "A2_Score": 1,
        "A3_Score": 0,
        "A4_Score": 1,
        "A5_Score": 0,
        "A6_Score": 1,
        "A7_Score": 0,
        "A8_Score": 1,
        "A9_Score": 0,
        "A10_Score": 1,
        "age": 6,
        "gender": 1,
        "ethnicity": 0,
        "jundice": 1,
        "austim": 0,
        "contry_of_res": 0,
        "used_app_before": 0,
        "result": 7,
        "age_desc": 0,
        "relation": 1
    }

    agent = ExplanationAgent(
        r"D:\Autism\backend\models\autism_model.pkl",
        r"D:\Autism\backend\models\background.pkl"
    )

    result = agent.explain(
        patient,
        r"D:\Autism\backend\reports\shap.png"
    )

    print(result)