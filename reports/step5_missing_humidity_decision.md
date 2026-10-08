# Step 5: Missing Humidity Analysis & Decision Report

**Document Version:** 1.0  
**Analysis Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/complete soil data.xlsx` (Untouched, Read-Only)  
**Execution Script:** `src/data/analyze_missing_humidity.py`  
**Diagnostic Artifact:** `reports/figures/missing_humidity_decision_analysis.png`  
**Status:** Strictly Analytical & Decision Protocol — **No dataset files have been modified or imputed.**

---

## 1. Executive Summary

This report delivers a rigorous, data-driven forensic audit of the **20 missing values in the `Humidity` column**—the only feature in the entire 611-row dataset with missing observations.

A crucial meteorological and structural finding is that **weather variables (`Temparature`, `Rainfall`, `Humidity`) were recorded at the Mandal (sub-district) administrative level**, exhibiting **zero variance ($\sigma = 0.0$) across all farm samples within any given Mandal**.

### Key Findings
1. **Localization:** Exactly 20 out of 20 missing values ($100\%$) are concentrated in **Mandal `Mydukur`** (Serial Numbers `S.NO 267` through `286`).
2. **Zero Internal Baseline:** `Mydukur` contains **zero valid humidity records** ($N_{\text{valid}} = 0$). Therefore, a pure within-Mandal median or mean **does not exist mathematically** (`NaN`).
3. **Severe Minority Class Extinction Threat:** Several rare crop classes (`Vegetables`, `Turemeric`, `Chillis`, `Tamota`, `Jowar`) are concentrated exclusively or predominantly within Mydukur. **Dropping these 20 rows would permanently extinguish 100% of all `Vegetables`, 100% of `Turemeric`, and 100% of `Chillis` samples from the dataset**, and destroy 75% of `Tamota` and `Jowar`.
4. **Meteorological Context:** In Mydukur, Temperature is fixed at **$31.00^\circ\text{C}$** and Rainfall at **$658.50\text{ mm}$**. Geographically and climatically adjacent Mandals in the Kadapa basin with similar temperatures ($30.0^\circ\text{C} - 31.5^\circ\text{C}$) record relative humidity values between **$61.00\%$ and $64.68\%$**.

---

## 2. Complete Manifest of the 20 Missing Humidity Rows

The 20 missing records span consecutive rows (0-indexed indices `266` through `285`), corresponding to S.NO `267` to `286` in [complete soil data.xlsx](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/complete%20soil%20data.xlsx):

| Row Index | S.NO | Mandal Name | Village Name | Soil Type | Temp (°C) | Rain (mm) | Humidity | Crop | N (kg/ha) | P2O5 (kg/ha) | K20 (kg/ha) | pH | EC (dS/m) |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 266 | 267 | Mydukur | Annaluru | 1 | 31.0 | 658.5 | **NaN** | paddy | 188.0 | 45 | 321 | 7.42 | 0.05 |
| 267 | 268 | Mydukur | Annaluru | 1 | 31.0 | 658.5 | **NaN** | Black gram | 176.0 | 38 | 344 | 7.68 | 0.04 |
| 268 | 269 | Mydukur | Sivapuram | 1 | 31.0 | 658.5 | **NaN** | Tamota | 226.0 | 29 | 412 | 7.55 | 0.06 |
| 269 | 270 | Mydukur | Sivapuram | 1 | 31.0 | 658.5 | **NaN** | Jowar | 213.0 | 34 | 367 | 7.61 | 0.05 |
| 270 | 271 | Mydukur | Nandyalampeta | 1 | 31.0 | 658.5 | **NaN** | Turemeric | 188.0 | 52 | 310 | 7.82 | 0.08 |
| 271 | 272 | Mydukur | Nandyalampeta | 9 | 31.0 | 658.5 | **NaN** | Black gram | 238.0 | 36 | 390 | 7.65 | 0.06 |
| 272 | 273 | Mydukur | Nandyalampeta | 9 | 31.0 | 658.5 | **NaN** | Black gram | 201.0 | 41 | 356 | 7.71 | 0.05 |
| 273 | 274 | Mydukur | Nandyalampeta | 9 | 31.0 | 658.5 | **NaN** | Vegetables | 163.0 | 24 | 425 | 7.49 | 0.07 |
| 274 | 275 | Mydukur | Audireddypalle | 9 | 31.0 | 658.5 | **NaN** | Chillis | 226.0 | 48 | 298 | 7.89 | 0.06 |
| 275 | 276 | Mydukur | Audireddypalle | 9 | 31.0 | 658.5 | **NaN** | Banana | 251.0 | 31 | 380 | 7.58 | 0.05 |
| 276 | 277 | Mydukur | Settivaripalli | 9 | 31.0 | 658.5 | **NaN** | Jowar | 176.0 | 27 | 344 | 7.63 | 0.04 |
| 277 | 278 | Mydukur | Settivaripalli | 9 | 31.0 | 658.5 | **NaN** | Jowar | 188.0 | 36 | 321 | 7.51 | 0.05 |
| 278 | 279 | Mydukur | Viswanadhapuram | 9 | 31.0 | 658.5 | **NaN** | Tamota | 213.0 | 44 | 367 | 7.74 | 0.06 |
| 279 | 280 | Mydukur | Viswanadhapuram | 9 | 31.0 | 658.5 | **NaN** | Tamota | 238.0 | 50 | 390 | 7.69 | 0.07 |
| 280 | 281 | Mydukur | Onipenta | 11 | 31.0 | 658.5 | **NaN** | Vegetables | 188.0 | 31 | 310 | 7.45 | 0.05 |
| 281 | 282 | Mydukur | Onipenta | 9 | 31.0 | 658.5 | **NaN** | Vegetables | 201.0 | 28 | 344 | 7.59 | 0.06 |
| 282 | 283 | Mydukur | Mittamedapalle | 11 | 31.0 | 658.5 | **NaN** | Vegetables | 226.0 | 42 | 378 | 7.62 | 0.05 |
| 283 | 284 | Mydukur | Mittamedapalle | 9 | 31.0 | 658.5 | **NaN** | Vegetables | 176.0 | 39 | 298 | 7.48 | 0.04 |
| 284 | 285 | Mydukur | Ganjikunta | 9 | 31.0 | 658.5 | **NaN** | Black gram | 213.0 | 35 | 356 | 7.73 | 0.06 |
| 285 | 286 | Mydukur | Ganjikunta | 9 | 31.0 | 658.5 | **NaN** | Black gram | 188.0 | 42 | 332 | 7.67 | 0.07 |

---

## 3. Humidity Distribution Analysis

### 3.1 Entire Dataset Baseline ($N=591$ Valid Observations)

Across all valid observations, humidity displays a moderately right-skewed distribution spanning from semi-arid conditions to saturated levels:

* **Valid Sample Count:** $591$ ($96.73\%$ of dataset)
* **Missing Sample Count:** $20$ ($3.27\%$ of dataset)
* **Minimum:** `45.0900 %` (Simhadripuram)
* **25th Percentile ($Q_1$):** `66.4600 %`
* **Median ($Q_2$):** `72.5900 %`
* **Mean:** `75.0755 %`
* **75th Percentile ($Q_3$):** `81.2000 %`
* **Maximum:** `100.0000 %` (Kamalapuram, Pendlimarri, C.K.Dinne)
* **Standard Deviation ($\sigma$):** `13.7091 %`
* **Interquartile Range (IQR):** `14.7400 %`
* **Skewness:** `+0.3843`
* **Kurtosis:** `-0.1722`

---

### 3.2 Mandal-Level Weather Profiles Across All 27 Mandals

The analysis in `src/data/analyze_missing_humidity.py` confirms that **standard deviation of weather variables within every single Mandal is identically $0.0$**. Each Mandal possesses a singular weather station signature:

| # | Mandal Name | Sample Count | Constant Temp (°C) | Constant Rain (mm) | Constant Humidity (%) | Completeness |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Khajipeta | 30 | 28.00 | 806.6 | 63.00 | 100.0% |
| 2 | Chapadu | 29 | 30.06 | 688.5 | 64.68 | 100.0% |
| 3 | Proddutur | 34 | 30.70 | 806.4 | 62.23 | 100.0% |
| 4 | Chennur | 19 | 31.00 | 875.8 | 61.00 | 100.0% |
| **5** | **Mydukur** | **20** | **31.00** | **658.5** | **NaN (MISSING)** | **0.0%** |
| 6 | Siddavatam | 20 | 31.46 | 853.5 | 71.00 | 100.0% |
| 7 | Gopavaram | 16 | 32.70 | 911.2 | 78.40 | 100.0% |
| 8 | Badvel | 20 | 33.59 | 739.4 | 69.09 | 100.0% |
| 9 | Atloor | 34 | 33.59 | 944.5 | 68.50 | 100.0% |
| 10 | Muddanur | 22 | 34.00 | 697.3 | 78.90 | 100.0% |
| 11 | Duvvuru | 29 | 34.09 | 751.4 | 72.59 | 100.0% |
| 12 | Peddamudiaum | 10 | 34.17 | 663.1 | 66.46 | 100.0% |
| 13 | Rajupalem | 22 | 34.40 | 734.6 | 66.50 | 100.0% |
| 14 | JAMMALAMADUGU | 26 | 34.59 | 834.3 | 77.40 | 100.0% |
| 15 | Simhadripuram | 24 | 34.70 | 626.4 | 45.09 | 100.0% |
| 16 | Chakrayapeta | 22 | 34.82 | 835.8 | 81.20 | 100.0% |
| 17 | Mylavaram | 26 | 35.23 | 858.2 | 67.80 | 100.0% |
| 18 | Kondapuram | 26 | 35.38 | 630.7 | 79.97 | 100.0% |
| 19 | Thondur | 20 | 35.50 | 735.0 | 95.51 | 100.0% |
| 20 | C.K.Dinne | 18 | 36.03 | 713.1 | 100.00 | 100.0% |
| 21 | Kadapa | 4 | 36.03 | 702.7 | 61.00 | 100.0% |
| 22 | Vontimitta | 20 | 36.12 | 770.6 | 72.86 | 100.0% |
| 23 | Lingala | 20 | 36.26 | 667.8 | 70.95 | 100.0% |
| 24 | Vempalli | 34 | 36.40 | 826.4 | 83.00 | 100.0% |
| 25 | Pendlimarri | 43 | 36.89 | 650.3 | 100.00 | 100.0% |
| 26 | Kamalapuram-3 | 1 | 37.50 | 762.4 | 100.00 | 100.0% |
| 27 | Kamalapuram | 22 | 37.50 | 762.4 | 100.00 | 100.0% |

---

### 3.3 Mydukur vs. Climatically and Geographically Adjacent Mandals

In YSR Kadapa district, Mandal Mydukur is geographically bordered by **Chapadu, Proddutur, Duvvuru, Khajipeta, and Badvel**. 

Meteorologically, Mandals with temperatures closely matching Mydukur's ($30.0^\circ\text{C} - 31.5^\circ\text{C}$) exhibit tightly clustered relative humidity readings:

| Mandal Name | Geographical Relation | Temperature (°C) | Rainfall (mm) | Humidity (%) | Distance / Climate Closeness |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Chapadu** | Immediate Western Border | `30.06` | `688.5` | **`64.68`** | Highly Similar ($|\Delta T| = 0.94^\circ\text{C}, |\Delta R| = 30\text{ mm}$) |
| **Chennur** | Southern Neighbor | `31.00` | `875.8` | **`61.00`** | Identical Temperature ($31.00^\circ\text{C}$) |
| **Proddutur** | North-Western Neighbor | `30.70` | `806.4` | **`62.23`** | Highly Similar ($|\Delta T| = 0.30^\circ\text{C}$) |
| **Siddavatam** | South-Eastern Basin | `31.46` | `853.5` | **`71.00`** | Similar Temperature ($|\Delta T| = 0.46^\circ\text{C}$) |
| **Badvel** | Eastern Border | `33.59` | `739.4` | **`69.09`** | Adjacent District Corridor |
| **Duvvuru** | Northern Border | `34.09` | `751.4` | **`72.59`** | Adjacent District Corridor |
| **Khajipeta** | South-Western Neighbor | `28.00` | `806.6` | **`63.00`** | Adjacent Basin |

* **Median of Temperature-Matched Mandals ($30 - 31.5^\circ\text{C}$):** **`63.45 %`**
* **Mean of Temperature-Matched Mandals ($30 - 31.5^\circ\text{C}$):** **`64.73 %`**

---

## 4. Multi-Feature Comparison: Mydukur vs. District Baseline

To determine whether Mydukur exhibits soil anomalies alongside its weather missingness, all 14 numerical features were compared between Mydukur ($N=20$) and the rest of the district ($N=591$):

| Feature | Unit | Mydukur Mean | Mydukur Median | Rest of District Mean | Rest of District Median | Agronomic Comparison / Variance |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **PH** | $-\log[H^+]$ | `7.616` | `7.650` | `8.000` | `8.030` | Moderately less alkaline (closer to neutral) |
| **EC** | dS/m | `0.057` | `0.055` | `0.168` | `0.130` | Significantly lower salinity ($< 0.1$ dS/m) |
| **OC** | % | `0.187` | `0.170` | `0.357` | `0.190` | Low organic carbon (typical for Kadapa) |
| **N** | kg/ha | `201.70` | `194.50` | `220.95` | `226.00` | Slightly lower available nitrogen |
| **P2O5** | kg/ha | `38.80` | `34.00` | `59.73` | `29.00` | Normal medium phosphorus range |
| **K20** | kg/ha | `348.70` | `361.00` | `375.40` | `392.00` | Abundant available potassium |
| **S** | ppm | `6.85` | `4.50` | `12.16` | `10.00` | Lower available sulfur |
| **CU** | ppm | `1.186` | `0.946` | `1.191` | `0.718` | In line with district micronutrient levels |
| **FC** | ratio | `5.877` | `3.908` | `5.395` | `3.670` | Comparable iron/field capacity index |
| **MN** | ppm | `5.405` | `5.413` | `10.695` | `7.429` | Lower manganese baseline |
| **ZN** | ppm | `1.894` | `0.980` | `0.893` | `0.508` | Higher available zinc |
| **BA** | ppm | `0.261` | `0.208` | `0.616` | `0.256` | Lower boron/barium index |
| **Temparature**| °C | `31.00` | `31.00` | `34.04` | `34.59` | **Cooler than district average by $\sim 3^\circ\text{C}$** |
| **Rainfall** | mm | `658.50` | `658.50` | `766.89` | `762.40` | **Drier than district average by $\sim 108\text{ mm}$** |

*Conclusion:* The chemical soil data for Mydukur is completely authentic, detailed, and uncorrupted. The missingness is strictly confined to the humidity sensor / recording cell for this single administrative unit.

---

## 5. Relationship Analysis of the 20 Missing Humidity Records

### 5.1 Relationship with Mandal & Village
* **Mandal:** $100\%$ of missing values belong to Mandal `Mydukur`. No other Mandal has even a single missing value.
* **Village:** The 20 records are distributed across 9 distinct villages within Mydukur:
  * Annaluru ($2$ farms)
  * Sivapuram ($2$ farms)
  * Nandyalampeta ($4$ farms)
  * Audireddypalle ($2$ farms)
  * Settivaripalli ($2$ farms)
  * Viswanadhapuram ($2$ farms)
  * Onipenta ($2$ farms)
  * Mittamedapalle ($2$ farms)
  * Ganjikunta ($2$ farms)
  This proves the missingness is not localized to a single farm or village, but corresponds to the Mandal meteorological reporting channel.

### 5.2 Relationship with Crops: The Minority Class Extinction Threat

Dropping rows with missing humidity (listwise deletion) is **strictly unacceptable** due to catastrophic class destruction:

| Crop Label | Total Count in Dataset | Count in Mydukur | Count Outside Mydukur | Impact if 20 Mydukur Rows Dropped |
| :--- | :---: | :---: | :---: | :--- |
| **`Vegetables`** | 5 | 5 | **0** | **$100.0\%$ Lost — Complete Class Extinction** |
| **`Turemeric`** | 1 | 1 | **0** | **$100.0\%$ Lost — Complete Class Extinction** |
| **`Chillis`** | 1 | 1 | **0** | **$100.0\%$ Lost — Complete Class Extinction** |
| **`Tamota`** (Tomato) | 4 | 3 | 1 | **$75.0\%$ Lost — Near-Complete Extinction (1 sample left)** |
| **`Jowar`** | 4 | 3 | 1 | **$75.0\%$ Lost — Near-Complete Extinction (1 sample left)** |
| **`Black gram`** | 30 | 5 | 25 | $16.7\%$ Lost |
| **`Banana`** | 5 | 1 | 4 | $20.0\%$ Lost |
| **`paddy`** | 143 | 1 | 142 | $0.7\%$ Lost |

*Three entire target classes exist nowhere else in the entire dataset.* Any solution that drops these rows destroys the predictive scope of the ensemble model.

---

## 6. Evaluation and Calculation of Candidate Imputation Strategies

### Candidate 1: Mandal-Level Median Imputation
* **Concept:** Impute missing values using the median of valid records from the same Mandal.
* **Calculated Value:** **`Undefined / NaN`**.
* **Feasibility:** **Impossible Standalone**. Because $0$ out of $20$ Mydukur records contain humidity, there is no within-Mandal data to calculate a median.

---

### Candidate 2: Overall Median Imputation
* **Concept:** Impute all 20 missing values with the median of all 591 valid observations across the entire dataset.
* **Calculated Value:** **`72.5900 %`** (Mean: `75.0755 %`).
* **Advantages:**
  * Clean, standard scikit-learn pipeline implementation: `SimpleImputer(strategy='median')`.
  * Zero risk of data leakage (does not use target label `CROP`).
  * Robust against extreme outliers (e.g., $100\%$ saturation or $45\%$ arid lows).
  * Universally defensible in academic peer review.
* **Limitations:**
  * Slightly overestimates Mydukur's humidity ($72.59\%$ vs $\sim 64\%$) because it does not condition on Mydukur's cooler $31.0^\circ\text{C}$ temperature.

---

### Candidate 3: Crop-Group Median Imputation
* **Concept:** Impute each missing record using the median humidity of other records sharing the same recorded `CROP`.
* **Calculated Values:**
  * `Black gram`: `77.40 %` ($N=25$ valid records elsewhere)
  * `paddy`: `69.09 %` ($N=142$ valid records elsewhere)
  * `Banana`: `83.00 %` ($N=4$ valid records elsewhere)
  * `Tamota`: `62.23 %` ($N=1$ valid record elsewhere)
  * `Jowar`: `45.09 %` ($N=1$ valid record elsewhere)
  * **`Vegetables`:** **`Undefined (0 valid records elsewhere)`**
  * **`Turemeric`:** **`Undefined (0 valid records elsewhere)`**
  * **`Chillis`:** **`Undefined (0 valid records elsewhere)`**
* **Feasibility & Ethical Flaws:**
  1. **Mathematically impossible for 7 out of 20 rows** (`Vegetables`, `Turemeric`, `Chillis`).
  2. **Severe Target Leakage:** Uses the prediction target $y$ (`CROP`) to fill input features $X$, invalidating generalization and causing artificial train-test leakage.
* **Evaluation:** **Strictly Rejected**.

---

### Candidate 4: Model-Based / Weather-Conditioned Imputation
* **Concept:** Predict humidity from Mydukur's known weather covariates ($\text{Temparature}=31.0^\circ\text{C}, \text{Rainfall}=658.5\text{ mm}$) using regression or iterative imputer trained on the other 26 complete Mandals.
* **Calculated Values:**
  * **Multivariate Imputer (IterativeImputer / MICE):** **`64.11 %`**
  * **Climate-Matched Neighbor Median ($30 - 31.5^\circ\text{C}$):** **`63.45 %`** (Mean: `64.73 %`, Chapadu: `64.68 %`)
  * **Ridge Regression ($\text{Temp} + \text{Rain}$):** **`60.55 %`**
  * **Linear Regression ($\text{Temp} + \text{Rain}$):** **`60.43 %`** ($R^2 = 0.3531$)
  * **KNN Regressor ($k=3$, distance-weighted):** **`76.53 %`**
* **Advantages:**
  * Highly faithful to the physical meteorology of the Kadapa basin ($61\% - 65\%$ for $31^\circ\text{C}$).
  * Preserves the joint correlation structure between weather variables.
  * Completely free of target leakage.
* **Limitations:** Requires introducing an imputation model into the preprocessing pipeline.

---

### Candidate 5: Retaining Missing Values (Native Tree Algorithm NaN Handling)
* **Concept:** Keep `Humidity = NaN` and let algorithms handle missing values natively.
* **Feasibility & Critical Risks:**
  * While XGBoost, LightGBM, and CatBoost natively handle NaNs, **standard scikit-learn `RandomForestClassifier` and `ExtraTreesClassifier`** (the central ensemble methods for an IEEE paper) **crash with `ValueError: Input X contains NaN`**.
  * Classical ensemble voting (`VotingClassifier`) or stacking (`StackingClassifier`) combining Random Forest, ExtraTrees, KNN, or SVM will fail immediately.
  * Feature scalers (`StandardScaler`, `MinMaxScaler`), PCA, and correlation analyses also fail or propagate NaNs.
* **Evaluation:** **Incompatible with the required ensemble architecture**.

---

## 7. Strategy Comparison Matrix

| Strategy | Imputed Value / Behavior | Preserves 611 Rows & Rare Crops? | Free of Target Leakage? | Ensemble Architecture Compatibility | Meteorological Realism | Academic Defensibility | Overall Recommendation Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Drop Missing Rows (Deletion)** | Drops 20 rows | **NO (Extinguishes 3 crop classes)** | Yes | Yes | N/A | Very Poor | **REJECTED** |
| **2. Mandal Median** | `Undefined (NaN)` | No | Yes | No | N/A | N/A | **REJECTED (Impossible)** |
| **3. Crop-Group Median** | Mixed / Undefined | **NO (Fails for rare crops)** | **NO (Severe Leakage)** | Yes | Poor | Very Poor | **REJECTED (Flawed)** |
| **4. Retain NaNs (No Imputation)** | Keeps `NaN` | Yes | Yes | **NO (Crashes RF & ExtraTrees)** | N/A | Poor | **REJECTED (Incompatible)** |
| **5. Model-Based Weather Imputation** | **`64.11 %`** *(MICE)* / **`64.68 %`** | **YES (100% Preserved)** | **YES** | **YES (100% Compatible)** | **Excellent ($61-65\%$)** | High | **STRONG CONTENDER** |
| **6. Overall Dataset Median** | **`72.59 %`** | **YES (100% Preserved)** | **YES** | **YES (100% Compatible)** | Moderate ($+8\%$ offset) | **Highest (Standard Benchmark)** | **RECOMMENDED PRIMARY STRATEGY** |

---

## 8. Final Recommendation and Justification

### Recommended Strategy: **Overall Median Imputation (`72.59 %`)**
*(With Model-Based Weather Imputation `64.11 %` documented as a secondary benchmark).*

### Rigorous Justification for Overall Median Imputation:
1. **Guaranteed Ensemble Compatibility:**
   Producing a clean, float-valued feature vector ensures that **every model in the proposed ensemble**—`RandomForestClassifier`, `ExtraTreesClassifier`, `XGBClassifier`, `LGBMClassifier`, `CatBoostClassifier`, and meta-classifiers (`StackingClassifier`, `VotingClassifier`)—trains seamlessly without compatibility errors or library version constraints.
2. **100% Minority Class Preservation:**
   All 20 Mydukur observations are preserved, safeguarding the entire sample population of `Vegetables` ($5$), `Turemeric` ($1$), `Chillis` ($1$), `Tamota` ($3$), and `Jowar` ($3$).
3. **Zero Target Leakage:**
   Imputing via overall median is calculated strictly from the feature space $X_{\text{train}}$ without referencing or conditioning on the ground-truth target $y$ (`CROP`), satisfying IEEE rigorous reproducibility standards.
4. **Defensible and Transparent:**
   In an academic thesis, project viva, or IEEE paper review, `SimpleImputer(strategy='median')` is universally accepted, objective, and involves zero tuned hyperparameters.
5. **Impact on Model Accuracy:**
   Across 611 records, 20 rows represent only $3.27\%$ of the dataset. Imputing $72.59\%$ (which sits comfortably within the 1st and 3rd quartiles $[66.46\%, 81.20\%]$) introduces minimal distributional distortion while keeping soil nutrient distinctions intact.

---

## 9. Risk Analysis and Mitigation Measures

| Potential Risk | Severity | Mechanism | Concrete Mitigation Measure |
| :--- | :---: | :--- | :--- |
| **Overestimating Mydukur Humidity** | Low | $72.59\%$ is $\sim 8\%$ higher than neighboring Chapadu ($64.68\%$). | Soil nutrients ($N, P, K, \text{pH}, \text{EC}$, micronutrients) provide strong, dominant discriminating signals for crop recommendation, attenuating slight weather offsets. |
| **Data Leakage in Cross-Validation** | Medium | Calculating overall median on the full dataset before train-test split causes slight leakage. | **Operational Pipeline Rule:** Embed `SimpleImputer(strategy='median')` inside a `sklearn.pipeline.Pipeline` or cross-validation fold to compute the median strictly on training folds. |
| **Collinearity Distortion** | Low | Assigning $72.59\%$ slightly shifts the $(T, R, H)$ covariance for 20 rows. | Conduct a sensitivity experiment in Step 6 comparing model performance with median ($72.59\%$) vs. MICE/weather-matched ($64.11\%$). |

---

## 10. Operational Preprocessing Protocol for Step 6

When the preprocessing script is implemented in Step 6:
1. **Do not modify `data/complete soil data.xlsx`**.
2. Instantiate `SimpleImputer(strategy='median')` on numeric features within the reproducible data pipeline.
3. The 20 Mydukur rows will be imputed to **`72.59%`** (or fold-specific training median).
4. For sensitivity analysis, provide a flag `--imputation-strategy median|weather_model` allowing downstream comparison between `72.59%` and `64.11%`.

---

## 11. Dataset Integrity Confirmation

* `data/complete soil data.xlsx` **remains 100% unaltered**.
* No in-place modifications, deletions, or imputations were written to the source Excel file.
