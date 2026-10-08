# Numeric Anomalies Investigation Report

**Document Version:** 1.0  
**Investigation Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/processed/genuine_agricultural_data.csv` (Untouched, Read-Only)  
**Status:** Strictly Exploratory — No dataset values have been modified or replaced.

---

## 1. Executive Summary

During the dataset profiling phase of Step 1, four specific cells in numerical columns were flagged because their string values prevented standard floating-point conversion. This report documents the exact records, their localized agronomic context within the Kadapa district, surrounding values from the same Mandals and Villages, descriptive statistics across the affected features, and a disciplined analysis of potential corrections without modifying the underlying data.

---

## 2. Inventory of Flagged Anomalies

| # | Column | Row Index | S.NO | Raw Value | Mandal Name | Village Name | Recorded Crop | Nature of Anomaly |
| :-: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | `EC` | 244 | 245 | `'0..07'` | Vempalli | Vempalli-7 | Grownut | Double decimal point typo |
| **2** | `FC` | 241 | 242 | `'2..956'` | Vempalli | Vempalli-5 | Grownut | Double decimal point typo |
| **3** | `MN` | 54 | 55 | `'1.13.79'` | Simhadripuram | Kasanur | sunflower | Multiple decimal points (ambiguous) |
| **4** | `BA` | 228 | 229 | `'0..16'` | Lingala | Peddakudala | Black Gram | Double decimal point typo |

---

## 3. Detailed Investigation of Each Anomaly

---

### Anomaly 1: Electrical Conductivity (`EC`) — Row Index 244 (S.NO 245)

#### Full Row Context
* **S.NO:** 245
* **MANDAL NAME:** Vempalli
* **VILLAGE NAME:** Vempalli-7
* **SOIL TYPE:** 1
* **PH:** 8.23
* **EC (Raw):** `'0..07'`
* **OC:** 0.19%
* **N:** 301.0 kg/ha
* **P2O5:** 36 kg/ha
* **K20:** 338 kg/ha
* **S:** 4 ppm
* **CU:** 0.144 ppm
* **FC:** 2.538
* **MN:** 3.484 ppm
* **ZN:** 0.802 ppm
* **BA:** 4.16 ppm
* **Temperature:** 36.4 °C
* **Humidity:** 83.0 %
* **Rainfall:** 826.4 mm
* **CROP:** Grownut

#### Surrounding Values in Column `EC` (Rows 240 to 248)

| Row Index | S.NO | Mandal Name | Village Name | EC Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 240 | 241 | Vempalli | Vempalli-5 | `0.06` | 8.27 | Grownut |
| 241 | 242 | Vempalli | Vempalli-5 | `0.05` | 8.32 | Grownut |
| 242 | 243 | Vempalli | Vempalli-6 | `0.07` | 8.29 | cotton |
| 243 | 244 | Vempalli | Vempalli-6 | `0.09` | 8.32 | cotton |
| **244** | **245** | **Vempalli** | **Vempalli-7** | **`'0..07'`** | **8.23** | **Grownut** |
| 245 | 246 | Vempalli | Vempalli-7 | `0.08` | 8.25 | Banana |
| 246 | 247 | Vempalli | Vempalli-8 | `0.15` | 8.47 | Grownut |
| 247 | 248 | Vempalli | Vempalli-8 | `0.11` | 8.35 | Grownut |
| 248 | 249 | Vempalli | Idupulapaya-1 | `0.05` | 8.52 | Grownut |

#### Observations & Interpretation
* The entry `'0..07'` contains an accidental double-period keystroke.
* Surrounding field records in Vempalli range consistently between `0.05` and `0.15` dS/m.
* **Obvious Possible Correction:** `0.07` *(requires verification)*.

---

### Anomaly 2: Field Capacity / Iron Index (`FC`) — Row Index 241 (S.NO 242)

#### Full Row Context
* **S.NO:** 242
* **MANDAL NAME:** Vempalli
* **VILLAGE NAME:** Vempalli-5
* **SOIL TYPE:** 1
* **PH:** 8.32
* **EC:** 0.05
* **OC:** 0.07%
* **N:** 163.0 kg/ha
* **P2O5:** 50 kg/ha
* **K20:** 527 kg/ha
* **S:** 14 ppm
* **CU:** 0.24 ppm
* **FC (Raw):** `'2..956'`
* **MN:** 6.884 ppm
* **ZN:** 0.152 ppm
* **BA:** 0.256 ppm
* **Temperature:** 36.4 °C
* **Humidity:** 83.0 %
* **Rainfall:** 826.4 mm
* **CROP:** Grownut

#### Surrounding Values in Column `FC` (Rows 238 to 245)

| Row Index | S.NO | Mandal Name | Village Name | FC Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 238 | 239 | Vempalli | Vempalli-4 | `2.538` | 8.21 | Grownut |
| 239 | 240 | Vempalli | Vempalli-4 | `1.034` | 8.30 | Banana |
| 240 | 241 | Vempalli | Vempalli-5 | `0.776` | 8.27 | Grownut |
| **241** | **242** | **Vempalli** | **Vempalli-5** | **`'2..956'`** | **8.32** | **Grownut** |
| 242 | 243 | Vempalli | Vempalli-6 | `3.140` | 8.29 | cotton |
| 243 | 244 | Vempalli | Vempalli-6 | `3.254` | 8.32 | cotton |
| 244 | 245 | Vempalli | Vempalli-7 | `2.538` | 8.23 | Grownut |
| 245 | 246 | Vempalli | Vempalli-7 | `3.490` | 8.25 | Banana |

#### Observations & Interpretation
* The entry `'2..956'` contains an accidental double-period keystroke between the integer digit `2` and the decimal portion `956`.
* Surrounding field records in Vempalli-4 through Vempalli-7 are all 3-decimal floating point numbers ranging between `0.776` and `3.490`.
* **Obvious Possible Correction:** `2.956` *(requires verification)*.

---

### Anomaly 3: Manganese (`MN`) — Row Index 54 (S.NO 55)

#### Full Row Context
* **S.NO:** 55
* **MANDAL NAME:** Simhadripuram
* **VILLAGE NAME:** Kasanur
* **SOIL TYPE:** 3
* **PH:** 8.25
* **EC:** 0.12
* **OC:** 0.03%
* **N:** 213.0 kg/ha
* **P2O5:** 9 kg/ha
* **K20:** 425 kg/ha
* **S:** 16 ppm
* **CU:** 0.466 ppm
* **FC:** 1.022
* **MN (Raw):** `'1.13.79'`
* **ZN:** 1.042 ppm
* **BA:** 2.78 ppm
* **Temperature:** 34.7 °C
* **Humidity:** 45.09 %
* **Rainfall:** 626.4 mm
* **CROP:** sunflower

#### Surrounding Values in Column `MN` (Rows 50 to 58)

| Row Index | S.NO | Mandal Name | Village Name | MN Value | Cu Value | Zn Value | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 50 | 51 | Simhadripuram | Balapanur | `0.516` | 0.214 | 0.506 | sweet orange |
| 51 | 52 | Simhadripuram | Balapanur | `3.184` | 0.026 | 0.592 | Black gram |
| 52 | 53 | Simhadripuram | Himakuntla | `2.014` | 0.278 | 1.140 | Sweet orange |
| 53 | 54 | Simhadripuram | Himakuntla | `1.174` | 0.026 | 1.128 | grownut |
| **54** | **55** | **Simhadripuram** | **Kasanur** | **`'1.13.79'`** | **0.466** | **1.042** | **sunflower** |
| 55 | 56 | Simhadripuram | Kasanur | `5.012` | 0.120 | 0.312 | grownut |
| 56 | 57 | Simhadripuram | Lomada | `1.138` | 0.120 | 0.452 | sweet orange |
| 57 | 58 | Simhadripuram | Lomada | `1.394` | 0.058 | 1.000 | grownut |
| 58 | 59 | Simhadripuram | Simhadripuram-1 | `1.722` | 0.120 | 0.508 | black gram |

#### Detailed Ambiguity Analysis
Unlike simple double-dot typos (`..`), the string `'1.13.79'` has two separate decimal points separating three distinct digit groups: `['1', '13', '79']`. The intended numeric value cannot be determined with certainty without referencing the laboratory logbook. Plausible interpretations include:

1. **Interpretation A — `1.1379` (or rounded `1.138`):**
   * Typist entered `1.13` and intended to type `79` (or `8`), accidentally inserting a dot between `13` and `79`.
   * *Evidence:* Notice that two rows later (Row index 56, S.NO 57 in the same Mandal) the recorded MN is exactly **`1.138`**. Furthermore, across all 24 records in Mandal Simhadripuram, the median MN is **`2.014`**, the mean is **`2.4926`**, and values typically range from `0.5` to `5.0`. A value of `1.1379` or `1.138` fits the local distribution exceptionally well.
2. **Interpretation B — `11.379`:**
   * Typist intended to enter `11.379`, but accidentally pressed a period after the first digit `1`.
   * *Evidence:* Across the global dataset (all Mandals), MN values reach up to `52.32`, with a global mean of `10.52`. Thus, `11.379` is completely plausible in the global context, though it would be the highest value in Mandal Simhadripuram (where the current non-corrupted maximum is `6.914`).
3. **Interpretation C — `13.79`:**
   * The leading `1.` was an accidental keystroke before typing `13.79`.
4. **Interpretation D — Statistical Imputation (Mandal Median or Global Median):**
   * Treat cell as corrupted and impute with Simhadripuram median (`2.014`) or global median (`7.182`).
* **Conclusion:** This value is inherently ambiguous. **No single correction can be guessed without formal verification.**

---

### Anomaly 4: Boron / Barium Index (`BA`) — Row Index 228 (S.NO 229)

#### Full Row Context
* **S.NO:** 229
* **MANDAL NAME:** Lingala
* **VILLAGE NAME:** Peddakudala
* **SOIL TYPE:** 1
* **PH:** 8.25
* **EC:** 0.33
* **OC:** 0.11%
* **N:** 226.0 kg/ha
* **P2O5:** 14 kg/ha
* **K20:** 459 kg/ha
* **S:** 19 ppm
* **CU:** 0.144 ppm
* **FC:** 2.716
* **MN:** 6.93 ppm
* **ZN:** 0.152 ppm
* **BA (Raw):** `'0..16'`
* **Temperature:** 36.26 °C
* **Humidity:** 70.95 %
* **Rainfall:** 667.8 mm
* **CROP:** Black Gram

#### Surrounding Values in Column `BA` (Rows 225 to 232)

| Row Index | S.NO | Mandal Name | Village Name | BA Value | pH | Crop |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 225 | 226 | Lingala | Peddakudala | `0.416` | 8.09 | Black Gram |
| 226 | 227 | Lingala | Peddakudala | `0.192` | 8.09 | Black Gram |
| 227 | 228 | Lingala | Peddakudala | `0.384` | 8.12 | Black Gram |
| **228** | **229** | **Lingala** | **Peddakudala** | **`'0..16'`** | **8.25** | **Black Gram** |
| 229 | 230 | Lingala | Peddakudala | `0.128` | 8.29 | Black Gram |
| 230 | 231 | Lingala | Peddakudala | `0.096` | 8.21 | Black Gram |
| 231 | 232 | Lingala | Peddakudala | `0.352` | 8.24 | Black Gram |
| 232 | 233 | Vempalli | Vempalli-1 | `0.256` | 8.32 | Grownut |

#### Observations & Interpretation
* The entry `'0..16'` contains an accidental double-period keystroke between `0` and `16`.
* Surrounding field records in the identical village (Peddakudala) range tightly between `0.096` and `0.416` ppm.
* In Mandal Lingala, the median BA is `0.256` ppm and the mean is `0.2846` ppm.
* **Obvious Possible Correction:** `0.16` (or `0.160`) *(requires verification)*.

---

## 4. Descriptive Statistics (Temporary Coercion to NaN for Analysis)

To evaluate the mathematical context of each feature without modifying the dataset, the single invalid string in each of the four columns was temporarily coerced to `NaN` exclusively in memory during statistical computation:

### Global Dataset Statistics (610 Valid Observations)

| Metric | `EC` (dS/m) | `FC` | `MN` (ppm) | `BA` (ppm) |
| :--- | :---: | :---: | :---: | :---: |
| **Valid Count** | 610 | 610 | 610 | 610 |
| **Coerced NaN Count** | 1 | 1 | 1 | 1 |
| **Mean** | 0.1644 | 5.4104 | 10.5211 | 0.6044 |
| **Median (50%)** | 0.1200 | 3.6990 | 7.1820 | 0.2560 |
| **Std Deviation** | 0.3500 | 5.2656 | 9.9720 | 3.9318 |
| **Minimum** | 0.0050 | 0.0260 | 0.0000 | 0.0190 |
| **25th Percentile** | 0.0700 | 1.9100 | 3.5800 | 0.1920 |
| **75th Percentile** | 0.2000 | 6.7295 | 14.1875 | 0.4160 |
| **Maximum** | 8.1800 | 42.9800 | 52.3200 | 96.0000 |
| **Interquartile Range (IQR)** | 0.1300 | 4.8195 | 10.6075 | 0.2240 |

### Local Mandal-Level Statistics

| Column | Target Mandal | Mandal Sample Count | Mandal Mean | Mandal Median | Mandal Min | Mandal Max |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`EC`** | Vempalli | 34 | 0.1133 | 0.0900 | 0.0200 | 0.4000 |
| **`FC`** | Vempalli | 34 | 2.8793 | 2.3580 | 0.2300 | 14.2800 |
| **`MN`** | Simhadripuram | 24 | 2.4926 | 2.0140 | 0.0040 | 6.9140 |
| **`BA`** | Lingala | 20 | 0.2846 | 0.2560 | 0.0960 | 0.5120 |

---

## 5. Summary of Recommended Verification Protocols

1. **For `EC = '0..07'` (Row 244):**
   * Syntactically obvious typo of double decimal point.
   * Recommendation: Correct to `0.07` upon formal verification.
2. **For `FC = '2..956'` (Row 241):**
   * Syntactically obvious typo of double decimal point.
   * Recommendation: Correct to `2.956` upon formal verification.
3. **For `BA = '0..16'` (Row 228):**
   * Syntactically obvious typo of double decimal point.
   * Recommendation: Correct to `0.16` upon formal verification.
4. **For `MN = '1.13.79'` (Row 54):**
   * Highly ambiguous multi-decimal string.
   * Three primary candidate treatments:
     - Candidate 1: Set to `1.138` (or `1.1379`), which matches Row 56 in the same Mandal and fits the Mandal distribution (mean: 2.49, median: 2.01).
     - Candidate 2: Set to `11.379`, which aligns with the global dataset mean (10.52).
     - Candidate 3: Impute with Mandal median (`2.014`) or global median (`7.182`).
   * *Final Decision Protocol:* Candidate must be explicitly confirmed before applying any update.

---

## 6. Dataset Integrity Confirmation

* Both `data/complete soil data.xlsx` and `data/processed/genuine_agricultural_data.csv` **remain 100% unaltered**.
* No in-place modifications, substitutions, or imputations were executed.
