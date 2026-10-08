# Step 8: Extreme Outlier Investigation Report

**Document Version:** 1.0  
**Analysis Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/complete soil data.xlsx` (Untouched, Read-Only)  
**Execution Script:** `src/data/investigate_outliers.py`  
**Diagnostic Artifact:** `reports/figures/extreme_outliers_investigation.png`  
**Status:** Strictly Exploratory & Analytical — **No dataset records have been deleted or modified.**

---

## 1. Executive Summary

This report delivers an exhaustive, multi-criteria forensic audit of extreme statistical values across all 15 numerical features in `data/complete soil data.xlsx`. 

A pivotal finding of this audit is the **clarification of S.NO 348 and target extreme values**:
* In the preliminary Step 1 inspection notes, S.NO 348 was mischaracterized as containing "multiple simultaneous extreme spikes across EC, P2O5, and BA".
* **Our exact row-by-row data audit reveals that S.NO 348 contains ONLY a single extreme value: `EC = 8.18 dS/m`**. Its $P_2O_5$ is a completely normal $21\text{ kg/ha}$, its $BA$ is a normal $0.416\text{ ppm}$, and its $OC$ is a normal $0.27\%$.
* The other target extreme values reported in Step 1 reside in completely separate records:
  * **`OC = 31.0 %`** is at **S.NO 84** (Kondapuram)
  * **`P2O5 = 856 kg/ha`** is at **S.NO 379** (Atloor)
  * **`BA = 96.0 ppm`** is at **S.NO 62** (Simhadripuram)
  * **`N = 850.0 kg/ha`** is at **S.NO 130** (Chakrayapeta)

Every candidate outlier is evaluated using a tripartite statistical hurdle (IQR extreme bounds $> Q_3 + 3.0 \times \text{IQR}$, $z$-scores $> 3.0$, and 99th percentile analysis) combined with agronomic and geochemical domain knowledge.

---

## 2. Statistical Outlier Detection Thresholds per Feature

The table below summarizes the parametric and non-parametric outlier boundaries across the dataset ($N=611$):

| Feature | Min | $Q_1$ (25%) | Median | $Q_3$ (75%) | Max | IQR | Mild Upper Bound ($Q_3 + 1.5\text{IQR}$) | Extreme Upper Bound ($Q_3 + 3.0\text{IQR}$) | Mild Outliers | Extreme Outliers | $z > 3.0$ Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`PH`** | 6.220 | 7.800 | 8.000 | 8.200 | 8.800 | 0.400 | 8.800 | 9.400 | 4 | 0 | 1 |
| **`EC`** | 0.005 | 0.070 | 0.120 | 0.200 | 8.180 | 0.130 | 0.395 | 0.590 | 46 | 21 | 2 |
| **`OC`** | 0.019 | 0.150 | 0.190 | 0.270 | 31.000 | 0.120 | 0.450 | 0.630 | 40 | 7 | 3 |
| **`N`** | 28.000 | 188.000 | 226.000 | 251.000 | 850.000 | 63.000 | 345.500 | 440.000 | 38 | 3 | 3 |
| **`P2O5`** | 3.000 | 18.000 | 30.000 | 46.000 | 856.000 | 28.000 | 88.000 | 130.000 | 84 | 48 | 21 |
| **`K20`** | 5.000 | 338.000 | 392.000 | 459.000 | 878.000 | 121.000 | 640.500 | 822.000 | 20 | 2 | 2 |
| **`S`** | 1.000 | 6.000 | 10.000 | 16.000 | 88.000 | 10.000 | 31.000 | 46.000 | 37 | 10 | 12 |
| **`CU`** | 0.012 | 0.214 | 0.718 | 1.822 | 7.820 | 1.608 | 4.234 | 6.646 | 13 | 4 | 7 |
| **`FC`** | 0.026 | 1.910 | 3.699 | 6.730 | 42.980 | 4.820 | 13.959 | 21.188 | 51 | 14 | 11 |
| **`MN`** | 0.000 | 3.580 | 7.182 | 14.188 | 52.320 | 10.608 | 30.099 | 46.010 | 29 | 4 | 7 |
| **`ZN`** | 0.008 | 0.236 | 0.516 | 1.076 | 14.420 | 0.840 | 2.336 | 3.596 | 58 | 28 | 12 |
| **`BA`** | 0.019 | 0.192 | 0.256 | 0.416 | 96.000 | 0.224 | 0.752 | 1.088 | 57 | 37 | 1 |
| **`Temparature`**| 28.000 | 32.700 | 34.590 | 36.030 | 37.500 | 3.330 | 41.025 | 46.020 | 0 | 0 | 0 |
| **`Humidity`** | 45.090 | 66.460 | 72.590 | 81.200 | 100.000 | 14.740 | 103.310 | 125.420 | 0 | 0 | 0 |
| **`Rainfall`** | 626.400 | 688.500 | 751.400 | 834.300 | 944.500 | 145.800 | 1053.000 | 1271.700 | 0 | 0 | 0 |

---

## 3. Forensic Investigation of S.NO 348

### 3.1 Full Record Verification
* **S.NO:** 348 (Row Index 347)
* **MANDAL NAME:** Mylavaram
* **VILLAGE NAME:** M.Komaladinne
* **SOIL TYPE:** 4
* **CROP:** Red Chilli
* **Attributes:**
  * $\text{PH} = 8.20$ (80th percentile, normal alkaline)
  * $\text{EC} = \mathbf{8.18\text{ dS/m}}$ (**Extreme Outlier**, global $z = +22.90$, Mylavaram $z = +4.90$)
  * $\text{OC} = 0.27\%$ (65th percentile, normal)
  * $\text{N} = 188.0\text{ kg/ha}$ (21st percentile, normal)
  * $\text{P}_2\text{O}_5 = 21\text{ kg/ha}$ (33rd percentile, normal)
  * $\text{K}_2\text{O} = 365\text{ kg/ha}$ (45th percentile, normal)
  * $\text{S} = 6\text{ ppm}$ (27th percentile, normal)
  * $\text{CU} = 0.266\text{ ppm}$ (25th percentile, normal)
  * $\text{FC} = 9.548\text{ ppm}$ (within Mylavaram range $[1.686, 20.440]$)
  * $\text{MN} = 15.58\text{ ppm}$ (within Mylavaram range $[6.194, 22.600]$)
  * $\text{ZN} = 1.354\text{ ppm}$ (82nd percentile, normal)
  * $\text{BA} = 0.416\text{ ppm}$ (68th percentile, normal)
  * $\text{Temparature} = 35.23^\circ\text{C}$, $\text{Humidity} = 67.8\%$, $\text{Rainfall} = 858.2\text{ mm}$

### 3.2 Evaluation of S.NO 348
1. **Misconception Debunked:** S.NO 348 does **not** contain multiple extreme values. Its $P_2O_5$ is 21 (not 856), its BA is 0.416 (not 96), and its OC is 0.27% (not 31.0%).
2. **Analysis of $EC = 8.18$:**
   * In soil physics, $EC = 8.18\text{ dS/m}$ represents a severely saline soil patch (solonchak condition). Natural saline depressions in black/red transition soils frequently exhibit localized electrical conductivity spikes between $4.0$ and $12.0\text{ dS/m}$.
   * Alternatively, the lab technician could have recorded `8.18` instead of `0.818` (a $10\times$ decimal error).
   * **Classification:** **Suspicious / Requires Source Verification**. While physically possible as a true saline patch, a $10\times$ decimal error is equally probable. It should not be deleted automatically.

---

## 4. Deep Forensic Analysis of the Other Target Extreme Outliers

### 4.1 Organic Carbon ($OC$) Extremes: `31.0%`, `30.35%`, and `23.0%`
* **Records Identified:**
  1. **S.NO 84:** $\text{OC} = \mathbf{31.0\%}$ (Mandal: Kondapuram, Village: K.sugumanchipalli, Soil Type: 1, Crop: Bean Gram)
  2. **S.NO 372:** $\text{OC} = \mathbf{30.35\%}$ (Mandal: Atloor, Village: Atloor, Soil Type: 1, Crop: Bajra)
  3. **S.NO 144:** $\text{OC} = \mathbf{23.0\%}$ (Mandal: Thondur, Village: Thounduru, Soil Type: 1, Crop: Grownut)
* **Agronomic Forensic Analysis:**
  * Mineral soils in semi-arid Rayalaseema have organic carbon levels typically between $0.1\%$ and $0.8\%$. All other 608 rows in this dataset have $OC < 1.0\%$.
  * An organic carbon content of $23\% - 31\%$ is only found in waterlogged peat bogs or histosols. In hot, semi-arid mineral soils (temperatures $>35^\circ\text{C}$ and pH $>7.7$), $23\% - 31\%$ organic carbon is **physically impossible**.
  * Look at the exact digits:
    * $31.0 \rightarrow \mathbf{0.31\%}$
    * $30.35 \rightarrow \mathbf{0.30\%}$ (or $\mathbf{0.35\%}$)
    * $23.0 \rightarrow \mathbf{0.23\%}$
  * In Kondapuram, neighboring OC values are $0.19, 0.23, 0.27, 0.31, 0.35$. An intended entry of `0.31` fits perfectly.
  * In Atloor, neighboring OC values are $0.15, 0.19, 0.24, 0.31, 0.35$.
  * In Thondur, neighboring OC values are $0.19, 0.23, 0.27, 0.31$.
* **Classification:** **Probable Data-Entry Error ($100\times$ decimal point omission)**.

---

### 4.2 Boron / Barium Index ($BA$) Extreme: `96.0` at S.NO 62
* **Record Identified:**
  * **S.NO 62:** $\text{BA} = \mathbf{96.0\text{ ppm}}$ (Mandal: Simhadripuram, Village: Simhadripuram-2, Soil Type: 1, Crop: Grownut)
* **Agronomic Forensic Analysis:**
  * Across all 24 records in Simhadripuram, the other 23 records have $BA$ values between $0.064$ and $2.78\text{ ppm}$ ($Q_1=0.128, \text{Median}=0.224, Q_3=0.416$).
  * The global median is $0.256\text{ ppm}$, and the 99th percentile is $4.16\text{ ppm}$.
  * $BA = 96.0$ is **$375\times$ the median** and nearly $20\times$ the next highest value in the entire 611-row dataset ($5.376$).
  * Notice the digits: `96`. On a keyboard, omitting the leading zero and decimal point before typing `96` produces `96` instead of **`0.96`** (or `0.096`). In Simhadripuram, values of $0.096$ and $0.16$ are common.
* **Classification:** **Probable Data-Entry Error (Missing Decimal Point for 0.96)**.

---

### 4.3 Phosphorus ($P_2O_5$) Extreme: `856 kg/ha` at S.NO 379 and the Atloor Regional Cluster
* **Record Identified:**
  * **S.NO 379:** $\text{P}_2\text{O}_5 = \mathbf{856\text{ kg/ha}}$ (Mandal: Atloor, Village: Atloor, Soil Type: 1, Crop: Bajra)
* **Agronomic Forensic Analysis:**
  * Unlike the isolated typos in OC and BA, high phosphorus is **not an isolated single-cell event**.
  * Out of 34 records in Mandal Atloor, **16 records exceed $400\text{ kg/ha}$**, including:
    `[439, 486, 486, 506, 514, 547, 554, 554, 574, 574, 635, 641, 641, 682, 685, 856]`.
  * Furthermore, Atloor fields simultaneously display extreme values in available Manganese ($MN$ up to $52.32\text{ ppm}$) and Zinc ($ZN$ up to $14.42\text{ ppm}$).
  * This reflects a **true spatial/geochemical cluster** or intensive historical application of single superphosphate (SSP) / diammonium phosphate (DAP) fertilizer in the Atloor basin.
* **Classification:** **Plausible Regional Extreme (True Agronomic/Geochemical Anomaly)**.

---

### 4.4 Nitrogen ($N$) Extremes: `850 kg/ha` (S.NO 130) and `801 kg/ha` (S.NO 422)
* **Records Identified:**
  * **S.NO 130:** $N = \mathbf{850.0\text{ kg/ha}}$ (Mandal: Chakrayapeta, Village: Gaddamvaripalli, Soil Type: 4, Crop: Grownut)
  * **S.NO 422:** $N = \mathbf{801.0\text{ kg/ha}}$ (Mandal: Proddutur, Village: Thallammapuram, Soil Type: 7, Crop: Black Gram)
  * **S.NO 274:** $N = \mathbf{564.0\text{ kg/ha}}$ (Mandal: Mydukur, Village: Nandyalampeta, Soil Type: 9, Crop: Vegetables)
* **Agronomic Forensic Analysis:**
  * Available nitrogen in tropical Indian soils is normally low-to-medium ($150 - 350\text{ kg/ha}$).
  * However, localized spikes of $500 - 850\text{ kg/ha}$ occur naturally in commercial farming following heavy basal or top-dressing of urea, intensive farmyard manure (FYM), or poultry droppings prior to soil sampling.
* **Classification:** **Plausible Extreme (High Fertilizer Application)**.

---

## 5. Multi-Feature Outlier Analysis (Simultaneous Extremes)

A key objective of Task 4 is verifying whether extreme values occur simultaneously across multiple soil features within the same observation.

Our programmatic scan evaluated rows exceeding the extreme IQR boundary ($> Q_3 + 3.0 \times \text{IQR}$) across multiple features:
* **Rows with 4 Simultaneous Extreme Features ($N=1$):**
  * **S.NO 372** (Atloor): Extreme in `OC` ($30.35$), `P2O5` ($263$), `MN` ($47.86$), and `ZN` ($4.05$).
* **Rows with 3 Simultaneous Extreme Features ($N=2$):**
  * **S.NO 358** (Atloor): Extreme in `P2O5` ($554$), `MN` ($51.72$), and `ZN` ($4.78$).
  * **S.NO 359** (Atloor): Extreme in `P2O5` ($574$), `MN` ($52.32$), and `ZN` ($14.42$).
* **Rows with 2 Simultaneous Extreme Features ($N=16$):**
  * S.NO 360, 363, 364, 366, 367, 376 (all in Atloor: `P2O5` paired with `FC`, `MN`, `ZN`, or `BA`).
  * S.NO 461, 467, 480 (all in Siddavatam: `EC` paired with `BA` or `ZN`, `P2O5` paired with `MN`).
  * S.NO 525, 530, 531 (Muddanur: `P2O5` paired with `BA` or `PH`).
  * S.NO 118 (Kamalapuram: `ZN` paired with `BA`).
  * S.NO 453 (Gopavaram: `N` paired with `CU`).
  * S.NO 576 (Pendlimarri: `P2O5` paired with `BA`).
  * S.NO 613 (C.K.Dinne: `ZN` paired with `BA`).

*Conclusion:* Multi-feature extreme values are concentrated in **specific geographic corridors** (chiefly Atloor and Siddavatam), demonstrating genuine spatial co-enrichment of micronutrients and phosphorus rather than random dataset corruption.

---

## 6. Comprehensive Outlier Assessment Matrix

| S.NO | Feature | Recorded Value | Detection Method | Assessment | Justification & Agronomic Context | Recommended Action |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **348** | `EC` | `8.18 dS/m` | IQR ($>0.59$), $z=+22.90$ | **Suspicious** | Severe salinity is physically possible in arid depressions, but $10\times$ decimal typo ($0.818$) is plausible. | Retain as-is; flag for robust tree splitting; do not delete. |
| **84** | `OC` | `31.0 %` | IQR ($>0.63$), $z=+21.50$ | **Probable data-entry error** | $>20\%$ OC impossible in semi-arid mineral soils (Histosol peat level). Clear $100\times$ decimal shift ($0.31\%$). | Retain untouched in raw; flag for decimal repair ($0.31$) in preprocessing. |
| **372** | `OC` | `30.35 %` | IQR ($>0.63$), $z=+21.05$ | **Probable data-entry error** | Impossible mineral soil OC. Textbook $100\times$ decimal shift ($0.30\%$ or $0.35\%$). | Retain untouched in raw; flag for decimal repair ($0.30$) in preprocessing. |
| **144** | `OC` | `23.0 %` | IQR ($>0.63$), $z=+15.91$ | **Probable data-entry error** | Impossible mineral soil OC. Textbook $100\times$ decimal shift ($0.23\%$). | Retain untouched in raw; flag for decimal repair ($0.23$) in preprocessing. |
| **62** | `BA` | `96.0 ppm` | IQR ($>1.09$), $z=+24.26$ | **Probable data-entry error** | $375\times$ local median; next highest in Mandal is $2.78$. Missing decimal point for $0.96$ ppm. | Retain untouched in raw; flag for decimal repair ($0.96$) in preprocessing. |
| **379** | `P2O5` | `856 kg/ha` | IQR ($>130$), $z=+8.67$ | **Plausible extreme** | Member of a contiguous 16-farm spatial cluster in Mandal Atloor ($P_2O_5 > 400$). True field condition. | Retain as-is; valid regional agricultural signal. |
| **372** | `P2O5` | `263 kg/ha` | IQR ($>130$), $z=+2.22$ | **Plausible extreme** | Member of Atloor high-phosphorus cluster. True field condition. | Retain as-is; valid regional agricultural signal. |
| **130** | `N` | `850.0 kg/ha` | IQR ($>440$), $z=+7.37$ | **Plausible extreme** | Reflects heavy nitrogenous fertilization (urea/manure) prior to sampling. | Retain as-is; valid high-input agricultural signal. |
| **422** | `N` | `801.0 kg/ha` | IQR ($>440$), $z=+6.79$ | **Plausible extreme** | Intensive fertilizer application in Proddutur. | Retain as-is; valid high-input agricultural signal. |
| **274** | `N` | `564.0 kg/ha` | IQR ($>440$), $z=+4.02$ | **Plausible extreme** | Commercial vegetable farming in Mydukur with heavy organic manuring. | Retain as-is; valid agricultural signal. |
| **359** | `MN` | `52.32 ppm` | IQR ($>46.0$), $z=+4.19$ | **Plausible extreme** | Natural manganese-rich parent material in Atloor basin. | Retain as-is; valid geochemical signal. |
| **359** | `ZN` | `14.42 ppm` | IQR ($>3.60$), $z=+10.89$ | **Plausible extreme** | Co-occurs with extreme MN and P2O5 in Atloor; true localized geochemical deposit. | Retain as-is; valid geochemical signal. |
| **531** | `PH` | `6.22` | IQR low ($<7.2$), $z=-4.88$ | **Plausible extreme** | Only acidic/slightly acidic soil in dataset; papaya field in Muddanur. | Retain as-is; vital negative indicator for alkaline-adapted crops. |
| **531** | `P2O5` | `527 kg/ha` | IQR ($>130$), $z=+5.10$ | **Plausible extreme** | Heavy phosphatic application in commercial papaya orchard. | Retain as-is; valid crop-specific signal. |

---

## 7. Why Simply Removing Statistical Outliers is Inappropriate in Agriculture

In traditional computer science or standard statistical tutorials, practitioners often apply aggressive outlier filtering (e.g. discarding all samples with $|z| > 3$ or beyond $1.5 \times \text{IQR}$). In agricultural machine learning, **this practice is scientifically invalid and harmful**:

1. **Non-Gaussian Distributions are the Biological Norm:**
   Soil nutrients and meteorological factors follow log-normal, exponential, or bimodal distributions dictated by geology, drainage basins, and management practices. Assuming normality and trimming tails discards valid agro-ecological reality.
2. **True Extreme Conditions are Vital Discriminative Signals:**
   * A soil with $EC = 8.18\text{ dS/m}$ represents severe salinity. An intelligent model must learn that salt-sensitive crops (like pulses or sweet orange) will fail under such conditions, whereas tolerant crops (like cotton or bajra) can survive. Removing this row strips the model of critical boundary decision intelligence.
   * A soil with $\text{pH} = 6.22$ (S.NO 531, Papaya) is the sole acidic observation. Removing it deprives the model of its only example of slightly acidic soil management.
3. **Regional Geochemical Clusters are Genuine:**
   The 16 high-phosphorus farms in Atloor represent an authentic regional soil characteristic. Deleting them would artificially homogenize the dataset and degrade predictive accuracy for farmers in the Atloor basin.
4. **Tree-Based Ensembles are Naturally Robust:**
   Decision trees, Random Forests, Extra Trees, XGBoost, and LightGBM split data using **monotonic rank-order thresholding** ($X_j \le \theta$). Unlike linear regression or neural networks, tree ensembles are mathematically invariant to monotonic feature scaling and extreme outlier magnitudes. A value of $856$ or $850$ simply falls into the upper partition leaf without distorting the split boundary for lower values.
5. **Clear Separation of Errors vs. Extremes:**
   * **True Agronomic Extremes** ($N=850, P=856, \text{pH}=6.22, MN=52.32$) must be **retained**.
   * **Obvious Decimal Keystroke Errors** ($OC=31.0, 30.35, 23.0$ and $BA=96.0$) should be **repaired via documented preprocessing transformations** rather than deleting entire farm records.

---

## 8. Dataset Integrity Confirmation

* `data/complete soil data.xlsx` **remains 100% unaltered**.
* No records have been deleted, dropped, or capped in the source files.
