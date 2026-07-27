"""
=========================================================
NeuroBridge AI
Evaluation Module
=========================================================
"""

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    PrecisionRecallDisplay
)


class ModelEvaluator:

    def __init__(self, model_path):

        self.model = joblib.load(model_path)

    #######################################################
    # Classification Report
    #######################################################

    def classification_report(self, X_test, y_test):

        prediction = self.model.predict(X_test)

        report = classification_report(
            y_test,
            prediction,
            output_dict=True
        )

        report_df = pd.DataFrame(report).transpose()

        print("\nClassification Report\n")
        print(report_df)

        return report_df

    #######################################################
    # Confusion Matrix
    #######################################################

    def confusion_matrix_plot(
        self,
        X_test,
        y_test,
        save_path
    ):

        prediction = self.model.predict(X_test)

        cm = confusion_matrix(
            y_test,
            prediction
        )

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm
        )

        disp.plot()

        plt.title("Confusion Matrix")

        save_path = Path(save_path)

        save_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        plt.savefig(save_path)

        plt.close()

        print(f"\nConfusion Matrix saved to:\n{save_path}")

    #######################################################
    # ROC Curve
    #######################################################

    def roc_curve_plot(
        self,
        X_test,
        y_test,
        save_path
    ):

        if not hasattr(self.model, "predict_proba"):

            print("Model does not support predict_proba()")
            return

        probability = self.model.predict_proba(X_test)[:, 1]

        fpr, tpr, _ = roc_curve(
            y_test,
            probability
        )

        auc = roc_auc_score(
            y_test,
            probability
        )

        plt.figure(figsize=(6,6))

        plt.plot(
            fpr,
            tpr,
            label=f"AUC = {auc:.3f}"
        )

        plt.plot(
            [0,1],
            [0,1],
            linestyle="--"
        )

        plt.xlabel("False Positive Rate")

        plt.ylabel("True Positive Rate")

        plt.title("ROC Curve")

        plt.legend()

        save_path = Path(save_path)

        save_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        plt.savefig(save_path)

        plt.close()

        print(f"\nROC Curve saved to:\n{save_path}")
        #######################################################
    # Precision Recall Curve
    #######################################################

    def precision_recall_plot(
        self,
        X_test,
        y_test,
        save_path
    ):

        if not hasattr(self.model, "predict_proba"):

            print("Model does not support predict_proba()")
            return

        probability = self.model.predict_proba(X_test)[:, 1]

        precision, recall, _ = precision_recall_curve(
            y_test,
            probability
        )

        display = PrecisionRecallDisplay(
            precision=precision,
            recall=recall
        )

        display.plot()

        plt.title("Precision Recall Curve")

        save_path = Path(save_path)

        save_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        plt.savefig(save_path)

        plt.close()

        print(f"\nPrecision Recall Curve saved to:\n{save_path}")

    #######################################################
    # Feature Importance
    #######################################################

    def feature_importance(
        self,
        feature_names,
        save_path
    ):

        model = self.model

        # If model is Pipeline (Logistic Regression/SVM)
        if hasattr(model, "named_steps"):
            model = model.named_steps.get("classifier", model)

        if not hasattr(model, "feature_importances_"):

            print("\nFeature Importance not available for this model.")
            return

        importance = model.feature_importances_

        importance_df = pd.DataFrame({

            "Feature": feature_names,
            "Importance": importance

        })

        importance_df = importance_df.sort_values(
            by="Importance",
            ascending=False
        )

        plt.figure(figsize=(10,6))

        plt.barh(
            importance_df["Feature"],
            importance_df["Importance"]
        )

        plt.gca().invert_yaxis()

        plt.title("Feature Importance")

        save_path = Path(save_path)

        save_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        plt.savefig(save_path)

        plt.close()

        print(f"\nFeature Importance saved to:\n{save_path}")

        return importance_df

    #######################################################
    # Evaluate Complete Model
    #######################################################

    def evaluate(
        self,
        X_test,
        y_test,
        feature_names,
        output_folder
    ):

        output_folder = Path(output_folder)

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.classification_report(
            X_test,
            y_test
        )

        self.confusion_matrix_plot(
            X_test,
            y_test,
            output_folder / "confusion_matrix.png"
        )

        self.roc_curve_plot(
            X_test,
            y_test,
            output_folder / "roc_curve.png"
        )

        self.precision_recall_plot(
            X_test,
            y_test,
            output_folder / "precision_recall_curve.png"
        )

        self.feature_importance(
            feature_names,
            output_folder / "feature_importance.png"
        )

        print("\nEvaluation Completed Successfully")