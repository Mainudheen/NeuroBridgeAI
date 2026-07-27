"""
=========================================================
NeuroBridge AI
Plot Utilities
=========================================================

Contains all visualization functions.

Author : NeuroBridge AI
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class PlotManager:

    #########################################################
    # Model Comparison
    #########################################################

    @staticmethod
    def model_comparison(results_df, save_path):

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        results_df = results_df.sort_values(
            by="Recall",
            ascending=False
        )

        plt.figure(figsize=(10, 6))

        plt.bar(
            results_df["Model"],
            results_df["Recall"]
        )

        plt.title("Model Comparison (Recall)")
        plt.xlabel("Models")
        plt.ylabel("Recall")

        plt.xticks(rotation=30, ha="right")

        plt.tight_layout()

        plt.savefig(save_path)

        plt.close()

        print(f"\nModel comparison saved to:\n{save_path}")

    #########################################################
    # Feature Importance
    #########################################################

    @staticmethod
    def feature_importance(feature_df, save_path):

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        feature_df = feature_df.sort_values(
            by="Importance",
            ascending=False
        )

        plt.figure(figsize=(10,6))

        plt.barh(
            feature_df["Feature"],
            feature_df["Importance"]
        )

        plt.gca().invert_yaxis()

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(save_path)

        plt.close()

        print(f"\nFeature importance saved to:\n{save_path}")

    #########################################################
    # Metric Comparison
    #########################################################

    @staticmethod
    def metrics(results_df, save_path):

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        metrics = results_df.set_index("Model")[
            [
                "Accuracy",
                "Precision",
                "Recall",
                "F1 Score",
                "ROC AUC"
            ]
        ]

        plt.figure(figsize=(12,6))

        metrics.plot(kind="bar")

        plt.title("Performance Metrics")

        plt.ylabel("Score")

        plt.xticks(rotation=30, ha="right")

        plt.tight_layout()

        plt.savefig(save_path)

        plt.close()

        print(f"\nMetrics chart saved to:\n{save_path}")

    #########################################################
    # Cross Validation
    #########################################################

    @staticmethod
    def cross_validation(results_df, save_path):

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(10,6))

        plt.bar(
            results_df["Model"],
            results_df["Cross Validation"]
        )

        plt.title("Cross Validation Accuracy")

        plt.ylabel("Accuracy")

        plt.xticks(rotation=30, ha="right")

        plt.tight_layout()

        plt.savefig(save_path)

        plt.close()

        print(f"\nCross Validation chart saved to:\n{save_path}")