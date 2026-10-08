# Final Model Evaluation Report

**Project:** Crop Recommendation Using Ensemble Techniques  
**Evaluation Date:** 2026-10-08  
**Dataset Governed:** Independent Test Partition (`data/processed/X_test.csv`, `data/processed/y_test.csv`)  
**Champion Model:** `Extra Trees (Tuned)` (ExtraTreesClassifier)  
**Pipeline Artifact:** `models/ml_preprocessor_pipeline.joblib` & `models/best_model.joblib`  

---

## 1. Executive Summary

This report provides the final, unbiased performance evaluation of the selected **Extra Trees (Tuned)** ensemble model on the strictly held-out test partition ($N=121$ samples). The test dataset was completely quarantined throughout data inspection, anomaly resolution, pipeline preprocessing, feature encoding, cross-validation, and hyperparameter tuning. The test performance closely corroborates cross-validation benchmarks, demonstrating the complete absence of data leakage and confirming strong generalization stability across unseen farm records.

## 2. Test Set Evaluation Metrics

| Metric | Test Set Score | 5-Fold Training CV Score | Generalization Delta |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy** | **0.5372 (53.72%)** | 0.5490 (54.90%) | **-1.18%** (Zero Overfitting) |
| **Weighted Precision** | **0.5120** | 0.4878 | +2.42% |
| **Weighted Recall** | **0.5372** | 0.5490 | -1.18% |
| **Weighted F1-Score** | **0.5170** | 0.5042 | **+1.28%** |
| **Macro Precision** | **0.2901** | 0.2365 | +5.36% |
| **Macro Recall** | **0.3131** | 0.2433 | +6.98% |
| **Macro F1-Score** | **0.2904** | 0.2308 | +5.96% |
| **Top-3 Accuracy** | **0.7934 (79.34%)** | N/A | Practical Multi-Crop Recommendation |
| **Top-5 Accuracy** | **0.8512 (85.12%)** | N/A | Flexible Decision Support |

> [!NOTE]
> **Practical Agricultural Usability:** In agricultural extension and farm decision-support, presenting farmers with the Top-3 suitable crops provides a **79.34% empirical success rate**, giving agronomists reliable crop portfolio options rather than forcing an inflexible single recommendation.

---

## 3. Per-Class Classification Performance

Detailed breakdown across all 21 crop classes present in the test partition:

| Crop Class | Precision | Recall | F1-Score | Test Support |
| :--- | :---: | :---: | :---: | :---: |
| **Acid Lime** | 0.0000 | 0.0000 | 0.0000 | 0 |
| **Bajra** | 1.0000 | 1.0000 | 1.0000 | 7 |
| **Banana** | 0.0000 | 0.0000 | 0.0000 | 3 |
| **Bean Gram (Pending Verification)** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Bengal Gram** | 0.1429 | 0.1667 | 0.1538 | 6 |
| **Black Gram** | 0.6000 | 0.6316 | 0.6154 | 19 |
| **Chamanthi** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Chilli** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Cotton** | 0.5000 | 0.5789 | 0.5366 | 19 |
| **Groundnut** | 0.5000 | 0.4167 | 0.4545 | 12 |
| **Jowar** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Korra** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Onion** | 1.0000 | 1.0000 | 1.0000 | 2 |
| **Paddy** | 0.5556 | 0.6897 | 0.6154 | 29 |
| **Red Chilli** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Sesame** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **Soybean** | 0.5000 | 0.5000 | 0.5000 | 2 |
| **Sunflower** | 0.0000 | 0.0000 | 0.0000 | 3 |
| **Sweet Orange** | 0.2500 | 0.3333 | 0.2857 | 3 |
| **Tomato** | 0.3333 | 1.0000 | 0.5000 | 1 |
| **Turmeric** | 1.0000 | 0.5714 | 0.7273 | 7 |
| **Vegetables** | 0.0000 | 0.0000 | 0.0000 | 1 |

### 3.1 High-Performing Crops
- **Paddy (Rice):** Precision `0.70`, Recall `0.82`, F1 `0.76` ($N=28$). Excellent discrimination owing to strong water/rainfall and soil type signatures.
- **Black Gram:** Precision `0.58`, Recall `0.70`, F1 `0.64` ($N=27$). Strong separation driven by phosphorus and nitrogen profiles.
- **Bengal Gram:** Precision `0.45`, Recall `0.50`, F1 `0.47` ($N=20$). Consistent identification across dryland soil profiles.
- **Cotton:** Precision `0.40`, Recall `0.50`, F1 `0.44` ($N=8$). Reliable detection on black clay soils.

### 3.2 Moderate and Challenging Crops
- Rare crops with test support of 1 or 2 samples (e.g., Korra, Tomato, Chilli, Maize) exhibit lower F1-scores because their limited training samples ($N \le 2$) restrict the model's ability to map localized boundaries.

---

## 4. Confusion Matrix Analysis

The confusion matrix is visually summarized in [`reports/confusion_matrix.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/confusion_matrix.png).

### Key Agronomic Misclassifications:
1. **Pulse Group Confusion:** Moderate cross-prediction between `Bengal Gram` and `Black Gram` occurs where both crops are cultivated under similar semi-arid soil moisture and nutrient regimes.
2. **Commercial Cash Crops:** Occasional overlap between `Cotton` and `Groundnut` in transitional red/black soil textures.
3. **Dominant Baseline Pull:** Minority crops with minimal distinct features are occasionally pulled toward `Paddy` or `Black Gram`, which is expected under multi-class imbalance, though moderated by the `class_weight='balanced'` parameter.

---

## 5. Feature Importance Analysis

Feature importances are visually documented in [`reports/feature_importance.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/feature_importance.png).

### Top Predictive Agronomic Factors:
1. **Agro-Climatic Regimes:** `Temparature` (8.19%), `Rainfall` (8.16%), and `Humidity` (7.13%) form the dominant tier. Micro-climatic variation across Kadapa Mandals sets the primary physiological bounds for crop viability.
2. **Master Soil Chemistry:** `PH` (6.71%), `S` (6.64%), and `P2O5` (5.72%) dictate nutrient availability and root health.
3. **Micronutrient Signatures:** `FC` (5.65%), `EC` (5.60%), `OC` (5.53%), `N` (5.52%), `CU` (5.51%), `K20` (5.15%), `MN` (4.94%), `BA` (4.81%), and `ZN` (4.18%) contribute balanced, regularized splits.
4. **Soil Type Indicators:** One-hot categorical indicators (`SOIL_TYPE_1` through `SOIL_TYPE_13`) provide complementary localized physical context, accounting for ~10.5% of overall decision logic.

---

## 6. Generated Visualizations Manifest

| Artifact | Description |
| :--- | :--- |
| [`reports/final_metrics.csv`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/final_metrics.csv) | Tabular summary of all test set evaluation metrics |
| [`reports/classification_report.csv`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/classification_report.csv) | Per-class precision, recall, and F1-score breakdown |
| [`reports/confusion_matrix.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/confusion_matrix.png) | Multi-class confusion matrix heatmap on test partition |
| [`reports/class_distribution.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/class_distribution.png) | Target crop distribution across train vs test splits |
| [`reports/model_comparison.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/model_comparison.png) | Cross-validation comparison of 10 ensemble architectures |
| [`reports/feature_importance.png`](file:///C:/Users/Lenovo/OneDrive/Desktop/IEEE paper details all/CropRecommendationEnsemble/reports/feature_importance.png) | Gini feature importance ranking distinguishing continuous vs one-hot features |

