# Step 1 — Dataset Inspection

**Document Version:** 1.0  
**Inspection Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset File:** `data/complete soil data.xlsx` (Untouched, Original)  

---

## 1. Dataset Source
The dataset consists of real agricultural field measurements collected from various agricultural farmlands across the **Kadapa district of Andhra Pradesh, India**. The dataset was provided as an Excel spreadsheet (`data/complete soil data.xlsx`) under the active worksheet titled `'complete soil data'`.

---

## 2. Dataset Dimensions
A programmatic inspection of the spreadsheet reveals the following raw dimensions:
* **Total Rows:** 611 data rows (excluding the single header row; Excel line count is 612).
* **Total Columns in Excel:** 16,384 columns (spanning columns `A` to `XFD`, the absolute technical column limit of Microsoft Excel).

---

## 3. Actual Agricultural Columns
Through programmatic column scanning (evaluating columns with at least one non-null value), exactly **20 genuine agricultural data columns** were identified:

| Column Index | Column Name | Technical Data Type | Description |
| :---: | :--- | :---: | :--- |
| 0 | `S.NO` | `int64` | Serial identification number |
| 1 | `MANDAL NAME` | `object` | Administrative sub-district name (27 unique Mandals) |
| 2 | `VILLAGE NAME` | `object` | Local village name (231 unique Villages) |
| 3 | `SOIL TYPE` | `int64` | Numeric classification of soil category |
| 4 | `PH` | `float64` | Soil pH level (acidity / alkalinity) |
| 5 | `EC` | `object` | Electrical Conductivity in dS/m (salinity indicator) |
| 6 | `OC` | `float64` | Organic Carbon percentage in soil (%) |
| 7 | `N` | `float64` | Available Nitrogen in soil (kg/ha) |
| 8 | `P2O5` | `int64` | Available Phosphorus / Phosphate (kg/ha) |
| 9 | `K20` | `int64` | Available Potassium / Potash (kg/ha; column header uses digit zero `'0'`) |
| 10 | `S` | `int64` | Available Sulphur (ppm) |
| 11 | `CU` | `float64` | Available Copper (ppm) |
| 12 | `FC` | `object` | Field Capacity or Iron ($Fe$) — *Meaning requires verification from the original dataset/source.* |
| 13 | `MN` | `object` | Available Manganese (ppm) |
| 14 | `ZN` | `float64` | Available Zinc (ppm) |
| 15 | `BA` | `object` | Boron ($B$) or Barium ($Ba$) — *Meaning requires verification from the original dataset/source.* |
| 16 | `Temparature` | `float64` | Mean ambient temperature in °C (Header spelled `'Temparature'`) |
| 17 | `Humidity` | `float64` | Relative humidity percentage (%) |
| 18 | `Rainfall` | `float64` | Local mean rainfall in mm |
| 19 | `CROP` | `object` | Target crop cultivated / recommended |

---

## 4. Empty Excel Artifact Columns
* **Total Empty Columns:** Exactly 16,364 columns (`Column1` through `Column16364`).
* **Non-Null Cell Count:** Exactly 0 non-null cells across all 16,364 trailing columns.
* **Cause:** When an Excel table formatting or styling range was created, the table region expanded across the entire horizontal boundary of the worksheet ($2^{14} = 16,384$ columns).
* **Treatment:** These columns contain zero informational value and must be filtered out programmatically during ingestion without modifying the original file.

---

## 5. Data Types
A detailed data type profile of the 20 genuine agricultural columns reveals an unexpected mismatch in four columns that logically represent numeric laboratory measurements:

| Column Name | Stored Pandas Data Type | Expected Logical Type | Cause of Discrepancy |
| :--- | :---: | :---: | :--- |
| `S.NO` | `int64` | Integer | Correctly stored as integer |
| `MANDAL NAME` | `object` | String / Categorical | Correctly stored as string |
| `VILLAGE NAME` | `object` | String / Categorical | Correctly stored as string |
| `SOIL TYPE` | `int64` | Categorical code | Stored as integer |
| `PH` | `float64` | Continuous Float | Correctly stored as float |
| `EC` | `object` | Continuous Float | **Typo:** Contains string `'0..07'` at Row index 244 |
| `OC` | `float64` | Continuous Float | Correctly stored as float |
| `N` | `float64` | Continuous Float | Correctly stored as float |
| `P2O5` | `int64` | Continuous Integer | Correctly stored as integer |
| `K20` | `int64` | Continuous Integer | Correctly stored as integer |
| `S` | `int64` | Continuous Integer | Correctly stored as integer |
| `CU` | `float64` | Continuous Float | Correctly stored as float |
| `FC` | `object` | Continuous Float | **Typo:** Contains string `'2..956'` at Row index 241 |
| `MN` | `object` | Continuous Float | **Typo:** Contains string `'1.13.79'` at Row index 54 |
| `ZN` | `float64` | Continuous Float | Correctly stored as float |
| `BA` | `object` | Continuous Float | **Typo:** Contains string `'0..16'` at Row index 228 |
| `Temparature` | `float64` | Continuous Float | Correctly stored as float |
| `Humidity` | `float64` | Continuous Float | Correctly stored as float (has 20 NaNs) |
| `Rainfall` | `float64` | Continuous Float | Correctly stored as float |
| `CROP` | `object` | String / Categorical | Correctly stored as string |

