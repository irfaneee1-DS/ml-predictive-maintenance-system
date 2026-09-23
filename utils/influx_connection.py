import os
from pathlib import Path

import pandas as pd
import streamlit as st
from influxdb_client_3 import InfluxDBClient3


# -----------------------------------
# Configuration
# -----------------------------------

def _get_config(key, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key, default)


HOST = _get_config("INFLUXDB_HOST", "http://localhost:8181")
DATABASE = _get_config("INFLUXDB_DATABASE", "dissertation")

TOKEN = (
    _get_config("INFLUXDB_TOKEN")
    or _get_config("DB_TOKEN")
)

client = None


# -----------------------------------
# Bundled CSV fallback
# -----------------------------------

CSV_FALLBACK_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "phase1_full_dataset.csv"
)


# -----------------------------------
# Get latest data from InfluxDB
# -----------------------------------

def _get_latest_from_influxdb():

    global client

    if not TOKEN:
        raise RuntimeError("InfluxDB token is not configured")

    if client is None:
        client = InfluxDBClient3(
            host=HOST,
            token=TOKEN,
            database=DATABASE
        )

    query = """
    SELECT *
    FROM bearing_features
    ORDER BY time DESC
    LIMIT 1
    """

    table = client.query(query=query)
    df = table.to_pandas()

    latest = df.iloc[0]

    return {
        "Mean": latest["Mean"],
        "RMS": latest["RMS"],
        "Std": latest["Std"],
        "Peak": latest["Peak"],
        "Peak_to_Peak": latest["Peak_to_Peak"],
        "Skewness": latest["Skewness"],
        "Kurtosis": latest["Kurtosis"],
        "Crest_Factor": latest["Crest_Factor"],
        "Shape_Factor": latest["Shape_Factor"],
        "Impulse_Factor": latest["Impulse_Factor"],
        "Spectral_Energy": latest["Spectral_Energy"],
        "Dominant_Frequency": latest["Dominant_Frequency"],
        "Amp_BPFO": latest["Amp_BPFO"],
        "Amp_BPFI": latest["Amp_BPFI"],
        "Amp_BSF": latest["Amp_BSF"],
        "BPFO_BPFI_Ratio": latest["BPFO_BPFI_Ratio"],
        "Band_0_500": latest["Band_0_500"],
        "Band_500_1000": latest["Band_500_1000"],
        "Band_1000_2000": latest["Band_1000_2000"],
        "Wavelet_D1": latest["Wavelet_D1"],
        "Wavelet_D2": latest["Wavelet_D2"],
        "Wavelet_D3": latest["Wavelet_D3"],
        "Wavelet_D4": latest["Wavelet_D4"],
        "Label": latest["Label"],
        "Time": latest["time"],
        "Source": "InfluxDB (live)"
    }


# -----------------------------------
# Get fallback data from bundled CSV
# -----------------------------------

def _get_latest_from_csv():

    df = pd.read_csv(CSV_FALLBACK_PATH)

    # Remove accidental whitespace from column names
    df.columns = df.columns.str.strip()

    latest = df.iloc[-1]

    return {
        "Mean": latest["Mean"],
        "RMS": latest["RMS"],
        "Std": latest["Std"],
        "Peak": latest["Peak"],
        "Peak_to_Peak": latest["Peak_to_Peak"],
        "Skewness": latest["Skewness"],
        "Kurtosis": latest["Kurtosis"],
        "Crest_Factor": latest["Crest_Factor"],
        "Shape_Factor": latest["Shape_Factor"],
        "Impulse_Factor": latest["Impulse_Factor"],
        "Spectral_Energy": latest["Spectral_Energy"],
        "Dominant_Frequency": latest["Dominant_Frequency"],
        "Amp_BPFO": latest["Amp_BPFO"],
        "Amp_BPFI": latest["Amp_BPFI"],
        "Amp_BSF": latest["Amp_BSF"],
        "BPFO_BPFI_Ratio": latest["BPFO_BPFI_Ratio"],
        "Band_0_500": latest["Band_0_500"],
        "Band_500_1000": latest["Band_500_1000"],
        "Band_1000_2000": latest["Band_1000_2000"],
        "Wavelet_D1": latest["Wavelet_D1"],
        "Wavelet_D2": latest["Wavelet_D2"],
        "Wavelet_D3": latest["Wavelet_D3"],
        "Wavelet_D4": latest["Wavelet_D4"],
        "Label": latest["Label"],
        #time = latest.get("Time", "CSV fallback")
        "Source": "CSV fallback"
    }

# -----------------------------------
# Main function
# -----------------------------------

def get_latest_sensor_data():

    try:
        return _get_latest_from_influxdb()

    except Exception:
        return _get_latest_from_csv()
