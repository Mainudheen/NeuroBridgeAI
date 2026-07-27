"""
==========================================================
NeuroBridge AI
Data Preprocessing Utility
==========================================================
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder


class DataPreprocessor:

    def __init__(self):

        self.encoders = {}

    # ---------------------------------------------------
    # Load Dataset
    # ---------------------------------------------------

    def load_dataset(self, path):

        df = pd.read_csv(path)

        print("Dataset Loaded Successfully")

        print("Shape :", df.shape)

        return df

    # ---------------------------------------------------
    # Remove Duplicates
    # ---------------------------------------------------

    def remove_duplicates(self, df):

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        print(f"Removed {before-after} duplicate rows")

        return df

    # ---------------------------------------------------
    # Handle Missing Values
    # ---------------------------------------------------

    def handle_missing_values(self, df):

        df.replace("?", np.nan, inplace=True)

        df.replace("", np.nan, inplace=True)

        df.replace("NA", np.nan, inplace=True)

        df.replace("N/A", np.nan, inplace=True)

        # Numeric Columns

        numeric = df.select_dtypes(include=["int64", "float64"]).columns

        for col in numeric:

            df[col].fillna(df[col].median(), inplace=True)

        # Categorical Columns

        categorical = df.select_dtypes(include=["object"]).columns

        for col in categorical:

            mode = df[col].mode()

            if len(mode) > 0:

                df[col].fillna(mode[0], inplace=True)

            else:

                df[col].fillna("Unknown", inplace=True)

        return df

    # ---------------------------------------------------
    # Remove Leakage
    # ---------------------------------------------------

    def remove_leakage(self, df):

        if "result" in df.columns:

            df.drop(columns=["result"], inplace=True)

            print("Removed result column")

        return df

    # ---------------------------------------------------
    # Encode Target
    # ---------------------------------------------------

    def encode_target(self, df):

        df["Class/ASD"] = (

            df["Class/ASD"]

            .astype(str)

            .str.upper()

            .str.strip()

        )

        df["Class/ASD"] = df["Class/ASD"].replace({

            "YES": 1,

            "NO": 0

        })

        return df

    # ---------------------------------------------------
    # Encode Features
    # ---------------------------------------------------

    def encode_features(self, df):

        categorical = df.select_dtypes(include=["object"]).columns

        for col in categorical:

            encoder = LabelEncoder()

            df[col] = encoder.fit_transform(df[col].astype(str))

            self.encoders[col] = encoder

        return df

    # ---------------------------------------------------
    # Save Encoders
    # ---------------------------------------------------

    def save_encoders(self, path):

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.encoders, path)

        print("Encoders Saved")

    # ---------------------------------------------------
    # Final Check
    # ---------------------------------------------------

    def validate(self, df):

        print()

        print("Remaining Missing Values")

        print(df.isnull().sum())

        total = df.isnull().sum().sum()

        print()

        print("Total NaN :", total)

        if total != 0:

            raise Exception("Dataset still contains NaN values.")

        print("Validation Passed")

    # ---------------------------------------------------
    # Save Dataset
    # ---------------------------------------------------

    def save_dataset(self, df, path):

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(path, index=False)

        print("Dataset Saved")

    # ---------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------

    def process(self, input_path, output_path, encoder_path):

        df = self.load_dataset(input_path)

        df = self.remove_duplicates(df)

        df = self.handle_missing_values(df)

        df = self.remove_leakage(df)

        df = self.encode_target(df)

        df = self.encode_features(df)

        df.dropna(inplace=True)

        self.validate(df)

        self.save_dataset(df, output_path)

        self.save_encoders(encoder_path)

        print()

        print("=" * 60)

        print("PREPROCESSING COMPLETED SUCCESSFULLY")

        print("=" * 60)

        return df