---

## 6. Missing Values
Among all 20 actual agricultural data columns, **only a single column contains missing values**:
* **Column:** `Humidity`
* **Missing Count:** 20 values
* **Missing Percentage:** 3.27% of the total dataset (591 valid entries out of 611)
* **Zero Missing Values in Remaining 19 Columns:** `S.NO`, `MANDAL NAME`, `VILLAGE NAME`, `SOIL TYPE`, `PH`, `EC`, `OC`, `N`, `P2O5`, `K20`, `S`, `CU`, `FC`, `MN`, `ZN`, `BA`, `Temparature`, `Rainfall`, and `CROP` have 100% complete records.

### Complete Record Breakdown of Rows with Missing Humidity:
All 20 missing values are geographically clustered in **Mandal `Mydukur`** across contiguous row indices 266 through 285:

| Row Index | S.NO | Mandal Name | Village Name | Recorded Crop | Temperature (°C) | Rainfall (mm) |
| :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| 266 | 267 | Mydukur | Annaluru | paddy | 31.0 | 658.5 |
| 267 | 268 | Mydukur | Annaluru | Black gram | 31.0 | 658.5 |
| 268 | 269 | Mydukur | Sivapuram | Tamota | 31.0 | 658.5 |
| 269 | 270 | Mydukur | Sivapuram | Jowar | 31.0 | 658.5 |
| 270 | 271 | Mydukur | Nandyalampeta | Turemeric | 31.0 | 658.5 |
| 271 | 272 | Mydukur | Nandyalampeta | Black gram | 31.0 | 658.5 |
| 272 | 273 | Mydukur | Nandyalampeta | Black gram | 31.0 | 658.5 |
| 273 | 274 | Mydukur | Nandyalampeta | Vegetables | 31.0 | 658.5 |
| 274 | 275 | Mydukur | Audireddypalle | Chillis | 31.0 | 658.5 |
| 275 | 276 | Mydukur | Audireddypalle | Banana | 31.0 | 658.5 |
| 276 | 277 | Mydukur | Settivaripalli | Jowar | 31.0 | 658.5 |
| 277 | 278 | Mydukur | Settivaripalli | Jowar | 31.0 | 658.5 |
| 278 | 279 | Mydukur | Viswanadhapuram | Tamota | 31.0 | 658.5 |
| 279 | 280 | Mydukur | Viswanadhapuram | Tamota | 31.0 | 658.5 |
| 280 | 281 | Mydukur | Onipenta | Vegetables | 31.0 | 658.5 |
| 281 | 282 | Mydukur | Onipenta | Vegetables | 31.0 | 658.5 |
| 282 | 283 | Mydukur | Mittamedapalle | Vegetables | 31.0 | 658.5 |
| 283 | 284 | Mydukur | Mittamedapalle | Vegetables | 31.0 | 658.5 |
| 284 | 285 | Mydukur | Ganjikunta | Black gram | 31.0 | 658.5 |
| 285 | 286 | Mydukur | Ganjikunta | Black gram | 31.0 | 658.5 |

*Note: Per protocol, no values have been filled or removed.*

---

## 7. Numeric Anomalies
Four individual cells in four numerical features contain malformed decimal typographical errors that prevent standard floating-point conversion:

| Column | Row Index | S.NO | Raw Value in Cell | Detailed Observation & Note |
| :---: | :---: | :---: | :---: | :--- |
| **`EC`** | 244 | 245 | `'0..07'` | Double decimal point. Possible correction: `0.07` — needs verification. |
| **`FC`** | 241 | 242 | `'2..956'` | Double decimal point. Possible correction: `2.956` — needs verification. |
| **`MN`** | 54 | 55 | `'1.13.79'` | Ambiguous multiple decimals. Could be `11.379` or `1.1379` or `1.138` — needs verification. |
| **`BA`** | 228 | 229 | `'0..16'` | Double decimal point. Possible correction: `0.16` — needs verification. |

