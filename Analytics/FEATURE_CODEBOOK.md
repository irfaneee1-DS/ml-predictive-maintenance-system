# 23-Feature Codebook

The final machine-learning dataset uses 23 engineered vibration features.

| No. | Feature | Feature group |
|---:|---|---|
| 1 | Mean | Time-domain |
| 2 | RMS | Time-domain |
| 3 | Std | Time-domain |
| 4 | Peak | Time-domain |
| 5 | Peak_to_Peak | Time-domain |
| 6 | Skewness | Time-domain |
| 7 | Kurtosis | Time-domain |
| 8 | Crest_Factor | Time-domain |
| 9 | Shape_Factor | Time-domain |
| 10 | Impulse_Factor | Time-domain |
| 11 | Spectral_Energy | Frequency-domain |
| 12 | Dominant_Frequency | Frequency-domain |
| 13 | Amp_BPFO | Bearing-frequency |
| 14 | Amp_BPFI | Bearing-frequency |
| 15 | Amp_BSF | Bearing-frequency |
| 16 | BPFO_BPFI_Ratio | Bearing-frequency |
| 17 | Band_0_500 | Frequency-band |
| 18 | Band_500_1000 | Frequency-band |
| 19 | Band_1000_2000 | Frequency-band |
| 20 | Wavelet_D1 | Wavelet |
| 21 | Wavelet_D2 | Wavelet |
| 22 | Wavelet_D3 | Wavelet |
| 23 | Wavelet_D4 | Wavelet |

## Feature descriptions

- **Mean** — Mean value of the vibration signal.
- **RMS** — Root-mean-square magnitude of the vibration signal.
- **Std** — Standard deviation of the vibration signal.
- **Peak** — Maximum peak magnitude of the vibration signal.
- **Peak_to_Peak** — Difference between the maximum and minimum signal values.
- **Skewness** — Measure of the asymmetry of the signal distribution.
- **Kurtosis** — Measure describing the peakedness/tail behaviour of the signal distribution.
- **Crest_Factor** — Ratio of peak magnitude to RMS.
- **Shape_Factor** — Ratio of RMS to the mean absolute signal value.
- **Impulse_Factor** — Ratio of peak magnitude to the mean absolute signal value.
- **Spectral_Energy** — Energy calculated from the frequency-domain representation.
- **Dominant_Frequency** — Frequency component with the highest magnitude in the analysed spectrum.
- **Amp_BPFO** — Amplitude associated with the Ball Pass Frequency Outer race.
- **Amp_BPFI** — Amplitude associated with the Ball Pass Frequency Inner race.
- **Amp_BSF** — Amplitude associated with the Ball Spin Frequency.
- **BPFO_BPFI_Ratio** — Ratio between the BPFO- and BPFI-related amplitudes.
- **Band_0_500** — Frequency-band feature for 0–500 Hz.
- **Band_500_1000** — Frequency-band feature for 500–1000 Hz.
- **Band_1000_2000** — Frequency-band feature for 1000–2000 Hz.
- **Wavelet_D1** — Wavelet detail coefficient feature at decomposition level D1.
- **Wavelet_D2** — Wavelet detail coefficient feature at decomposition level D2.
- **Wavelet_D3** — Wavelet detail coefficient feature at decomposition level D3.
- **Wavelet_D4** — Wavelet detail coefficient feature at decomposition level D4.

## Target variable

The classification target is:

| Label | Class |
|---:|---|
| 0 | Healthy |
| 1 | Inner Race Fault |
| 2 | Ball Fault |
| 3 | Outer Race Fault |

The final Random Forest model uses these 23 predictors in the order stored in:

`models/random_forest_23_features_columns.txt`
