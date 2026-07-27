"""
=========================================================
NeuroBridge AI
Model Factory
=========================================================

This module contains all machine learning models used in
the autism prediction system.

Author : NeuroBridge AI
"""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


class ModelFactory:

    @staticmethod
    def get_models():
        """
        Returns all machine learning models.
        """

        models = {

            "Logistic Regression": Pipeline([
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(
                    max_iter=1000,
                    random_state=42
                ))
            ]),

            "Decision Tree": DecisionTreeClassifier(
                random_state=42
            ),

            "Random Forest": RandomForestClassifier(
                n_estimators=300,
                random_state=42
            ),

            "SVM": Pipeline([
                ("scaler", StandardScaler()),
                ("classifier", SVC(
                    probability=True,
                    random_state=42
                ))
            ]),

            "XGBoost": XGBClassifier(
                eval_metric="logloss",
                random_state=42
            ),

            "LightGBM": LGBMClassifier(
                random_state=42
            ),

            "CatBoost": CatBoostClassifier(
                verbose=0,
                random_state=42
            )
        }

        return models


if __name__ == "__main__":

    models = ModelFactory.get_models()

    print("=" * 60)
    print("AVAILABLE MODELS")
    print("=" * 60)

    for name in models:
        print(name)