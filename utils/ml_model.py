# ============================================
# 23-Feature Random Forest Prediction Utility
# ============================================

from pathlib import Path
import joblib
import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Final 23-feature Random Forest model
MODEL_PATH = BASE_DIR / "models" / "random_forest_23_features.pkl"


# Exact feature schema used by the trained model
FEATURE_SCHEMA_PATH = (
    BASE_DIR / "models" / "random_forest_23_features_columns.txt"
)


# Load the trained model
model = joblib.load(MODEL_PATH)


# Load the exact feature order
with open(FEATURE_SCHEMA_PATH, "r") as f:
    FEATURE_COLUMNS = [line.strip() for line in f if line.strip()]


def predict_fault(features):

    # Check that the supplied feature set contains
    # exactly the expected 23 predictors
    if len(features) != len(FEATURE_COLUMNS):
        raise ValueError(
            f"Expected {len(FEATURE_COLUMNS)} features, "
            f"but received {len(features)}."
        )

    # Create a DataFrame using the exact trained feature order
    feature_df = pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS
    )

    # Run Random Forest prediction
    prediction = model.predict(feature_df)[0]

    # Prediction confidence
    confidence = model.predict_proba(feature_df).max() * 100


    # Convert numerical class to bearing-condition name
    label_mapping = {
        0: "Healthy",
        1: "Inner Race Fault",
        2: "Ball Fault",
        3: "Outer Race Fault"
    }


    prediction_name = label_mapping.get(
        int(prediction),
        "Unknown"
    )


    return prediction_name, confidence
