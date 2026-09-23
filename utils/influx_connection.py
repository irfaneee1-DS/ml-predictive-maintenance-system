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



# -----------------------------------
# Get Latest Sensor Features
# -----------------------------------

def get_latest_sensor_data():

    query = """
    SELECT *
    FROM bearing_features
    ORDER BY time DESC
    LIMIT 1
    """

    table = client.query(query=query)

    df = table.to_pandas()

    latest = df.iloc[0]

    sensor_data = latest.to_dict()

    sensor_data["Time"] = latest["time"]

    return sensor_data
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
        "Time": latest["time"]
    }
