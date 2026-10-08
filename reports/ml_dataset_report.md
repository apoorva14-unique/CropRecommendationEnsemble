# Machine Learning Dataset Preparation & Split Report

**Document Version:** 1.0  
**Execution Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Source Dataset:** `data/processed/crop_data_cleaned.csv`  
**Status:** Validated, Leakage-Free, and Ready for Model Training.  

---

## 1. Executive Summary & Sample Counts

- **Final Total Samples:** **611** (100.0% data retention; 0 rows removed)
- **Training Set Size:** **490 samples** (80.20% of dataset)
- **Testing Set Size:** **121 samples** (19.80% of dataset)
- **Candidate Input Features:** **16 features** (1 categorical, 15 continuous numerical)
- **Final Post-Pipeline Encoded ML Features:** **27 features** (15 numerical + 12 One-Hot Encoded soil types)
- **Target Variable:** `CROP` (**34 canonical classes**)

---

## 2. Feature Schema & Column Boundary Evaluation

### 2.1 Excluded Columns and Scientific Rationale

| Column Name | Unique Count | Classification | Treatment | Forensic / Agronomic Justification |
| :--- | :---: | :---: | :---: | :--- |
| **`S.NO`** | 608 | Administrative ID | **EXCLUDED** | Arbitrary sequential identifier assigned to soil samples. Including `S.NO` as a feature would cause artificial index memorization and catastrophic data leakage. |
| **`MANDAL NAME`** | 27 | Geographic Sub-district | **EXCLUDED** | Administrative boundary. A generalizable crop recommender must predict crops based on biophysical soil/climate traits, not geographic addresses. Including Mandal causes severe spatial overfitting. |
| **`VILLAGE NAME`** | 231 | Hamlet Address | **EXCLUDED** | High-cardinality nominal text (38% cardinality ratio). Including 231 sparse categories creates extreme dimensionality curse and memorization without agronomic generalization. |

### 2.2 Included Input Features

#### Categorical Features (1 Feature)
- **`SOIL TYPE`:** Nominal integer taxonomy codes (1 to 13; code 6 absent). Represents fundamental soil physical properties (texture, depth, porosity, drainage). Treated strictly as nominal categorical and encoded via One-Hot Encoding.

#### Numerical Features (15 Features)
1. **Soil Chemical Properties (12 Features):**
   - Primary Macronutrients: Available Nitrogen (`N`, kg/ha), Available Phosphorus (`P2O5`, kg/ha), Available Potassium (`K20`, kg/ha)
   - Geochemical Foundations: Soil Reaction (`PH`), Electrical Conductivity (`EC`, dS/m), Organic Carbon (`OC`, %)
   - Secondary & Micronutrients: Available Sulphur (`S`, ppm), Available Copper (`CU`, ppm), Field Capacity / DTPA Iron (`FC`, ppm), Available Manganese (`MN`, ppm), Available Zinc (`ZN`, ppm), Boron / Barium Index (`BA`, ppm)
2. **Agro-Climatic Properties (3 Features):**
   - Mean Ambient Temperature (`Temparature`, °C)
   - Relative Atmospheric Humidity (`Humidity`, %)
   - Seasonal / Annual Precipitation (`Rainfall`, mm)

---

## 3. Target Variable & Class Distribution Analysis

### 3.1 Class Imbalance & Singleton Classes
The target variable `CROP` encompasses **34 canonical classes** across 611 samples. The distribution exhibits acute natural class imbalance:
- Dominant classes ($N \ge 30$): `Paddy` (143), `Black Gram` (95), `Cotton` (93), `Groundnut` (61), `Turmeric` (35), `Bajra` (34), `Bengal Gram` (30) constitute **80.36%** of all samples.
- Rare classes ($N < 4$): 16 classes constitute only **4.09%** of samples.
- **Singleton classes ($N = 1$):** Exactly **10 classes** (`Guava`, `Chamanthi (Mums)`, `Muskmelon`, `Red Gram`, `Sweet Lime`, `Castor`, `Allam (Ginger)`, `Nannari`, `Papaya`, `Green Chilli`).

### 3.2 Complete Class Distribution: Train vs. Test

