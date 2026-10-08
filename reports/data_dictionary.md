# Data Dictionary: Agricultural Soil and Climate Dataset

**Dataset File:** `data/complete soil data.xlsx`  
**Sheet Name:** `complete soil data`  
**Total Records:** 611 data rows  
**Total Agricultural Columns:** 20 genuine non-empty columns (excluding 16,364 empty Excel artifact columns)  
**Geographic Scope:** Kadapa District, Andhra Pradesh, India  

---

## Agricultural Features Dictionary

| Column Name | Detected Data Type | Non-Null Count | Missing Count | Unique Count | Observed Range [Min, Max] | Preliminary Interpretation & Technical Notes |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`S.NO`** | `int64` | 611 | 0 | 608 | [0, 616] | Serial number assigned to records. Note: 3 duplicate values exist (29, 65, 66 appear twice); minimum starts at 0. |
| **`MANDAL NAME`** | `object` (string) | 611 | 0 | 27 | N/A | Administrative sub-district (Tehsil/Mandal) within Kadapa district (e.g., Jammalamadugu, Pendlimarri, Vempalli, Atloor). |
| **`VILLAGE NAME`** | `object` (string) | 611 | 0 | 231 | N/A | Administrative village or hamlet where soil sample was collected (e.g., Uppalapadu, Moragudi, Atloor). |
| **`SOIL TYPE`** | `int64` | 611 | 0 | 12 | [1, 13] | Numeric classification code representing soil taxonomy/texture. Mentioned in Section 3.4 of the IEEE paper. |
| **`PH`** | `float64` | 611 | 0 | 108 | [6.22, 8.90] | Soil pH value (potential of hydrogen), quantifying soil acidity/alkalinity. Primary feature used in paper and Flask app. |
| **`EC`** | `object` (string) | 611 | 0 | 57 | [0.005, 8.18]* | Electrical Conductivity in dS/m (indicator of soil salinity). Detected as `object` due to double-dot typo (`'0..07'` at row 244). High outlier: 8.18 at S.NO 348. Feature used in Flask deployment. |
| **`OC`** | `float64` | 611 | 0 | 37 | [0.015, 31.0] | Organic Carbon percentage (%) in the soil sample. High outlier: 31.0 at row index 337 (typical range: 0.1% to 1.14%). Potential anomaly — needs verification. |
| **`N`** | `float64` | 611 | 0 | 39 | [1.0, 850.0] | Available Nitrogen in soil (kg/ha). Key macronutrient. Evaluated in paper and Flask application. Contains 3 values > 500 (max: 850.0) — potential anomaly — needs verification. |
| **`P2O5`** | `int64` | 611 | 0 | 87 | [2, 856] | Available Phosphorus (Phosphate, $P_2O_5$) in soil (kg/ha). Corresponds to feature $P$ in IEEE paper and Flask application. |
| **`K20`** | `int64` | 611 | 0 | 106 | [5, 743] | Available Potassium (Potash, $K_2O$) in soil (kg/ha). Corresponds to feature $K$ in IEEE paper and Flask application. (Header uses digit zero `'0'`). |
| **`S`** | `int64` | 611 | 0 | 40 | [1, 45] | Available Sulphur content in soil (ppm). Secondary macronutrient. |
| **`CU`** | `float64` | 611 | 0 | 315 | [0.00, 18.98] | Available Copper content in soil (ppm). Micronutrient. |
| **`FC`** | `object` (string) | 611 | 0 | 437 | [0.026, 42.98]* | Abbreviation in soil lab reports. Could represent Field Capacity or Iron ($Fe$) / Ferric Content. Detected as `object` due to double-dot typo (`'2..956'` at row 241). **Meaning requires verification from the original dataset/source.** |
| **`MN`** | `object` (string) | 611 | 0 | 531 | [0.00, 52.32]* | Available Manganese content in soil (ppm). Micronutrient. Detected as `object` due to multi-decimal malformed string (`'1.13.79'` at row 54). |
| **`ZN`** | `float64` | 611 | 0 | 359 | [0.008, 14.42] | Available Zinc content in soil (ppm). Micronutrient. |
| **`BA`** | `object` (string) | 611 | 0 | 89 | [0.019, 96.0]* | Abbreviation in soil lab reports. Could represent Boron ($B$) or Barium ($Ba$). Detected as `object` due to double-dot typo (`'0..16'` at row 228). High outlier: 96.0. **Meaning requires verification from the original dataset/source.** |
| **`Temparature`** | `float64` | 611 | 0 | 23 | [28.0, 37.5] | Local ambient mean temperature in °C. (Header spelled `'Temparature'`). Core agro-climatic feature used in paper and Flask app. |
| **`Humidity`** | `float64` | 591 | 20 (3.27%) | 22 | [45.09, 100.0] | Relative humidity percentage (%). Contains 20 missing (`NaN`) values in Mandal Mydukur (rows 266–285). Core feature used in paper and Flask app. |
| **`Rainfall`** | `float64` | 611 | 0 | 26 | [626.4, 944.5] | Mean seasonal/annual precipitation in mm. Core feature used in paper and Flask app. |
| **`CROP`** | `object` (string) | 611 | 0 | 61 | N/A | Target recommendation output label. Contains 61 raw categories with case/spelling variations and 8 singleton classes. |

*\*Note: Minimum and maximum for `EC`, `FC`, `MN`, `BA` were calculated by coercing the single unconvertible typo in each column to NaN for statistical profiling only without modifying the underlying dataset.*

---

## Discarded Artifact Columns

* **Columns `Column1` through `Column16364`:** Exactly 16,364 trailing empty columns spanning up to Excel's table dimension ceiling ($2^{14} = 16,384$). Every single cell contains `NaN`. These columns carry no data or information and are programmatically excluded.