*Note: No values have been modified.*

---

## 8. Crop Labels
Analysis of the `CROP` target column reveals substantial label fragmentation:
* **Raw Unique Crop Labels:** **61 distinct strings**.
* **Case-Insensitive / Trimmed Unique Labels:** **46 distinct strings**.
* **Types of Variations Observed:**
  1. **Capitalization Differences:**
     * `cotton` (89) vs `Cotton` (4)
     * `Grownut` (55) vs `grownut` (6)
     * `Bengal gram` (24) vs `Bengal Gram` (6)
     * `Banana` (5) vs `banana` (9)
     * `sunflower` (11) vs `Sunflower` (2)
     * `chamanthi` (6) vs `Chamanthi` (1)
     * `Vegetables` (5) vs `vegetables` (1)
     * `soyabean` (6) vs `Soyabean` (3)
  2. **Typographical Spelling Differences:**
     * Black Gram: `Black Gram` (48), `Black gram` (30), `black gram` (3), `Blakgram` (10), `Blak Gram` (2), `Blak gram` (1), `Blackgram` (1)
     * Turmeric: `Turmeric` (22), `turmeric` (8), `Turemaric` (2), `termeric` (1), `Turemeric` (1), `Turmaric` (1)
     * Sweet Orange: `sweet orange` (12), `Sweet orange` (1), `sweet ornage` (3), `swwet orange` (1), `sweet lime` (1)
     * Tomato: `Tamota` (4)
     * Sesame: `sesam` (4), `sesasum` (1), `Sesamum` (1)
     * Chillies: `chillis` (2), `Chillis` (1), `Red Chilli` (3), `Greenchilli` (1)
     * Jowar: `Jowar` (4), `Jouar` (2), `jouar` (1)
     * Muskmelon: `muckmelon` (1)
     * Castor: `Caster` (1)
  3. **Vernacular / Regional Telugu Names:**
     * `Allam` (1) — Telugu for Ginger
     * `Korra` (4) — Telugu for Foxtail Millet
     * `Chamanthi` (7) — Telugu for Chrysanthemum (also present as `mums` (1))
     * `Nannari` (1) — Indian Sarsaparilla (*Hemidesmus indicus*)
  4. **Generic Categorical Names:**
     * `Vegetables` (6 total)

*Per strict protocol: No labels have been merged, and no identity assumptions have been applied.*

---

## 9. Class Frequency Distribution
Complete frequency count of all 61 raw crop labels in the dataset:

| Rank | Raw Crop Label | Frequency | Percentage (%) | Rank | Raw Crop Label | Frequency | Percentage (%) |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| 1 | `paddy` | 143 | 23.40% | 32 | `maize` | 2 | 0.33% |
| 2 | `cotton` | 89 | 14.57% | 33 | `Acidlime` | 2 | 0.33% |
| 3 | `Grownut` | 55 | 9.00% | 34 | `Green Gram` | 2 | 0.33% |
| 4 | `Black Gram` | 48 | 7.86% | 35 | `Sunflower` | 2 | 0.33% |
| 5 | `Bajra` | 34 | 5.56% | 36 | `chillis` | 2 | 0.33% |
| 6 | `Black gram` | 30 | 4.91% | 37 | `Turemaric` | 2 | 0.33% |
| 7 | `Bengal gram` | 24 | 3.93% | 38 | `Jouar` | 2 | 0.33% |
| 8 | `Turmeric` | 22 | 3.60% | 39 | `Blak Gram` | 2 | 0.33% |
| 9 | `sweet orange` | 12 | 1.96% | 40 | `jouar` | 1 | 0.16% |
| 10 | `sunflower` | 11 | 1.80% | 41 | `guava` | 1 | 0.16% |
| 11 | `Blakgram` | 10 | 1.64% | 42 | `Sweet orange` | 1 | 0.16% |
| 12 | `banana` | 9 | 1.47% | 43 | `termeric` | 1 | 0.16% |
| 13 | `turmeric` | 8 | 1.31% | 44 | `muckmelon` | 1 | 0.16% |
| 14 | `onion` | 8 | 1.31% | 45 | `swwet orange` | 1 | 0.16% |
| 15 | `grownut` | 6 | 0.98% | 46 | `mums` | 1 | 0.16% |
| 16 | `soyabean` | 6 | 0.98% | 47 | `Blak gram` | 1 | 0.16% |
| 17 | `chamanthi` | 6 | 0.98% | 48 | `Chillis` | 1 | 0.16% |
| 18 | `Bengal Gram` | 6 | 0.98% | 49 | `Turemeric` | 1 | 0.16% |
| 19 | `Vegetables` | 5 | 0.82% | 50 | `Blackgram` | 1 | 0.16% |
| 20 | `Banana` | 5 | 0.82% | 51 | `Red Gram` | 1 | 0.16% |
| 21 | `Jowar` | 4 | 0.65% | 52 | `vegetables` | 1 | 0.16% |
| 22 | `Cotton` | 4 | 0.65% | 53 | `sweet lime` | 1 | 0.16% |
| 23 | `korra` | 4 | 0.65% | 54 | `sesasum` | 1 | 0.16% |
| 24 | `Tamota` | 4 | 0.65% | 55 | `Allam` | 1 | 0.16% |
| 25 | `sesam` | 4 | 0.65% | 56 | `Turmaric` | 1 | 0.16% |
| 26 | `Soyabean` | 3 | 0.49% | 57 | `Caster` | 1 | 0.16% |
| 27 | `black gram` | 3 | 0.49% | 58 | `papaya` | 1 | 0.16% |
| 28 | `Bean Gram` | 3 | 0.49% | 59 | `Nannari` | 1 | 0.16% |
| 29 | `sweet ornage` | 3 | 0.49% | 60 | `Greenchilli` | 1 | 0.16% |
| 30 | `Red Chilli` | 3 | 0.49% | 61 | `Sesamum` | 1 | 0.16% |
| 31 | `Chamanthi` | 1 | 0.16% | **Total** | — | **611** | **100.0%** |

