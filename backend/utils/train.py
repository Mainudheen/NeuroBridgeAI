"""
=========================================================
NeuroBridge AI
Training Module
=========================================================

Loads dataset
Splits train/test
Trains all models
Selects the best model

Author : NeuroBridge AI
"""

import joblib
import pandas as pd

from pathlib import Path

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from utils.model_factory import ModelFactory


class AutismTrainer:

    def __init__(self):

        self.dataset = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.models = ModelFactory.get_models()

        self.results = []

        self.best_model = None
        self.best_model_name = None
        self.best_recall = -1

    #######################################################
    # Load Dataset
    #######################################################

    def load_dataset(self, csv_path):

        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found : {csv_path}"
            )

        self.dataset = pd.read_csv(csv_path)

        print("=" * 60)
        print("Dataset Loaded Successfully")
        print("=" * 60)

        print(self.dataset.head())

        return self.dataset

    #######################################################
    # Split Dataset
    #######################################################

    def split_dataset(self):

        X = self.dataset.drop("Class/ASD", axis=1)

        y = self.dataset["Class/ASD"]

        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test
        ) = train_test_split(

            X,
            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

        print()

        print("Training Samples :", len(self.X_train))
        print("Testing Samples  :", len(self.X_test))

    #######################################################
    # Train Models
    #######################################################

    def train_models(self):

        print()
        print("=" * 60)
        print("Training Models")
        print("=" * 60)

        for name, model in self.models.items():

            print(f"\n{name}")

            model.fit(
                self.X_train,
                self.y_train
            )

            prediction = model.predict(
                self.X_test
            )

            accuracy = accuracy_score(
                self.y_test,
                prediction
            )

            precision = precision_score(
                self.y_test,
                prediction
            )

            recall = recall_score(
                self.y_test,
                prediction
            )

            f1 = f1_score(
                self.y_test,
                prediction
            )

            if hasattr(model, "predict_proba"):

                probability = model.predict_proba(
                    self.X_test
                )[:, 1]

                roc_auc = roc_auc_score(
                    self.y_test,
                    probability
                )

            else:

                roc_auc = 0

            cv = cross_val_score(

                model,

                self.X_train,

                self.y_train,

                cv=5,

                scoring="accuracy"

            ).mean()

            self.results.append({

                "Model": name,

                "Accuracy": accuracy,

                "Precision": precision,

                "Recall": recall,

                "F1 Score": f1,

                "ROC AUC": roc_auc,

                "Cross Validation": cv

            })

            print(f"Accuracy  : {accuracy:.4f}")
            print(f"Precision : {precision:.4f}")
            print(f"Recall    : {recall:.4f}")
            print(f"F1 Score  : {f1:.4f}")
            print(f"ROC AUC   : {roc_auc:.4f}")
            print(f"CV Score  : {cv:.4f}")

            if recall > self.best_recall:

                self.best_recall = recall

                self.best_model = model

                self.best_model_name = name

        print()

        print("=" * 60)
        print("Best Model")
        print("=" * 60)

        print(self.best_model_name)
        print(f"Recall : {self.best_recall:.4f}")
        #######################################################
    # Save Best Model
    #######################################################

    #######################################################
# Save Best Model
#######################################################

    def save_model(self, model_path):

        if self.best_model is None:
            raise ValueError("No trained model available.")

        model_path = Path(model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

    # Save trained model
        joblib.dump(self.best_model, model_path)

    # Save background dataset for SHAP
        background_path = model_path.parent / "background.pkl"

        background_data = self.X_train.sample(
            min(100, len(self.X_train)),
            random_state=42
        )

        joblib.dump(background_data, background_path)

        print()
        print("=" * 60)
        print("Model Saved Successfully")
        print("=" * 60)
        print(model_path)

        print()
        print("=" * 60)
        print("Background Dataset Saved Successfully")
        print("=" * 60)
        print(background_path)

    #######################################################
    # Save Results
    #######################################################

    def save_results(self, csv_path):

        csv_path = Path(csv_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        results_df = pd.DataFrame(self.results)

        results_df = results_df.sort_values(
            by="Recall",
            ascending=False
        )

        results_df.to_csv(
            csv_path,
            index=False
        )
        from utils.plots import PlotManager

        report_folder = csv_path.parent

        PlotManager.model_comparison(
            results_df,
            report_folder / "model_comparison.png"
        )

        PlotManager.metrics(
            results_df,
            report_folder / "metrics_comparison.png"
        )

        PlotManager.cross_validation(
            results_df,
            report_folder / "cross_validation.png"
        )

        print()
        print("=" * 60)
        print("Results Saved Successfully")
        print("=" * 60)
        print(csv_path)

    #######################################################
    # Display Results
    #######################################################

    def show_results(self):

        if len(self.results) == 0:
            print("No results available.")
            return

        results_df = pd.DataFrame(self.results)

        results_df = results_df.sort_values(
            by="Recall",
            ascending=False
        )

        print()
        print("=" * 80)
        print("MODEL COMPARISON")
        print("=" * 80)

        print(results_df.to_string(index=False))

    #######################################################
    # Complete Training Pipeline
    #######################################################

    def run(
        self,
        dataset_path,
        model_path,
        results_path
    ):

        self.load_dataset(dataset_path)

        self.split_dataset()

        self.train_models()

        self.show_results()

        self.save_model(model_path)

        self.save_results(results_path)

        print()
        print("=" * 60)
        print("Training Completed Successfully")
        print("=" * 60)