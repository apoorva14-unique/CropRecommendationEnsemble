# Humidity Missing-Value Analysis Report

**Document Version:** 1.0  
**Analysis Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/processed/genuine_agricultural_data.csv` (Untouched, Read-Only)  
**Status:** Strictly Exploratory — No dataset values have been imputed or deleted.

---

## 1. Executive Summary

This report delivers a thorough investigation into the **20 missing values in the `Humidity` column**—the only feature in the entire dataset with missing observations. A crucial structural finding is that weather parameters (Temperature, Rainfall, Humidity) were recorded at the **Mandal (sub-district) administrative level**, with each Mandal sharing identical weather measurements across all its farm samples. 

Critically, **100% of the 20 missing values belong to Mandal `Mydukur`**, and `Mydukur` contains **zero valid humidity observations**. Furthermore, several rare crop classes (`Vegetables`, `Tamota`, `Jowar`) are concentrated predominantly or exclusively within Mydukur. Dropping these 20 rows would cause severe class extinction.

---

## 2. Confirmation of the 20 Missing Humidity Records

* **Total Dataset Rows:** 611
* **Valid Humidity Records:** 591 ($96.73\%$)
* **Missing Humidity Records:** 20 ($3.27\%$)
* **Contiguity:** Spans consecutive row indices **266 through 285** (Serial Numbers `S.NO 267` to `286`).
* **Mandal Distribution:** Exactly 20 out of 20 missing records ($100\%$) are located in **Mandal `Mydukur`**.

### Complete Manifest of the 20 Missing Records

| Row Index | S.NO | Mandal Name | Village Name | Recorded Crop | Temperature (°C) | Rainfall (mm) | Humidity (%) |
| :---: | :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| 266 | 267 | Mydukur | Annaluru | paddy | 31.0 | 658.5 | **NaN** |
| 267 | 268 | Mydukur | Annaluru | Black gram | 31.0 | 658.5 | **NaN** |
| 268 | 269 | Mydukur | Sivapuram | Tamota | 31.0 | 658.5 | **NaN** |
| 269 | 270 | Mydukur | Sivapuram | Jowar | 31.0 | 658.5 | **NaN** |
| 270 | 271 | Mydukur | Nandyalampeta | Turemeric | 31.0 | 658.5 | **NaN** |
| 271 | 272 | Mydukur | Nandyalampeta | Black gram | 31.0 | 658.5 | **NaN** |
| 272 | 273 | Mydukur | Nandyalampeta | Black gram | 31.0 | 658.5 | **NaN** |
| 273 | 274 | Mydukur | Nandyalampeta | Vegetables | 31.0 | 658.5 | **NaN** |
| 274 | 275 | Mydukur | Audireddypalle | Chillis | 31.0 | 658.5 | **NaN** |
| 275 | 276 | Mydukur | Audireddypalle | Banana | 31.0 | 658.5 | **NaN** |
| 276 | 277 | Mydukur | Settivaripalli | Jowar | 31.0 | 658.5 | **NaN** |
| 277 | 278 | Mydukur | Settivaripalli | Jowar | 31.0 | 658.5 | **NaN** |
| 278 | 279 | Mydukur | Viswanadhapuram | Tamota | 31.0 | 658.5 | **NaN** |
| 279 | 280 | Mydukur | Viswanadhapuram | Tamota | 31.0 | 658.5 | **NaN** |
| 280 | 281 | Mydukur | Onipenta | Vegetables | 31.0 | 658.5 | **NaN** |
| 281 | 282 | Mydukur | Onipenta | Vegetables | 31.0 | 658.5 | **NaN** |
| 282 | 283 | Mydukur | Mittamedapalle | Vegetables | 31.0 | 658.5 | **NaN** |
| 283 | 284 | Mydukur | Mittamedapalle | Vegetables | 31.0 | 658.5 | **NaN** |
| 284 | 285 | Mydukur | Ganjikunta | Black gram | 31.0 | 658.5 | **NaN** |
| 285 | 286 | Mydukur | Ganjikunta | Black gram | 31.0 | 658.5 | **NaN** |

---

## 3. Statistical Calculations

* **Overall Dataset Humidity Mean:** **`75.0755 %`**
* **Overall Dataset Humidity Median:** **`72.5900 %`**
* **Overall Dataset Humidity Std Dev:** **`13.7091 %`**
* **Overall Dataset Humidity Range:** **`[45.09 %, 100.0 %]`**
* **Total Records in Mandal Mydukur:** **20**
* **Valid Humidity Records in Mandal Mydukur:** **0**
* **Mydukur Humidity Mean:** **`Undefined / NaN`** (Zero valid records exist in Mydukur)
* **Mydukur Humidity Median:** **`Undefined / NaN`** (Zero valid records exist in Mydukur)

---

## 4. Cross-Mandal Humidity Completeness Check

Every other Mandal in the Kadapa dataset exhibits **100% complete humidity measurements**:

| # | Mandal Name | Total Records | Valid Records | Missing Count | Completion Rate | Constant Temp (°C) | Constant Rain (mm) | Constant Humidity (%) |
| :-: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Atloor | 34 | 34 | 0 | 100.0% | 33.59 | 944.5 | 68.50 |
| 2 | Badvel | 20 | 20 | 0 | 100.0% | 33.59 | 739.4 | 69.09 |
| 3 | C.K.Dinne | 18 | 18 | 0 | 100.0% | 36.03 | 713.1 | 100.00 |
| 4 | Chakrayapeta | 22 | 22 | 0 | 100.0% | 34.82 | 835.8 | 81.20 |
| 5 | Chapadu | 29 | 29 | 0 | 100.0% | 30.06 | 688.5 | 64.68 |
| 6 | Chennur | 19 | 19 | 0 | 100.0% | 31.00 | 875.8 | 61.00 |
| 7 | Duvvuru | 29 | 29 | 0 | 100.0% | 34.09 | 751.4 | 72.59 |
| 8 | Gopavaram | 16 | 16 | 0 | 100.0% | 32.70 | 911.2 | 78.40 |
| 9 | JAMMALAMADUGU | 26 | 26 | 0 | 100.0% | 34.59 | 834.3 | 77.40 |
| 10 | Kadapa | 4 | 4 | 0 | 100.0% | 36.03 | 702.7 | 61.00 |
| 11 | Kamalapuram | 22 | 22 | 0 | 100.0% | 37.50 | 762.4 | 100.00 |
| 12 | Kamalapuram-3 | 1 | 1 | 0 | 100.0% | 37.50 | 762.4 | 100.00 |
| 13 | Khajipeta | 30 | 30 | 0 | 100.0% | 28.00 | 806.6 | 63.00 |
| 14 | Kondapuram | 26 | 26 | 0 | 100.0% | 35.38 | 630.7 | 79.97 |
| 15 | Lingala | 20 | 20 | 0 | 100.0% | 36.26 | 667.8 | 70.95 |
| 16 | Muddanur | 22 | 22 | 0 | 100.0% | 34.00 | 697.3 | 78.90 |
| **17** | **Mydukur** | **20** | **0** | **20** | **0.0%** | **31.00** | **658.5** | **MISSING** |
| 18 | Mylavaram | 26 | 26 | 0 | 100.0% | 35.23 | 858.2 | 67.80 |
| 19 | Peddamudiaum | 10 | 10 | 0 | 100.0% | 34.17 | 663.1 | 66.46 |
| 20 | Pendlimarri | 43 | 43 | 0 | 100.0% | 36.89 | 650.3 | 100.00 |
| 21 | Proddutur | 34 | 34 | 0 | 100.0% | 30.70 | 806.4 | 62.23 |
| 22 | Rajupalem | 22 | 22 | 0 | 100.0% | 34.40 | 734.6 | 66.50 |
| 23 | Siddavatam | 20 | 20 | 0 | 100.0% | 31.46 | 853.5 | 71.00 |
| 24 | Simhadripuram | 24 | 24 | 0 | 100.0% | 34.70 | 626.4 | 45.09 |
| 25 | Thondur | 20 | 20 | 0 | 100.0% | 35.50 | 735.0 | 95.51 |
| 26 | Vempalli | 34 | 34 | 0 | 100.0% | 36.40 | 826.4 | 83.00 |
| 27 | Vontimitta | 20 | 20 | 0 | 100.0% | 36.12 | 770.6 | 72.86 |

---

## 5. Critical Impact on Crop Class Representation

A pivotal discovery is the distribution of crops across the 20 Mydukur rows:

| Crop Label | Total Count in Dataset | Count in Mandal Mydukur | Count in All Other Mandals | Percentage Lost If Dropped |
| :--- | :---: | :---: | :---: | :---: |
| `Vegetables` | 5 | 5 | **0** | **100.0% (Complete Extinction)** |
| `Tamota` (Tomato) | 4 | 3 | **1** | **75.0%** |
| `Jowar` | 4 | 3 | **1** | **75.0%** |
| `Turemeric` | 1 | 1 | **0** | **100.0% (Complete Extinction)** |
| `Chillis` | 1 | 1 | **0** | **100.0% (Complete Extinction)** |
| `Black gram` | 30 | 5 | 25 | 16.7% |
| `Banana` | 5 | 1 | 4 | 20.0% |
| `paddy` | 143 | 1 | 142 | 0.7% |

*If rows are dropped, entire crop classes are permanently eliminated from the dataset, severely degrading model utility and minority class learning.*

---

## 6. Evaluation of Imputation & Handling Options

### Option 1: Dropping Rows (Listwise Deletion)
* **Mechanism:** Discard all 20 rows where `Humidity` is NaN, reducing the dataset from $N=611$ to $N=591$.
* **Advantages:** Avoids introducing synthetic or estimated weather data.
* **Disadvantages:**
  - Destroys 100% of the `Vegetables` class (all 5 samples are in Mydukur).
  - Destroys 75% of `Tamota` and 75% of `Jowar` samples.
  - Wipes out genuine, high-quality soil chemical measurements ($N, P, K, \text{pH}, \text{EC}$, micronutrients) for 20 farms.
* **Evaluation:** Highly damaging to class diversity and model training.

### Option 2: Overall Median Imputation
* **Mechanism:** Replace the 20 missing values with the median of all valid observations across Kadapa: **`72.59 %`**.
* **Advantages:**
  - Simple, robust against extreme values (like 100% or 45%), highly reproducible, and mathematically sound for a B.Tech project.
  - Fully preserves all 611 records and protects rare crop classes.
* **Disadvantages:** Assigns the county-wide median rather than reflecting Mydukur's specific thermal and precipitation conditions (31.0°C and 658.5 mm).
* **Evaluation:** Strong, practical, and defensively justifiable baseline.

### Option 3: Climate-Matched / Neighboring Mandal Median Imputation
* **Mechanism:** Since weather is recorded at the Mandal weather station level, impute humidity using the median/mean of geographically adjacent or climatically similar Mandals in Kadapa that share similar Temperature ($31.0^\circ\text{C}$) and Rainfall ($658.5\text{ mm}$):
  * *Chapadu* ($\text{Temp}=30.06^\circ\text{C}, \text{Rain}=688.5\text{ mm}$): Humidity = **`64.68%`**
  * *Chennur* ($\text{Temp}=31.00^\circ\text{C}, \text{Rain}=875.8\text{ mm}$): Humidity = **`61.00%`**
  * *Proddutur* ($\text{Temp}=30.70^\circ\text{C}, \text{Rain}=806.4\text{ mm}$): Humidity = **`62.23%`**
  * *Khajipeta* ($\text{Temp}=28.00^\circ\text{C}, \text{Rain}=806.6\text{ mm}$): Humidity = **`63.00%`**
  * *Average of Climate Neighbors:* **`~62.7% – 64.7%`**.
* **Advantages:** Agronomically and meteorologically more realistic than the county-wide median.
* **Disadvantages:** Requires defining a neighbor-matching rule.
* **Evaluation:** Very strong domain-grounded alternative.

### Option 4: Model-Based Imputation (Regression / KNN / IterativeImputer)
* **Mechanism:** Train a lightweight regression model (e.g. Ridge Regression or KNN with $k=3$) to predict `Humidity` as a function of `Temperature`, `Rainfall`, and geographic coordinates/Mandal encodings from the other 26 complete Mandals.
* **Advantages:** Captures mathematical inter-dependencies among weather variables.
* **Disadvantages:** Introduces algorithmic complexity for a single feature missing across only 20 records.
* **Evaluation:** Good for advanced research, but may be over-engineered compared to direct median or climate-matching.

---

## 7. Recommended Defensible Option

### Primary Recommendation: **Overall Median Imputation (`72.59%`)** (or **Climate-Matched Median `64.68%`**)
1. **Preserves Sample Size and Minority Crops:** Retains all 611 records, preventing the catastrophic extinction of `Vegetables`, `Tamota`, and `Jowar`.
2. **Defensible and Transparent:** Transparent and easily defended in a project viva/defense, adhering strictly to scikit-learn's standard `SimpleImputer(strategy='median')`.
3. **No Target Leakage:** Does not use the target `CROP` variable for imputation.

*(Note: Per instructions, no imputation has been applied to any dataset file at this stage.)*