*Key Takeaway:* The top 4 categories (`paddy`, `cotton`, `Grownut`, `Black Gram`) account for over 54% of all records. In contrast, 14 labels appear only once (singleton classes).

---

## 10. Duplicate Records
* **Duplicate Rows:** **0 duplicates** across all 20 actual agricultural features (every row represents a distinct field measurement vector).
* **Duplicate S.NO Values:** **3 duplicate values** exist:
  * `S.NO = 29` (appears at row index 28 and row index 29)
  * `S.NO = 65` (appears at row index 64 and row index 65)
  * `S.NO = 66` (appears at row index 66 and row index 67)
* **S.NO Range:** Minimum is `0` (at row index 9), and Maximum is `616`. Total unique S.NO count is 608.

---

## 11. Numeric Statistics
Descriptive statistical profile across all 17 continuous/numerical agricultural features:

| Feature | Valid Count | Coerced Count | Mean | Median | Std Dev | Min | 25% | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `S.NO` | 611 | 0 | 305.7889 | 306.00 | 177.9739 | 0.000 | 150.50 | 459.50 | 616.00 |
| `SOIL TYPE` | 611 | 0 | 2.3028 | 1.00 | 2.6023 | 1.000 | 1.00 | 3.00 | 13.00 |
| `PH` | 611 | 0 | 7.9875 | 8.02 | 0.2638 | 6.220 | 7.83 | 8.145 | 8.90 |
| `EC`* | 610 | 1 | 0.1644 | 0.12 | 0.3500 | 0.005 | 0.07 | 0.20 | 8.18 |
| `OC` | 611 | 0 | 0.3512 | 0.19 | 1.9721 | 0.015 | 0.125 | 0.27 | 31.00 |
| `N` | 611 | 0 | 220.3237 | 226.00 | 61.4102 | 1.000 | 188.00 | 250.00 | 850.00 |
| `P2O5` | 611 | 0 | 59.0475 | 30.00 | 111.5840 | 2.000 | 18.00 | 46.00 | 856.00 |
| `K20` | 611 | 0 | 374.5237 | 392.00 | 161.3833 | 5.000 | 270.00 | 486.00 | 743.00 |
| `S` | 611 | 0 | 11.9869 | 9.00 | 8.4891 | 1.000 | 5.00 | 16.00 | 45.00 |
| `CU` | 611 | 0 | 1.1913 | 0.748 | 1.4446 | 0.000 | 0.264 | 1.666 | 18.98 |
| `FC`* | 610 | 1 | 5.4104 | 3.699 | 5.2656 | 0.026 | 1.910 | 6.7295 | 42.98 |
| `MN`* | 610 | 1 | 10.5211 | 7.182 | 9.9720 | 0.000 | 3.580 | 14.1875 | 52.32 |
| `ZN` | 611 | 0 | 0.9259 | 0.516 | 1.2928 | 0.008 | 0.236 | 1.076 | 14.42 |
| `BA`* | 610 | 1 | 0.6044 | 0.256 | 3.9318 | 0.019 | 0.192 | 0.416 | 96.00 |
| `Temparature` | 611 | 0 | 33.9388 | 34.59 | 2.4652 | 28.000 | 32.70 | 36.03 | 37.50 |
| `Humidity` | 591 | 0 | 75.0755 | 72.59 | 13.7091 | 45.090 | 66.46 | 81.20 | 100.00 |
| `Rainfall` | 611 | 0 | 763.3398 | 751.40 | 89.9228 | 626.400 | 688.50 | 834.30 | 944.50 |

