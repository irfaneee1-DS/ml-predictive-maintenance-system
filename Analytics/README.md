# Analytical Reproducibility

This folder contains the analytical notebooks used for the Predictive Maintenance ML System.

## Environment

The analytical notebooks were developed using:

- Python 3.13.9
- NumPy 2.1.3
- Pandas 2.2.3
- SciPy 1.15.3
- PyWavelets 1.8.0
- Scikit-learn 1.6.1
- XGBoost 3.3.0
- SHAP 0.52.0
- Joblib 1.4.2
- Matplotlib 3.10.0

The complete pinned dependency list is provided in the repository root `requirements.txt`.

## Analytical Workflow

Run the notebooks in the following order:

1. `01_Load_CWRU_Data.ipynb`  
   CWRU bearing data loading and preparation.

2. `02_Windowing_and_Segmentation.ipynb`  
   Signal windowing and segmentation.

3. `03_Feature_Engineering.ipynb`  
   Extraction of the engineered vibration features.

4. `04_Build_ML_Dataset.ipynb`  
   Construction of the machine-learning dataset.

5. `07_Random Forest & Decision Tree.ipynb`  
   Random Forest and Decision Tree modelling.

6. `08_GroupKFold Validation.ipynb`  
   Grouped validation of the models.

7. `09_XGBoost.ipynb`  
   XGBoost modelling.

8. `10_SHAP Explainability.ipynb`  
   SHAP-based explainability analysis.

9. `11_Final_23_Feature_RF_Deployment.ipynb`  
   Final 23-feature Random Forest model preparation for deployment.

10. `16_Fair_4Class_Model_Comparison.ipynb`  
    Four-class comparison of the final models.

## Existing Project Outputs

The resulting analytical outputs are stored in the repository `data/` directory, including:

- `phase1_full_dataset.csv`
- `groupfold_results.csv`
- `model_comparison.csv`
- `window_summary.csv`
- `shap_feature_importance.csv`
- `xgboost_feature_importance.csv`

The final Random Forest deployment artefacts are stored in `models/`:

- `random_forest_23_features.pkl`
- `random_forest_23_features_columns.txt`
- `random_forest_performance.json`

## Source Data

The analytical workflow uses the Case Western Reserve University (CWRU) bearing dataset.

The raw `.mat` source files are not included in this repository. The source-file definitions used for the analysis are documented separately as part of the project reproducibility documentation.

## Reproduction

1. Install the pinned dependencies from the repository root:

   `pip install -r requirements.txt`

2. Obtain the required CWRU source data.

3. Run the analytical notebooks in the workflow order listed above.

4. The notebooks generate the analytical datasets, validation results, model-comparison results and explainability outputs used by the project.

5. The final Random Forest deployment artefacts are stored in the `models/` directory.

## Separation of Code

The `Analytics/` directory contains the analytical notebooks.

The application implementation is maintained separately in:

- `pages/`
- `utils/`
- `0_🏠_Home.py`

This separation distinguishes the analytical workflow from the deployed Streamlit application.
