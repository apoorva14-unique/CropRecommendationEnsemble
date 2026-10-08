# Step 4: Verification of Numeric Anomalies Report

**Document Version:** 1.0  
**Verification Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/complete soil data.xlsx` (Untouched, Read-Only)  
**Execution Script:** `src/data/verify_numeric_anomalies.py`  
**Diagnostic Artifact:** `reports/figures/numeric_anomalies_verification.png`  
**Status:** Strictly Exploratory & Analytical — **No dataset files have been modified, overwritten, or imputed.**

---

## 1. Executive Summary

During Step 1 dataset inspection, four specific records across numerical columns were detected to contain malformed string values rather than standard floating-point numbers. Because automatic string-to-float coercion in standard machine learning pipelines either silently introduces `NaN` values or drops valid records, this investigation conducts a disciplined, reproducible forensic audit of all four anomalies.

### Summary Inventory of Identified Anomalies

| # | Column Flagged | Row Index (0-based) | S.NO | Raw Malformed Value | Mandal Name | Village Name | Recorded Crop | Anomaly Typology |
| :-: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | `EC` | 244 | 245 | `'0..07'` | Vempalli | Vempalli-7 | Grownut | Double decimal point keystroke typo |
| **2** | `FC` | 241 | 242 | `'2..956'` | Vempalli | Vempalli-5 | Grownut | Double decimal point keystroke typo |
| **3** | `MN` | 54 | 55 | `'1.13.79'` | Simhadripuram | Kasanur | sunflower | Multi-decimal segmented string (Ambiguous) |
| **4** | `BA` | 228 | 229 | `'0..16'` | Lingala | Peddakudala | Black Gram | Double decimal point keystroke typo |

Each record is analyzed against surrounding observations, local administrative unit (Mandal and Village) baselines, soil type context, crop nutrient standards, and global dataset distributions.

---

## 2. Complete Row Displays for All Four Flagged Observations

Below are the complete 20 genuine agricultural feature values for each flagged row, extracted directly from [complete soil data.xlsx](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/complete%20soil%20data.xlsx):

| Feature / Attribute | S.NO 245 (`EC`) | S.NO 242 (`FC`) | S.NO 55 (`MN`) | S.NO 229 (`BA`) |
| :--- | :---: | :---: | :---: | :---: |
| **S.NO** | 245 | 242 | 55 | 229 |
| **MANDAL NAME** | Vempalli | Vempalli | Simhadripuram | Lingala |
| **VILLAGE NAME** | Vempalli-7 | Vempalli-5 | Kasanur | Peddakudala |
| **SOIL TYPE** | 1 | 1 | 3 | 1 |
| **PH** | 8.23 | 8.32 | 8.25 | 8.25 |
| **EC** | **`0..07`** *(Flagged)* | 0.05 | 0.12 | 0.33 |
| **OC** | 0.19 | 0.07 | 0.03 | 0.11 |
| **N** | 301.0 | 163.0 | 213.0 | 226.0 |
| **P2O5** | 36 | 50 | 9 | 14 |
| **K20** | 338 | 527 | 425 | 459 |
| **S** | 4 | 14 | 16 | 19 |
| **CU** | 0.144 | 0.24 | 0.466 | 0.144 |
| **FC** | 2.538 | **`2..956`** *(Flagged)* | 1.022 | 2.716 |
| **MN** | 3.484 | 6.884 | **`1.13.79`** *(Flagged)* | 6.93 |
| **ZN** | 0.802 | 0.152 | 1.042 | 0.152 |
| **BA** | 4.16 | 0.256 | 2.78 | **`0..16`** *(Flagged)* |
| **Temparature** | 36.4 | 36.4 | 34.7 | 36.26 |
| **Humidity** | 83.0 | 83.0 | 45.09 | 70.95 |
| **Rainfall** | 826.4 | 826.4 | 626.4 | 667.8 |
| **CROP** | Grownut | Grownut | sunflower | Black Gram |

*(Note: Raw Excel column header for Temperature is spelled `'Temparature'`)*.

---

## 3. Anomaly 1 — Electrical Conductivity (`EC`) at S.NO 245

### 3.1 Context and Surrounding Records

Row index 244 (S.NO 245) represents a groundnut field in Village Vempalli-7, Mandal Vempalli, with Soil Type 1.

| Row Index | S.NO | Mandal Name | Village Name | Soil Type | EC Raw Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 240 | 241 | Vempalli | Vempalli-5 | 1 | 0.06 | 8.27 | Grownut |
| 241 | 242 | Vempalli | Vempalli-5 | 1 | 0.05 | 8.32 | Grownut |
| 242 | 243 | Vempalli | Vempalli-6 | 1 | 0.07 | 8.29 | cotton |
| 243 | 244 | Vempalli | Vempalli-6 | 1 | 0.09 | 8.32 | cotton |
| **244** | **245** | **Vempalli** | **Vempalli-7** | **1** | **`0..07`** | **8.23** | **Grownut** |
| 245 | 246 | Vempalli | Vempalli-7 | 1 | 0.08 | 8.25 | Banana |
| 246 | 247 | Vempalli | Vempalli-8 | 4 | 0.15 | 8.47 | Grownut |
| 247 | 248 | Vempalli | Vempalli-8 | 1 | 0.11 | 8.35 | Grownut |
| 248 | 249 | Vempalli | Idupulapaya-1 | 1 | 0.05 | 8.52 | Grownut |

### 3.2 Statistical Comparison

When temporarily coercing the single malformed string to NaN:

* **Global Dataset Baseline ($N=610$):**
  * Minimum: `0.0050` dS/m
  * 25th Percentile ($Q_1$): `0.0700` dS/m
  * Median ($Q_2$): `0.1200` dS/m
  * Mean: `0.1644` dS/m
  * 75th Percentile ($Q_3$): `0.2000` dS/m
  * Maximum: `8.1800` dS/m
  * Standard Deviation: `0.3500` dS/m
  * Interquartile Range (IQR): `0.1300` dS/m
* **Mandal Vempalli Baseline ($N=33$ valid):**
  * Minimum: `0.0100` dS/m
  * 25th Percentile ($Q_1$): `0.0700` dS/m
  * Median ($Q_2$): `0.0900` dS/m
  * Mean: `0.1133` dS/m
  * 75th Percentile ($Q_3$): `0.1400` dS/m
  * Maximum: `0.3700` dS/m
  * Standard Deviation: `0.0764` dS/m
* **Village Vempalli-7 Context ($N=1$ other):**
  * S.NO 246 has an EC value of exactly `0.08` dS/m.

### 3.3 Evaluation of Interpretations

1. **Typographical Error (`0.07`):**
   * The operator pressed the period key twice consecutively (`0..07`), an extremely common numpad double-tap error.
   * A value of `0.07` is identical to S.NO 243 (`0.07`), adjacent to S.NO 244 (`0.09`), and sits directly next to S.NO 246 (`0.08` in the exact same village).
   * It exactly equals the 25th percentile of the Mandal distribution ($Q_1 = 0.0700$).

### 3.4 Verification Determination

* **Recommended Treatment:** Parse as `0.07`.
* **Confidence Level:** **Very High (>99%)**.
* **External/Source Verification Required:** **No**. The typo is syntactically unambiguous and mathematically consistent with all local and global distributions.

---

## 4. Anomaly 2 — Field Capacity / Iron Index (`FC`) at S.NO 242

### 4.1 Context and Surrounding Records

Row index 241 (S.NO 242) represents a groundnut field in Village Vempalli-5, Mandal Vempalli, with Soil Type 1.

| Row Index | S.NO | Mandal Name | Village Name | Soil Type | FC Raw Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 237 | 238 | Vempalli | Vempalli-4 | 3 | 1.820 | 8.25 | Banana |
| 238 | 239 | Vempalli | Vempalli-4 | 1 | 2.538 | 8.21 | Grownut |
| 239 | 240 | Vempalli | Vempalli-4 | 1 | 1.034 | 8.30 | Banana |
| 240 | 241 | Vempalli | Vempalli-5 | 1 | 0.776 | 8.27 | Grownut |
| **241** | **242** | **Vempalli** | **Vempalli-5** | **1** | **`2..956`** | **8.32** | **Grownut** |
| 242 | 243 | Vempalli | Vempalli-6 | 1 | 3.140 | 8.29 | cotton |
| 243 | 244 | Vempalli | Vempalli-6 | 1 | 3.254 | 8.32 | cotton |
| 244 | 245 | Vempalli | Vempalli-7 | 1 | 2.538 | 8.23 | Grownut |
| 245 | 246 | Vempalli | Vempalli-7 | 1 | 3.490 | 8.25 | Banana |

### 4.2 Statistical Comparison

When temporarily coercing the single malformed string to NaN:

* **Global Dataset Baseline ($N=610$):**
  * Minimum: `0.0260`
  * 25th Percentile ($Q_1$): `1.9100`
  * Median ($Q_2$): `3.6990`
  * Mean: `5.4104`
  * 75th Percentile ($Q_3$): `6.7295`
  * Maximum: `42.9800`
  * Standard Deviation: `5.2656`
  * Interquartile Range (IQR): `4.8195`
* **Mandal Vempalli Baseline ($N=33$ valid):**
  * Minimum: `0.7760`
  * 25th Percentile ($Q_1$): `1.8200`
  * Median ($Q_2$): `2.3580`
  * Mean: `2.8793`
  * 75th Percentile ($Q_3$): `3.2540`
  * Maximum: `6.2380`
  * Standard Deviation: `1.6897`
  * Interquartile Range (IQR): `1.4340`
* **Village Vempalli-5 Context ($N=1$ other):**
  * S.NO 241 has an FC value of `0.776`.

### 4.3 Evaluation of Interpretations

1. **Typographical Error (`2.956`):**
   * The operator pressed the period key twice between integer digit `2` and decimal portion `956` (`2..956`).
   * A value of `2.956` preserves the 3-decimal precision universally present across Vempalli records (`2.538`, `1.034`, `0.776`, `3.140`, `3.254`, `3.490`).
   * `2.956` lies comfortably within Mandal Vempalli's interquartile range ($[1.8200, 3.2540]$) and is within $0.08$ of the Mandal mean ($2.8793$).

### 4.4 Verification Determination

* **Recommended Treatment:** Parse as `2.956`.
* **Confidence Level:** **Very High (>99%)**.
* **External/Source Verification Required:** **No**. Unambiguous syntactic typo matching surrounding precision and distribution.

---

## 5. Anomaly 3 — Manganese (`MN`) at S.NO 55 — Special Deep Investigation

### 5.1 Context and Surrounding Records

Row index 54 (S.NO 55) represents a sunflower crop sample in Village Kasanur, Mandal Simhadripuram, on Soil Type 3.

| Row Index | S.NO | Mandal Name | Village Name | Soil Type | MN Raw Value | Cu (ppm) | Zn (ppm) | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| 49 | 50 | Simhadripuram | A.K,Guduru | 1 | 0.004 | 0.152 | 0.302 | Grownut |
| 50 | 51 | Simhadripuram | Balapanur | 3 | 0.516 | 0.214 | 0.506 | sweet orange |
| 51 | 52 | Simhadripuram | Balapanur | 3 | 3.184 | 0.026 | 0.592 | Black gram |
| 52 | 53 | Simhadripuram | Himakuntla | 3 | 2.014 | 0.278 | 1.140 | Sweet orange |
| 53 | 54 | Simhadripuram | Himakuntla | 3 | 1.174 | 0.026 | 1.128 | grownut |
| **54** | **55** | **Simhadripuram** | **Kasanur** | **3** | **`1.13.79`** | **0.466** | **1.042** | **sunflower** |
| 55 | 56 | Simhadripuram | Kasanur | 3 | 5.012 | 0.120 | 0.312 | grownut |
| 56 | 57 | Simhadripuram | Lomada | 3 | 1.138 | 0.120 | 0.452 | sweet orange |
| 57 | 58 | Simhadripuram | Lomada | 1 | 1.394 | 0.058 | 1.000 | grownut |
| 58 | 59 | Simhadripuram | Simhadripuram-1 | 1 | 1.722 | 0.120 | 0.508 | black gram |
| 59 | 60 | Simhadripuram | Simhadripuram-1 | 1 | 3.916 | 0.026 | 0.838 | sunflower |

### 5.2 Multi-Level Statistical Baselines

* **Global Dataset Baseline ($N=610$):**
  * Minimum: `0.0000` ppm
  * 25th Percentile ($Q_1$): `3.5800` ppm
  * Median ($Q_2$): `7.1820` ppm
  * Mean: `10.5211` ppm
  * 75th Percentile ($Q_3$): `14.1875` ppm
  * Maximum: `52.3200` ppm
  * Standard Deviation: `9.9720` ppm
* **Mandal Simhadripuram Baseline ($N=23$ valid):**
  * Minimum: `0.0040` ppm
  * 25th Percentile ($Q_1$): `1.2650` ppm
  * Median ($Q_2$): `2.0140` ppm
  * Mean: `2.4926` ppm
  * 75th Percentile ($Q_3$): `3.6050` ppm
  * Maximum: `6.9140` ppm (S.NO 64)
  * Standard Deviation: `1.6859` ppm
  * Interquartile Range (IQR): `2.3400` ppm
  * *Distribution Characteristics:* Simhadripuram has the second-lowest available manganese baseline in the entire district. 22 out of 23 records are below `5.02` ppm.
* **Soil Type 3 within Simhadripuram ($N=9$ valid):**
  * Minimum: `0.5160` ppm, Median: `2.0140` ppm, Mean: `2.5060` ppm, Maximum: `5.0120` ppm.
* **Sunflower Crop Baseline in Simhadripuram ($N=4$ other records):**
  * Observations: `[2.014, 3.916, 4.136, 6.914]`
  * Median: `4.0260` ppm, Mean: `4.2450` ppm.
* **Sunflower Crop Baseline Globally ($N=12$ other records):**
  * Range: $[0.588, 10.970]$, Median: `4.0260` ppm, Mean: `4.4795` ppm.

---

### 5.3 In-Depth Investigation: Plausibility of Candidate Interpretations

Unlike simple double-dot errors (`..`), the string `'1.13.79'` has non-adjacent decimal points separating three distinct digit segments: `['1', '13', '79']`. The digits in sequence are `1-1-3-7-9`.

```
Raw String:  1  .  1  3  .  7  9
             │     └───┘     └───┘
          Segment 1 Segment 2 Segment 3