*\*Note: For `EC`, `FC`, `MN`, and `BA`, the single unconvertible typographical error was coerced to NaN solely to compute descriptive summary statistics. No dataset values were altered.*

---

## 12. Potential Data-Quality Issues
1. **Empty Spreadsheet Overflow:** 16,364 trailing empty columns in Excel.
2. **Missing Meteorological Observations:** 20 records (3.27%) missing `Humidity` data in Mandal Mydukur.
3. **Typographical String Contamination:** Four numerical laboratory measurements contain string typos (`'0..07'`, `'2..956'`, `'1.13.79'`, `'0..16'`).
4. **Severe Crop Label Fragmentation:** 61 raw classes, with spelling mistakes (`Blakgram`, `Tamota`, `grownut`, `Turemaric`, etc.) and regional dialect terms (`Allam`, `Korra`).
5. **Extreme Class Imbalance:** 14 crop classes have only a single observation ($N=1$), making conventional stratified $k$-fold cross-validation mathematically impossible without explicit consolidation or filtering.
6. **Severe Outliers / Potential Measurement Anomalies:**
   * `OC = 31.0%` at Row index 337 (normal soil organic carbon is typically under 1.5%; 31.0% is extraordinarily high).
   * `EC = 8.18 dS/m` at S.NO 348 (while typical values range between 0.01 and 1.35).
   * `N = 850.0 kg/ha` at S.NO 355 (3 records have $N > 500$, compared to mean of 220 kg/ha).
   * `P2O5 = 856 kg/ha` at S.NO 348 (compared to 75th percentile of 46 kg/ha).
   * `BA = 96.0 ppm` at S.NO 348 (compared to median of 0.256 ppm).
   * *Notice that S.NO 348 contains multiple simultaneous extreme spikes across EC, P2O5, and BA — Potential anomaly — needs verification.*
7. **Identifier Discrepancies:** Duplicate S.NO values (29, 65, 66) and index starting at 0.

---

## 13. Items Requiring Verification
All uncertain, ambiguous, or contradictory items identified during Step 1 inspection:

1. **Missing Humidity Resolution:**
   * Whether the 20 rows with missing humidity should be dropped (leaving 591 rows) or imputed using Mandal/regional medians: **Needs verification**.
2. **Numeric Typo Corrections:**
   * Whether `'0..07'` should be corrected to `0.07`: **Needs verification**.
   * Whether `'2..956'` should be corrected to `2.956`: **Needs verification**.
   * Whether `'1.13.79'` should be corrected to `11.379`, `1.138`, or median: **Needs verification**.
   * Whether `'0..16'` should be corrected to `0.16`: **Needs verification**.
3. **Crop Consolidation Strategy:**
   * Which exact mapping rules should be used to consolidate 61 raw labels into canonical crops, and whether singleton crops should be merged into broader categories or filtered: **Needs verification**.
4. **Exact Feature Subsets in Paper:**
   * The IEEE paper reports evaluation on "all features", "6 features", and "4 features", but nowhere lists which features belong to the 6- or 4-feature sets: **Needs verification**.
5. **Technical Meaning of Laboratory Abbreviations:**
   * Meaning of column `FC` (Field Capacity vs Iron/Ferric content): **Meaning requires verification from the original dataset/source.**
   * Meaning of column `BA` (Boron vs Barium): **Meaning requires verification from the original dataset/source.**
6. **Extreme Outliers:**
   * Whether records like S.NO 348 (EC=8.18, P2O5=856, BA=96.0) and Row 337 (OC=31.0) are valid extreme agro-chemical field conditions or lab recording errors: **Needs verification**.

---

## 14. Conclusion
Step 1 (Dataset Inspection) has been completed in strict accordance with scientific standards:
- The original Excel dataset remains **100% untouched and unmodified**.
- No machine learning models, cleaning pipelines, or synthetic imputations were executed.
- Programmatic inspection successfully cataloged all genuine agricultural columns, missing values, string anomalies, class distributions, and structural properties.
- All inspection artifacts, data profiles, dictionaries, and exploratory visualizations have been compiled and saved under `reports/`.

We are now ready to establish verified preprocessing rules in Step 2.