| # | Crop Class | Total Count | % of Dataset | Train Count | Test Count | Train Allocation % |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | **`Paddy`** | 143 | 23.40% | 114 | 29 | 79.7% |
| 2 | **`Black Gram`** | 95 | 15.55% | 76 | 19 | 80.0% |
| 3 | **`Cotton`** | 93 | 15.22% | 74 | 19 | 79.6% |
| 4 | **`Groundnut`** | 61 | 9.98% | 49 | 12 | 80.3% |
| 5 | **`Turmeric`** | 35 | 5.73% | 28 | 7 | 80.0% |
| 6 | **`Bajra`** | 34 | 5.56% | 27 | 7 | 79.4% |
| 7 | **`Bengal Gram`** | 30 | 4.91% | 24 | 6 | 80.0% |
| 8 | **`Sweet Orange`** | 17 | 2.78% | 14 | 3 | 82.4% |
| 9 | **`Banana`** | 14 | 2.29% | 11 | 3 | 78.6% |
| 10 | **`Sunflower`** | 13 | 2.13% | 10 | 3 | 76.9% |
| 11 | **`Soybean`** | 9 | 1.47% | 7 | 2 | 77.8% |
| 12 | **`Onion`** | 8 | 1.31% | 6 | 2 | 75.0% |
| 13 | **`Jowar`** | 7 | 1.15% | 6 | 1 | 85.7% |
| 14 | **`Chamanthi`** | 7 | 1.15% | 6 | 1 | 85.7% |
| 15 | **`Vegetables`** | 6 | 0.98% | 5 | 1 | 83.3% |
| 16 | **`Sesame`** | 6 | 0.98% | 5 | 1 | 83.3% |
| 17 | **`Korra`** | 4 | 0.65% | 3 | 1 | 75.0% |
| 18 | **`Tomato`** | 4 | 0.65% | 3 | 1 | 75.0% |
| 19 | **`Bean Gram (Pending Verification)`** | 3 | 0.49% | 2 | 1 | 66.7% |
| 20 | **`Chilli`** | 3 | 0.49% | 2 | 1 | 66.7% |
| 21 | **`Red Chilli`** | 3 | 0.49% | 2 | 1 | 66.7% |
| 22 | **`Acid Lime`** | 2 | 0.33% | 2 | 0 | 100.0% |
| 23 | **`Maize`** | 2 | 0.33% | 2 | 0 | 100.0% |
| 24 | **`Green Gram`** | 2 | 0.33% | 2 | 0 | 100.0% |
| 25 | **`Chamanthi (Mums)`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 26 | **`Muskmelon`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 27 | **`Guava`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 28 | **`Sweet Lime`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 29 | **`Red Gram`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 30 | **`Castor`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 31 | **`Allam (Ginger)`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 32 | **`Nannari`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 33 | **`Papaya`** | 1 | 0.16% | 1 | 0 | 100.0% |
| 34 | **`Green Chilli`** | 1 | 0.16% | 1 | 0 | 100.0% |

---

## 4. Split Strategy: Defensible Handling of Rare Classes

### 4.1 Why Standard Stratification Fails Mathematically
When attempting ordinary `train_test_split(X, y, test_size=0.20, stratify=y)` on this dataset, scikit-learn raises an immediate `ValueError`:
```text
ValueError: The least populated class in y has only 1 member, which is too few. The minimum number of groups for any class cannot be less than 2.
```
Mathematically, a singleton sample ($N=1$) cannot be partitioned into two disjoint subsets. Placing the singleton in the test set would guarantee that the training set has 0 samples for that class—creating an impossible, unlearnable prediction task. Silently deleting rare classes violates the core requirement of preserving authentic agricultural diversity.

### 4.2 Approved Hybrid Singleton-Allocated Stratified Split
1. **Singleton Deterministic Allocation:** All 10 singletons ($N=1$) are assigned deterministically to the **training set** (`X_train, y_train`). This guarantees the model observes all 34 known crop classes during training.
2. **Exact Stratification for Multi-Sample Classes:** The remaining 24 classes ($N=601$) are split using strict stratified random sampling (`test_size=0.20, random_state=42`).
3. **Outcome:**
   - **Train Set:** 490 samples (80.20%) covering all 34 classes.
   - **Test Set:** 121 samples (19.80%) covering 21 evaluated classes.
   - **Zero Class Leakage:** 100% of test classes have corresponding training instances.

### 4.3 Supervised Cross-Validation Benchmark Protocol ($N \ge 4$)
For downstream 5-fold cross-validation during ensemble model training, classes with $N \ge 4$ (18 classes, $N=601$, $98.36\%$ of data) will serve as the primary stratified CV benchmark, while the complete 34-class dataset serves for retrieval and full evaluation.

---

## 5. Machine Learning Preprocessing Pipeline & Encoding

### 5.1 Leakage-Free Architecture
In accordance with strict machine learning standards, **no transformations were fitted on the complete dataset prior to splitting**. The preprocessing pipeline was constructed using `sklearn.compose.ColumnTransformer` and fitted **strictly and exclusively on `X_train_raw`**.