```

We evaluate the plausibility of all candidate interpretations using local agronomic context, distribution z-scores, and keyboard layout mechanics:

#### Candidate A: `1.1379` (or rounded `1.138`)

* **Typographical Hypothesis:** The operator entered `1.13`, stopped or hesitated, and accidentally hit the period key before typing `79`. Alternatively, the operator typed on a numpad where the `.` key was struck twice between segment pairs.
* **Agronomic & Statistical Evidence:**
  * **Direct Row Comparison:** At S.NO 57 (just two rows below S.NO 55, also in Mandal Simhadripuram, and also with Soil Type 3), the recorded MN value is exactly **`1.138`**. If `1.1379` is rounded to standard 3-decimal lab precision, it is identically **`1.138`**!
  * **Neighbor Row Comparison:** At S.NO 54 (one row before S.NO 55, also Soil Type 3), MN is `1.174`.
  * **Mandal Z-Score:** $z = \frac{1.1379 - 2.4926}{1.6859} = -0.80$. This sits comfortably within 1 standard deviation of the Simhadripuram mean.
  * **Soil Type 3 Range:** Fits well inside the Soil Type 3 range for Simhadripuram ($[0.516, 5.012]$).
  * **Sunflower Crop Z-Score:** $z = -1.54$ in Simhadripuram, $z = -1.17$ globally. Completely within natural biological variation for sunflower soils.

#### Candidate B: `11.379`

* **Typographical Hypothesis:** The intended measurement was `11.379`. The operator hit the decimal point prematurely after the first `1` rather than after `11` (`1.13.79` instead of `11.379`).
* **Agronomic & Statistical Evidence:**
  * **Global Mean Alignment:** Globally across all 610 records, the dataset mean is `10.5211` ppm ($z = +0.09$ globally). At a glance, `11.379` looks typical of the global dataset.
  * **Local Inconsistency (Extreme Outlier):** In Mandal Simhadripuram, the highest recorded MN out of all 23 valid observations is `6.914` ppm. If S.NO 55 were `11.379`, its local z-score would be:
    $$z = \frac{11.379 - 2.4926}{1.6859} = +5.27$$
    A $z$-score of $+5.27$ represents an extreme statistical outlier (local probability $p < 10^{-6}$).
  * **Soil Type 3 in Simhadripuram:** The maximum observed value is `5.012` ppm. `11.379` would be more than $2.27\times$ higher than any other Soil Type 3 observation in the entire Mandal.
  * **Sunflower in Simhadripuram:** The local sunflower mean is `4.245` ppm ($z = +3.53$).

#### Candidate C: `1.13`

* **Typographical Hypothesis:** The operator entered `1.13`, and `.79` was an inadvertent appended fragment.
* **Agronomic & Statistical Evidence:**
  * Statistically almost identical to Candidate A ($z = -0.81$ locally).
  * However, discarding the digits `7` and `9` without justification is less plausible than recognizing `1.1379` as an extra decimal separator error.

#### Candidate D: `13.79`

* **Typographical Hypothesis:** The leading `1.` was an accidental keystroke before typing `13.79`.
* **Agronomic & Statistical Evidence:**
  * Local $z$-score in Simhadripuram would be $+6.70$ (drastic local outlier).

#### Candidate E: Robust Local Imputation (`2.014` or `4.026`)

* If we treat `1.13.79` as an unresolvable corrupted entry in the absence of the physical lab logbook, statistical imputation using the **Mandal Median (`2.014`)** or **Crop-in-Mandal Median (`4.026`)** avoids introducing either positive or negative bias.

---

### 5.4 Summary Comparison of MN Candidates

| Candidate Interpretation | Value | Simhadripuram $z$-Score | Global $z$-Score | Simhadripuram Range $[0.004, 6.914]$ | Alignment with S.NO 57 (`1.138`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Candidate A (`1.1379` / `1.138`)** | `1.1379` | **$-0.80$** | $-0.94$ | **Within Range (Plausible)** | **Exact Match upon 3-decimal rounding** |
| **Candidate B (`11.379`)** | `11.379` | **$+5.27$** | $+0.09$ | **Severe Local Outlier ($>1.6\times$ max)** | No match |
| **Candidate C (`1.13`)** | `1.13` | $-0.81$ | $-0.94$ | Within Range | Truncates valid digits |
| **Candidate D (`13.79`)** | `13.79` | $+6.70$ | $+0.33$ | Extreme Local Outlier ($>2\times$ max) | No match |
| **Candidate E (Mandal Median)** | `2.014` | $-0.28$ | $-0.85$ | Within Range (Central) | Neutral imputation |

### 5.5 Verification Determination for MN

* **Recommended Treatment:**
  * **Primary Technical Recommendation:** Replace with **`1.138`** (or `1.1379`). The proximity to S.NO 57 (`1.138` in the same Mandal and Soil Type), the natural 3-decimal rounding of `1.1379`, and the local $z$-score of $-0.80$ make this overwhelmingly more probable than `11.379` ($z = +5.27$).
  * **Fallback / Conservative Treatment:** Impute with **Simhadripuram Mandal Median (`2.014`)** if strict zero-inference policy is enforced.
* **Confidence Level:** **Moderate (75% for `1.138`, 20% for `11.379`, 5% other)**.
* **External/Source Verification Required:** **Yes**. Because two structurally possible numeric interpretations exist (`1.1379` vs `11.379`), formal verification against the original Kadapa district laboratory register / Soil Health Card source logbook is strongly advised before permanent canonical dataset publication.

---

## 6. Anomaly 4 — Boron / Barium Index (`BA`) at S.NO 229

### 6.1 Context and Surrounding Records

Row index 228 (S.NO 229) represents a black gram crop field in Village Peddakudala, Mandal Lingala, with Soil Type 1.

| Row Index | S.NO | Mandal Name | Village Name | Soil Type | BA Raw Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 223 | 224 | Lingala | Peddakudala | 4 | 0.160 | 8.05 | Black Gram |
| 224 | 225 | Lingala | Peddakudala | 9 | 0.256 | 8.01 | Black Gram |
| 225 | 226 | Lingala | Peddakudala | 1 | 0.416 | 8.09 | Black Gram |
| 226 | 227 | Lingala | Peddakudala | 1 | 0.192 | 8.09 | Black Gram |
| 227 | 228 | Lingala | Peddakudala | 1 | 0.384 | 8.12 | Black Gram |
| **228** | **229** | **Lingala** | **Peddakudala** | **1** | **`0..16`** | **8.25** | **Black Gram** |
| 229 | 230 | Lingala | Peddakudala | 1 | 0.128 | 8.29 | Black Gram |
| 230 | 231 | Lingala | Peddakudala | 1 | 0.096 | 8.21 | Black Gram |
| 231 | 232 | Lingala | Peddakudala | 1 | 0.352 | 8.24 | Black Gram |
| 232 | 233 | Vempalli | Vempalli-1 | 1 | 0.256 | 8.32 | Grownut |

### 6.2 Statistical Comparison

When temporarily coercing the single malformed string to NaN:

* **Global Dataset Baseline ($N=610$):**
  * Minimum: `0.0190` ppm
  * 25th Percentile ($Q_1$): `0.1920` ppm
  * Median ($Q_2$): `0.2560` ppm
  * Mean: `0.6044` ppm
  * 75th Percentile ($Q_3$): `0.4160` ppm
  * Maximum: `96.0000` ppm
  * Standard Deviation: `3.9318` ppm
  * Interquartile Range (IQR): `0.2240` ppm
* **Mandal Lingala Baseline ($N=19$ valid):**
  * Minimum: `0.0960` ppm
  * 25th Percentile ($Q_1$): `0.1920` ppm
  * Median ($Q_2$): `0.2560` ppm
  * Mean: `0.2846` ppm
  * 75th Percentile ($Q_3$): `0.4000` ppm
  * Maximum: `0.5120` ppm
  * Standard Deviation: `0.1266` ppm
  * Interquartile Range (IQR): `0.2080` ppm
* **Village Peddakudala Context ($N=19$ records):**
  * All 19 valid records in Peddakudala range tightly between `0.096` and `0.512` ppm.
  * Notice that at **S.NO 224** in the exact same village for the exact same crop (Black Gram), the recorded BA value is **precisely `0.16`**!

### 6.3 Evaluation of Interpretations

1. **Typographical Error (`0.16`):**
   * The operator entered an extra period (`0..16`).
   * An identical value of `0.16` already exists in this exact village at S.NO 224.
   * `0.16` is completely harmonious with surrounding values (`0.192`, `0.384`, `0.128`, `0.096`).

### 6.4 Verification Determination

* **Recommended Treatment:** Parse as `0.16`.
* **Confidence Level:** **Very High (>99%)**.
* **External/Source Verification Required:** **No**. Syntactically and contextually certain.

---

## 7. Diagnostic Visual Verification

A high-resolution diagnostic plot evaluating all four anomalous features against their respective Mandal distributions has been compiled and saved to [numeric_anomalies_verification.png](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/reports/figures/numeric_anomalies_verification.png).

```
+---------------------------------------+---------------------------------------+
|  1. EC in Mandal Vempalli             |  2. FC in Mandal Vempalli             |
|     Candidate: 0.07                   |     Candidate: 2.956                  |
|     (Matches Q1 = 0.07, S.NO 246=0.08)|     (Matches mean 2.88, within IQR)   |
+---------------------------------------+---------------------------------------+
|  3. BA in Mandal Lingala              |  4. MN in Mandal Simhadripuram        |
|     Candidate: 0.16                   |     Cand A: 1.138 (z = -0.80) [BEST]  |
|     (Matches S.NO 224 in same village)|     Cand B: 11.379 (z = +5.27, OUTLIER|
+---------------------------------------+---------------------------------------+
```

---

## 8. Final Recommendations and Treatment Protocol

Below is the definitive verification and recommendation matrix for all four numeric string anomalies:

| # | Feature | S.NO | Raw Value | Recommended Preprocessing Treatment | Confidence Level | External Source Verification Required? | Operational Preprocessing Rule for Step 5 |
| :-: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `EC` | 245 | `'0..07'` | **`0.07`** | **Very High (>99%)** | **No** | Clean string typo `..` $\rightarrow$ `.`, convert to `float(0.07)`. |
| **2** | `FC` | 242 | `'2..956'` | **`2.956`** | **Very High (>99%)** | **No** | Clean string typo `..` $\rightarrow$ `.`, convert to `float(2.956)`. |
| **3** | `MN` | 55 | `'1.13.79'` | **`1.138`** *(Primary)*<br>*(or Simhadripuram Median `2.014`)* | **Moderate (75%)** | **Yes** *(for 100% paper audit trail)* | Apply primary value `1.138` with programmatic flag, or impute with Mandal median `2.014` if strict conservative policy is preferred. |
| **4** | `BA` | 229 | `'0..16'` | **`0.16`** | **Very High (>99%)** | **No** | Clean string typo `..` $\rightarrow$ `.`, convert to `float(0.16)`. |

### Important Pipeline Confirmation

1. The original dataset file [complete soil data.xlsx](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/complete%20soil%20data.xlsx) **has not been modified, overwritten, or altered in any manner**.
2. All empirical evidence documented above is programmatically reproducible via `python src/data/verify_numeric_anomalies.py`.
3. Concrete dataset cleaning and transformation will take place strictly within the programmatic preprocessing pipeline in Step 5.
