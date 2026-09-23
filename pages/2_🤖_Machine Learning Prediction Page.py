import json
from utils.ml_model import predict_fault
import streamlit as st
from utils.influx_connection import get_latest_sensor_data
from datetime import datetime

st.set_page_config(page_title="Machine Learning Prediction",
                   page_icon="🤖",
                   layout="wide")

st.title("🤖 Machine Learning Prediction")
st.write("Random Forest based bearing fault diagnosis and maintenance recommendation.")
st.divider()

# ---------------------------------------
# Read Latest Prediction from SQLite
# ---------------------------------------

model_name = "Random Forest"

import sqlite3
from pathlib import Path
from datetime import datetime

db_path = Path(__file__).parent.parent / "data" / "predictive_maintenance.db"

try:

    # Read latest sensor features from InfluxDB
    latest = get_latest_sensor_data()

    feature_columns = [
        "Mean",
        "RMS",
        "Std",
        "Peak",
        "Peak_to_Peak",
        "Skewness",
        "Kurtosis",
        "Crest_Factor",
        "Shape_Factor",
        "Impulse_Factor",
        "Spectral_Energy",
        "Dominant_Frequency",
        "Amp_BPFO",
        "Amp_BPFI",
        "Amp_BSF",
        "BPFO_BPFI_Ratio",
        "Band_0_500",
        "Band_500_1000",
        "Band_1000_2000",
        "Wavelet_D1",
        "Wavelet_D2",
        "Wavelet_D3",
        "Wavelet_D4"
    ]

    features = [latest[column] for column in feature_columns]

    prediction, confidence = predict_fault(features)

    # Save prediction into SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (timestamp, prediction, confidence)
    VALUES (?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        str(prediction),
        float(confidence)
    ))
    prediction_id = cursor.lastrowid

    conn.commit()
    conn.close()

    st.success("✅ Prediction saved successfully!")

     # ---------------------------------------
    # Automatic Maintenance Work Order
    # ---------------------------------------

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
#---------------------------------------
# Check for an existing open work order
#---------------------------------------
    cursor.execute("""
    SELECT
        id,
        work_order,
        equipment,
        priority,
        status,
        assigned_to,
        created_on
    FROM work_orders
    WHERE status='Open'
    ORDER BY id DESC
    LIMIT 1
    """)

    current_work_order = cursor.fetchone()
#-------------------------------------------------------
# Create a work order for the current prediction
#-------------------------------------------------------
    if prediction != "Healthy":

        work_order_number = "WO-" + datetime.now().strftime("%Y%m%d-%H%M%S")

        cursor.execute("""
        INSERT INTO work_orders
        (
            work_order,
            equipment,
            priority,
            status,
            assigned_to,
            created_on,
            prediction_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            work_order_number,
            "Bearing Assembly",
            "High",
            "Open",
            "Maintenance Team",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prediction_id
        ))

        conn.commit()
#------------------------------------------------------
# Read the work order linked to the current prediction
#------------------------------------------------------
        cursor.execute("""
        SELECT
            id,
            work_order,
            equipment,
            priority,
            status,
            assigned_to,
            created_on
        FROM work_orders
        WHERE prediction_id = ?
        LIMIT 1
        """, (prediction_id,))

        current_work_order = cursor.fetchone()

    conn.close()
#-----------------------------------------
# Always display the current work order
#-----------------------------------------
    if current_work_order:

        st.success("🔧 Maintenance Work Order Generated")

        st.info(f"""
### Automatically Generated Work Order

**Work Order Number:** {current_work_order[1]}

**Equipment:** {current_work_order[2]}

**Priority:** {current_work_order[3]}

**Status:** {current_work_order[4]}

**Assigned To:** {current_work_order[5]}

**Created On:** {current_work_order[6]}
""")

except Exception as e:

    st.error(f"Error: {e}")

    prediction = "No Prediction"
    confidence = 0

    mean = 0
    peak = 0
    peak_to_peak = 0
    rms = 0
    std = 0
       
# Prediction Summary
st.header("Prediction Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Prediction Model",
        model_name
    )

with col2:
    st.metric(
        "Predicted Fault",
        prediction
    )

with col3:
    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(confidence / 100)
#-----------------------------------  
# Model Information
#-----------------------------------
st.divider()

st.header("Model Information")

st.info("""
**Model Name:** Random Forest Classifier

**Training Dataset:** Case Western Reserve University (CWRU) Bearing Dataset

**Predictors Used:** 23 engineered vibration features

**Validation:** Source-file grouped four-fold validation

**Model Configuration:** 200 trees, random state 42

**Feature Selection:** No separate feature-selection step was applied; the final model uses the defined 23-feature predictor set.
""")
#----------------------------------------
# Maintenance Recommendation
#----------------------------------------
if prediction == "Healthy":
    st.success("🟢 No Immediate Maintenance Required")
else:
    st.error("🔴 High Priority Maintenance Required")
# ---------------------------------------
# Feature Values Used
# ---------------------------------------

st.divider()

st.header("Feature Values Used")

import pandas as pd

feature_df = pd.DataFrame({
    "Feature": feature_columns,
    "Value": [
        latest[column]
        for column in feature_columns
    ]
})

st.dataframe(
    feature_df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------
# Random Forest Feature Importance
# ---------------------------------------

st.divider()

st.header("Random Forest Feature Importance")

import joblib
import matplotlib.pyplot as plt

model_path = Path(__file__).parent.parent / "models" / "random_forest_23_features.pkl"

rf_model = joblib.load(model_path)

feature_importance_df = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": rf_model.feature_importances_
})

# Sort from highest to lowest importance
feature_importance_df = feature_importance_df.sort_values(
    "Importance",
    ascending=True
)

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(10, 8))

ax.barh(
    feature_importance_df["Feature"],
    feature_importance_df["Importance"],
    height=0.45
)

ax.set_xlabel("Importance")
ax.set_ylabel("Feature")
ax.set_title("Random Forest Feature Importance")

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)
# ---------------------------------------
# Prediction History
# ---------------------------------------

st.header("Prediction History")

import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path(__file__).parent.parent / "database" / "predictive_maintenance.db"

conn = sqlite3.connect(db_path)

history = pd.read_sql_query("""
SELECT
    timestamp AS Time,
    prediction AS Prediction,
    ROUND(confidence,2) AS Confidence
FROM predictions
ORDER BY id DESC
LIMIT 10
""", conn)

conn.close()

history["Confidence"] = history["Confidence"].astype(str) + "%"

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)
# ---------------------------------------
# Model Performance
# ---------------------------------------

st.divider()

st.header("Model Performance")

performance_path = (
    Path(__file__).parent.parent
    / "models"
    / "random_forest_performance.json"
)

with open(performance_path, "r") as f:
    performance = json.load(f)
#st.write("DEBUG:", performance)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Accuracy",
        f"{performance['accuracy'] * 100:.2f}%"
    )

with col2:
    st.metric(
        "Macro F1-score",
        f"{performance['macro_f1'] * 100:.2f}%"
    )

with col3:
    st.metric(
        "MCC",
        f"{performance['mcc']:.4f}"
    )

st.caption(
    f"{performance['validation']} | "
    f"{performance['predictors']} predictors | "
    f"Fold SD: {performance['standard_deviation']:.4f}"
)

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)