### 5.2 Preprocessing Components
1. **Categorical Feature Encoding:**
   - Feature: `SOIL TYPE` (codes: 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13)
   - Transformer: `OneHotEncoder(categories=..., handle_unknown='ignore', sparse_output=False)`
   - Output: 12 binary dummy columns (`SOIL_TYPE_1` through `SOIL_TYPE_13`)
   - Fault Tolerance: `handle_unknown='ignore'` prevents runtime exceptions if an unseen soil category appears in future inference.
2. **Numerical Feature Processing & Missing Value Imputation:**
   - Features: 15 continuous soil/weather attributes
   - Transformer: `SimpleImputer(strategy='median')`
   - Median imputation learned strictly from `X_train` training folds.

### 5.3 Encoded Feature Inventory (27 Features)

| # | Feature Name | Source Column | Feature Type | Role in Models |
| :-: | :--- | :--- | :---: | :--- |
| 1 | **`PH`** | `PH` | Continuous Float | Chemical / Environmental Parameter |
| 2 | **`EC`** | `EC` | Continuous Float | Chemical / Environmental Parameter |
| 3 | **`OC`** | `OC` | Continuous Float | Chemical / Environmental Parameter |
| 4 | **`N`** | `N` | Continuous Float | Chemical / Environmental Parameter |
| 5 | **`P2O5`** | `P2O5` | Continuous Float | Chemical / Environmental Parameter |
| 6 | **`K20`** | `K20` | Continuous Float | Chemical / Environmental Parameter |
| 7 | **`S`** | `S` | Continuous Float | Chemical / Environmental Parameter |
| 8 | **`CU`** | `CU` | Continuous Float | Chemical / Environmental Parameter |
| 9 | **`FC`** | `FC` | Continuous Float | Chemical / Environmental Parameter |
| 10 | **`MN`** | `MN` | Continuous Float | Chemical / Environmental Parameter |
| 11 | **`ZN`** | `ZN` | Continuous Float | Chemical / Environmental Parameter |
| 12 | **`BA`** | `BA` | Continuous Float | Chemical / Environmental Parameter |
| 13 | **`Temparature`** | `Temparature` | Continuous Float | Chemical / Environmental Parameter |
| 14 | **`Humidity`** | `Humidity` | Continuous Float | Chemical / Environmental Parameter |
| 15 | **`Rainfall`** | `Rainfall` | Continuous Float | Chemical / Environmental Parameter |
| 16 | **`SOIL_TYPE_1`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 17 | **`SOIL_TYPE_2`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 18 | **`SOIL_TYPE_3`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 19 | **`SOIL_TYPE_4`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 20 | **`SOIL_TYPE_5`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 21 | **`SOIL_TYPE_7`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 22 | **`SOIL_TYPE_8`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 23 | **`SOIL_TYPE_9`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 24 | **`SOIL_TYPE_10`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 25 | **`SOIL_TYPE_11`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 26 | **`SOIL_TYPE_12`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |
| 27 | **`SOIL_TYPE_13`** | `SOIL TYPE` | Binary Indicator (0/1) | Soil Taxonomy Classification |

---

## 6. Data Leakage Risk Audit

Every potential point of data leakage has been audited and mitigated:

1. **Global Fit Leakage:** Mitigated. Scalers, imputers, and encoders are fitted strictly on `X_train`.
2. **Serial ID Memorization:** Mitigated. `S.NO` is completely omitted from feature matrices.
3. **Geographic Memorization:** Mitigated. `MANDAL NAME` and `VILLAGE NAME` are omitted from feature matrices.
4. **Unseen Class Crash:** Mitigated. Singletons allocated to train ensure 100% test class coverage.
5. **Index Misalignment:** Programmatic assertion confirms `X_train.index == y_train.index` identically.

---

## 7. Reproducibility Settings & Artifact Manifest

- **Random Seed:** `random_state = 42`
- **Execution Script:** `week3_preprocessing/ml_preparation.py`
- **Pipeline Serialization:** `data/processed/ml_preprocessor_pipeline.joblib`

### Generated Artifacts

| File | Dimensions | Purpose |
| :--- | :---: | :--- |
| [`data/processed/X_train.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/X_train.csv) | $490 \times 27$ | Post-pipeline encoded training features |
| [`data/processed/X_test.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/X_test.csv) | $121 \times 27$ | Post-pipeline encoded testing features |
| [`data/processed/y_train.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/y_train.csv) | $490 \times 1$ | Training target labels (`CROP`) |
| [`data/processed/y_test.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/y_test.csv) | $121 \times 1$ | Testing target labels (`CROP`) |
| [`data/processed/X_train_raw.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/X_train_raw.csv) | $490 \times 16$ | Pre-encoded training features (16 features) |
| [`data/processed/X_test_raw.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/X_test_raw.csv) | $121 \times 16$ | Pre-encoded testing features (16 features) |
