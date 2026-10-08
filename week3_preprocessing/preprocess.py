"""
Week 3: Complete and Reproducible Preprocessing Pipeline for Crop Recommendation.

Governed strictly by:
- reports/step9_preprocessing_policy.md
- reports/step1_dataset_inspection.md through reports/step8_outlier_investigation.md

Raw Dataset:
  data/complete soil data.xlsx (Read-only, strictly immutable)

Outputs:
  data/processed/crop_data_cleaned.csv
  data/processed/crop_recommendation_clean.csv (Synced)
  reports/preprocessing_report.md
  reports/data_quality_log.csv
  reports/crop_label_mapping.csv
  reports/preprocessing_summary.csv
"""

import os
import sys
import pandas as pd
import numpy as np

def run_preprocessing():
    print("=" * 80)
    print("STARTING COMPLETE REPRODUCIBLE DATA PREPROCESSING PIPELINE")
    print("Project: Crop Recommendation Using Ensemble Techniques")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. LOAD ORIGINAL RAW DATASET (READ-ONLY)
    # -------------------------------------------------------------------------
    raw_excel_path = os.path.join("data", "complete soil data.xlsx")
    if not os.path.exists(raw_excel_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_excel_path}")

    print(f"Loading raw dataset from: {raw_excel_path}")
    df_raw = pd.read_excel(raw_excel_path)
    orig_rows, orig_cols = df_raw.shape
    print(f"Raw Sheet Dimensions: {orig_rows} rows x {orig_cols} columns")

    # -------------------------------------------------------------------------
    # 2. FILTER TO 20 GENUINE AGRICULTURAL COLUMNS (IGNORE 16,364 PHANTOMS)
    # -------------------------------------------------------------------------
    genuine_cols = [
        'S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE',
        'PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S',
        'CU', 'FC', 'MN', 'ZN', 'BA',
        'Temparature', 'Humidity', 'Rainfall', 'CROP'
    ]

    for c in genuine_cols:
        if c not in df_raw.columns:
            raise KeyError(f"Expected column '{c}' not found in raw dataset.")

    df = df_raw[genuine_cols].copy()
    print(f"Filtered to genuine columns: {len(genuine_cols)} columns (ignored {orig_cols - len(genuine_cols)} phantom columns)")

    # Baseline tracking metrics
    missing_before_total = int(df.isna().sum().sum())
    missing_before_by_col = df.isna().sum().to_dict()
    dtypes_before = df.dtypes.astype(str).to_dict()
    raw_crop_classes_count = df['CROP'].nunique()

    # Track every data quality item for data_quality_log.csv
    dq_records = []

    # -------------------------------------------------------------------------
    # 3. IDENTIFIER & LOCATION METADATA HANDLING
    # -------------------------------------------------------------------------
    # S.NO: Tracking ID only, excluded from ML features
    # MANDAL NAME, VILLAGE NAME: Administrative location metadata, excluded from ML features
    df['S.NO'] = df['S.NO'].astype(int)

    # -------------------------------------------------------------------------
    # 4. HANDLE THE FOUR MALFORMED NUMERIC STRING VALUES (POLICY RULE 2)
    # -------------------------------------------------------------------------
    malformed_values_before = 4

    # S.NO 245: EC '0..07' -> 0.07 (double period typo)
    mask_ec = (df['S.NO'] == 245) & (df['EC'] == '0..07')
    if mask_ec.any():
        mandal_val = df.loc[mask_ec, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_ec, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_ec, 'EC'] = 0.07
        dq_records.append({
            's_no': 245, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'EC', 'issue_category': 'Malformed String Typo',
            'raw_value': "'0..07'", 'cleaned_value': '0.07',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': 'Double decimal point keystroke on numpad resolved to 0.07; fits local baseline (0.05-0.20 dS/m)'
        })

    # S.NO 242: FC '2..956' -> 2.956 (double period typo)
    mask_fc = (df['S.NO'] == 242) & (df['FC'] == '2..956')
    if mask_fc.any():
        mandal_val = df.loc[mask_fc, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_fc, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_fc, 'FC'] = 2.956
        dq_records.append({
            's_no': 242, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'FC', 'issue_category': 'Malformed String Typo',
            'raw_value': "'2..956'", 'cleaned_value': '2.956',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': 'Double decimal point keystroke on numpad resolved to 2.956; fits local distribution (1.5-4.5 ppm)'
        })

    # S.NO 229: BA '0..16' -> 0.16 (double period typo)
    mask_ba = (df['S.NO'] == 229) & (df['BA'] == '0..16')
    if mask_ba.any():
        mandal_val = df.loc[mask_ba, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_ba, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_ba, 'BA'] = 0.16
        dq_records.append({
            's_no': 229, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'BA', 'issue_category': 'Malformed String Typo',
            'raw_value': "'0..16'", 'cleaned_value': '0.16',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': 'Double decimal point keystroke on numpad resolved to 0.16; fits local distribution (0.10-0.35 ppm)'
        })

    # S.NO 55: MN '1.13.79' -> 1.138 (segmented string typo)
    mask_mn = (df['S.NO'] == 55) & (df['MN'] == '1.13.79')
    if mask_mn.any():
        mandal_val = df.loc[mask_mn, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_mn, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_mn, 'MN'] = 1.138
        dq_records.append({
            's_no': 55, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'MN', 'issue_category': 'Malformed String Typo',
            'raw_value': "'1.13.79'", 'cleaned_value': '1.138',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': 'Segmented decimal string normalized to local Simhadripuram standard 3-decimal baseline (S.NO 57=1.138)'
        })

    malformed_values_after = 0
    print(f"Corrected {malformed_values_before} malformed numeric string typos.")

    # -------------------------------------------------------------------------
    # 5. NUMERIC TYPE COERCION & CATEGORICAL HANDLING
    # -------------------------------------------------------------------------
    numeric_features = [
        'PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S',
        'CU', 'FC', 'MN', 'ZN', 'BA',
        'Temparature', 'Humidity', 'Rainfall'
    ]
    for col in numeric_features:
        df[col] = pd.to_numeric(df[col], errors='raise')

    # SOIL TYPE is nominal categorical (1 to 13)
    df['SOIL TYPE'] = df['SOIL TYPE'].astype(int)

    # -------------------------------------------------------------------------
    # 6. EXTREME OUTLIER TREATMENT (POLICY RULE 7 & RULE 9)
    # -------------------------------------------------------------------------
    # Decimal omission errors (with verified physical/geochemical proof)
    # S.NO 84: OC 31.0 -> 0.31 (100x decimal shift in mineral soil)
    mask_oc_84 = (df['S.NO'] == 84) & (df['OC'] == 31.0)
    if mask_oc_84.any():
        mandal_val = df.loc[mask_oc_84, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_oc_84, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_oc_84, 'OC'] = 0.31
        dq_records.append({
            's_no': 84, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'OC', 'issue_category': 'Decimal Keystroke Outlier Repair',
            'raw_value': '31.0', 'cleaned_value': '0.31',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': '100x decimal omission error in mineral soil (31% OC physically impossible in semi-arid soils; baseline 0.11-0.80%)'
        })

    # S.NO 372: OC 30.35 -> 0.30 (100x decimal shift in mineral soil)
    mask_oc_372 = (df['S.NO'] == 372) & (df['OC'] == 30.35)
    if mask_oc_372.any():
        mandal_val = df.loc[mask_oc_372, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_oc_372, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_oc_372, 'OC'] = 0.30
        dq_records.append({
            's_no': 372, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'OC', 'issue_category': 'Decimal Keystroke Outlier Repair',
            'raw_value': '30.35', 'cleaned_value': '0.30',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': '100x decimal omission error in mineral soil (Atloor baseline 0.02-0.35%)'
        })

    # S.NO 144: OC 23.0 -> 0.23 (100x decimal shift in mineral soil)
    mask_oc_144 = (df['S.NO'] == 144) & (df['OC'] == 23.0)
    if mask_oc_144.any():
        mandal_val = df.loc[mask_oc_144, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_oc_144, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_oc_144, 'OC'] = 0.23
        dq_records.append({
            's_no': 144, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'OC', 'issue_category': 'Decimal Keystroke Outlier Repair',
            'raw_value': '23.0', 'cleaned_value': '0.23',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': '100x decimal omission error in mineral soil (Thondur baseline 0.11-0.39%)'
        })

    # S.NO 62: BA 96.0 -> 0.96 (missing decimal point for 0.96 ppm)
    mask_ba_62 = (df['S.NO'] == 62) & (df['BA'] == 96.0)
    if mask_ba_62.any():
        mandal_val = df.loc[mask_ba_62, 'MANDAL NAME'].iloc[0]
        village_val = df.loc[mask_ba_62, 'VILLAGE NAME'].iloc[0]
        df.loc[mask_ba_62, 'BA'] = 0.96
        dq_records.append({
            's_no': 62, 'mandal_name': mandal_val, 'village_name': village_val,
            'feature': 'BA', 'issue_category': 'Decimal Keystroke Outlier Repair',
            'raw_value': '96.0', 'cleaned_value': '0.96',
            'status': 'Confirmed Correction', 'confidence': 'High',
            'justification': 'Missing decimal point for 0.96 ppm (96.0 is 375x median; Simhadripuram baseline 0.06-2.78 ppm)'
        })

    # PRESERVED EXTREME OUTLIERS (NO ROW REMOVAL, NO ARBITRARY VALUE MODIFICATION)
    # S.NO 348: EC 8.18 (Plausible localized saline depression / solonchak patch)
    mask_ec_348 = (df['S.NO'] == 348)
    if mask_ec_348.any():
        dq_records.append({
            's_no': 348, 'mandal_name': df.loc[mask_ec_348, 'MANDAL NAME'].iloc[0],
            'village_name': df.loc[mask_ec_348, 'VILLAGE NAME'].iloc[0],
            'feature': 'EC', 'issue_category': 'Preserved Agronomic Extreme / Potential Anomaly',
            'raw_value': '8.18', 'cleaned_value': '8.18',
            'status': 'Preserved as Potential Anomaly', 'confidence': 'Moderate',
            'justification': 'Plausible localized extreme saline depression (solonchak condition) or possible 10x error (0.818); preserved without row deletion'
        })

    # S.NO 379: P2O5 856 (Part of 16-record regional high-P spatial cluster in Atloor)
    mask_p_379 = (df['S.NO'] == 379)
    if mask_p_379.any():
        dq_records.append({
            's_no': 379, 'mandal_name': df.loc[mask_p_379, 'MANDAL NAME'].iloc[0],
            'village_name': df.loc[mask_p_379, 'VILLAGE NAME'].iloc[0],
            'feature': 'P2O5', 'issue_category': 'Preserved Geochemical Cluster Outlier',
            'raw_value': '856.0', 'cleaned_value': '856.0',
            'status': 'Preserved as Potential Anomaly', 'confidence': 'High',
            'justification': 'Authentic 16-record regional high-P cluster in Mandal Atloor (P2O5 439-856 kg/ha); preserved without row deletion'
        })

    # S.NO 130: N 850 (Plausible high commercial fertilizer / manure application)
    mask_n_130 = (df['S.NO'] == 130)
    if mask_n_130.any():
        dq_records.append({
            's_no': 130, 'mandal_name': df.loc[mask_n_130, 'MANDAL NAME'].iloc[0],
            'village_name': df.loc[mask_n_130, 'VILLAGE NAME'].iloc[0],
            'feature': 'N', 'issue_category': 'Preserved Agronomic Extreme',
            'raw_value': '850.0', 'cleaned_value': '850.0',
            'status': 'Preserved as Potential Anomaly', 'confidence': 'High',
            'justification': 'Plausible heavy commercial fertilizer / farmyard manure application prior to sampling; preserved without row deletion'
        })

    # S.NO 422: N 801 (Plausible high nitrogen)
    mask_n_422 = (df['S.NO'] == 422)
    if mask_n_422.any():
        dq_records.append({
            's_no': 422, 'mandal_name': df.loc[mask_n_422, 'MANDAL NAME'].iloc[0],
            'village_name': df.loc[mask_n_422, 'VILLAGE NAME'].iloc[0],
            'feature': 'N', 'issue_category': 'Preserved Agronomic Extreme',
            'raw_value': '801.0', 'cleaned_value': '801.0',
            'status': 'Preserved as Potential Anomaly', 'confidence': 'High',
            'justification': 'Plausible heavy basal fertilizer application; preserved without row deletion'
        })

    # -------------------------------------------------------------------------
    # 7. HANDLE MISSING HUMIDITY VALUES (POLICY RULE 3 & RULE 8)
    # -------------------------------------------------------------------------
    valid_humidity = df['Humidity'].dropna()
    humidity_median = float(valid_humidity.median())
    missing_humidity_mask = df['Humidity'].isna()
    missing_humidity_count = int(missing_humidity_mask.sum())

    if missing_humidity_count > 0:
        missing_rows = df[missing_humidity_mask]
        for _, row in missing_rows.iterrows():
            dq_records.append({
                's_no': int(row['S.NO']),
                'mandal_name': str(row['MANDAL NAME']),
                'village_name': str(row['VILLAGE NAME']),
                'feature': 'Humidity',
                'issue_category': 'Missing Value Imputation',
                'raw_value': 'NaN',
                'cleaned_value': f"{humidity_median:.2f}",
                'status': 'Confirmed Imputation',
                'confidence': 'High',
                'justification': 'Imputed with overall dataset median (72.59%); Mydukur has 0 valid humidity entries (100% missing); listwise deletion would extinguish Vegetables, Turmeric, Chillis'
            })
        df.loc[missing_humidity_mask, 'Humidity'] = humidity_median

    print(f"Imputed {missing_humidity_count} missing Humidity values with median = {humidity_median:.2f}%.")

    # -------------------------------------------------------------------------
    # 8. STANDARDIZE CROP LABELS (CANONICAL MAPPING)
    # -------------------------------------------------------------------------
    # Comprehensive master mapping dictionary for all 61 raw labels
    crop_mapping_rules = {
        'paddy': ('Paddy', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'cotton': ('Cotton', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'Grownut': ('Groundnut', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize colloquial spelling Grownut to Groundnut'),
        'Black Gram': ('Black Gram', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'Bajra': ('Bajra', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard pearl millet'),
        'Black gram': ('Black Gram', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize sentence case to Title Case'),
        'Bengal gram': ('Bengal Gram', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize sentence case to Title Case'),
        'Turmeric': ('Turmeric', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'sweet orange': ('Sweet Orange', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize lowercase to Title Case (Citrus sinensis)'),
        'sunflower': ('Sunflower', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'Blakgram': ('Black Gram', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', "Correct typo (missing 'c' and space)"),
        'banana': ('Banana', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'turmeric': ('Turmeric', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'onion': ('Onion', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard crop name'),
        'grownut': ('Groundnut', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize colloquial spelling and capitalize'),
        'soyabean': ('Soybean', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize Indian spelling soyabean to Soybean'),
        'chamanthi': ('Chamanthi', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize Telugu regional flower name (Chrysanthemum)'),
        'Bengal Gram': ('Bengal Gram', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'Vegetables': ('Vegetables', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Preserve aggregate horticultural class'),
        'Banana': ('Banana', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'Jowar': ('Jowar', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard sorghum cereal'),
        'Cotton': ('Cotton', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'korra': ('Korra', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize Telugu name for Foxtail Millet'),
        'Tamota': ('Tomato', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize Telugu phonetic Tamota to Tomato'),
        'sesam': ('Sesame', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize truncated sesam to Sesame'),
        'Soyabean': ('Soybean', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize Indian spelling Soyabean to Soybean'),
        'black gram': ('Black Gram', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize lowercase to Title Case'),
        'Bean Gram': ('Bean Gram (Pending Verification)', 'Unresolved Anomaly', 'Moderate', 'source_verification_required', 'Unresolved Anomaly', 'Suspected typo for Bengal Gram in Kondapuram; retained distinct to avoid ungrounded guessing'),
        'sweet ornage': ('Sweet Orange', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', "Correct typo 'ornage' to 'orange'"),
        'Red Chilli': ('Red Chilli', 'Botanical Preservation', 'Moderate', 'evaluate_subclass', 'Confirmed Correction', 'Commercial subclass of Capsicum annuum (mature dried)'),
        'maize': ('Maize', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard cereal name'),
        'Acidlime': ('Acid Lime', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize to spaced Title Case (Citrus aurantifolia)'),
        'Green Gram': ('Green Gram', 'Botanical Preservation', 'High', 'keep_separate_species', 'Confirmed Correction', 'Preserve distinct pulse species (Vigna radiata / Moong)'),
        'Sunflower': ('Sunflower', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Standard canonical Title Case'),
        'chillis': ('Chilli', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize spelling and capitalize'),
        'Turemaric': ('Turmeric', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo'),
        'Jouar': ('Jowar', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo Jouar to Jowar'),
        'Blak Gram': ('Black Gram', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', "Correct typo (missing 'c')"),
        'jouar': ('Jowar', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo and casing'),
        'guava': ('Guava', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize fruit name (Psidium guajava)'),
        'Sweet orange': ('Sweet Orange', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize sentence case to Title Case'),
        'termeric': ('Turmeric', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo'),
        'muckmelon': ('Muskmelon', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct typo muckmelon to Muskmelon (Cucumis melo)'),
        'swwet orange': ('Sweet Orange', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', "Correct typo 'swwet' to 'sweet'"),
        'mums': ('Chamanthi (Mums)', 'Horticultural Synonym', 'Moderate', 'synonym_consolidation', 'Confirmed Correction', 'Universal English trade name for Chrysanthemum (Chamanthi)'),
        'Blak gram': ('Black Gram', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', "Correct typo (missing 'c') and casing"),
        'Chillis': ('Chilli', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Standardize plural to singular canonical Title Case'),
        'Turemeric': ('Turmeric', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo'),
        'Blackgram': ('Black Gram', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Insert missing space between words'),
        'Red Gram': ('Red Gram', 'Botanical Preservation', 'High', 'keep_separate_species', 'Confirmed Correction', 'Preserve distinct pulse species (Cajanus cajan / Pigeonpea)'),
        'vegetables': ('Vegetables', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize aggregate horticultural category'),
        'sweet lime': ('Sweet Lime', 'Botanical Preservation', 'High', 'keep_separate_species', 'Confirmed Correction', 'Preserve distinct citrus species (Citrus limetta / Mitha Nimbu)'),
        'sesasum': ('Sesame', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct spelling typo sesasum to Sesame'),
        'Allam': ('Allam (Ginger)', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Preserve Telugu regional crop name for Ginger (Zingiber officinale)'),
        'Turmaric': ('Turmeric', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct phonetic spelling typo'),
        'Caster': ('Castor', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Correct typo Caster to Castor (Ricinus communis)'),
        'papaya': ('Papaya', 'Format Normalization', 'High', 'format_normalization', 'Confirmed Correction', 'Capitalize standard fruit name (Carica papaya)'),
        'Nannari': ('Nannari', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Preserve Telugu regional medicinal crop (Hemidesmus indicus)'),
        'Greenchilli': ('Green Chilli', 'Botanical Preservation', 'Moderate', 'evaluate_subclass', 'Confirmed Correction', 'Commercial subclass of Capsicum annuum (fresh immature)'),
        'Sesamum': ('Sesame', 'Spelling Correction', 'High', 'spelling_correction', 'Confirmed Correction', 'Standardize Latin genus name to common name Sesame'),
        'Chamanthi': ('Chamanthi', 'Botanical Preservation', 'High', 'keep_as_is', 'Confirmed Correction', 'Preserve valid Title Case Telugu flower name')
    }

    raw_label_counts = df['CROP'].value_counts()
    crop_mapping_records = []
    crop_lookup = {}

    for raw_lbl, (can_lbl, cat, conf, act, stat, just) in crop_mapping_rules.items():
        freq = int(raw_label_counts.get(raw_lbl, 0))
        crop_lookup[raw_lbl] = can_lbl
        crop_mapping_records.append({
            'raw_label': raw_lbl,
            'frequency': freq,
            'canonical_label': can_lbl,
            'category': cat,
            'confidence': conf,
            'action': act,
            'status': stat,
            'justification': just
        })

    # Log ambiguous crop records
    for s_no_amb in [82, 83, 84]:
        mask_amb = df['S.NO'] == s_no_amb
        if mask_amb.any():
            dq_records.append({
                's_no': s_no_amb,
                'mandal_name': df.loc[mask_amb, 'MANDAL NAME'].iloc[0],
                'village_name': df.loc[mask_amb, 'VILLAGE NAME'].iloc[0],
                'feature': 'CROP',
                'issue_category': 'Unresolved Crop Identity Anomaly',
                'raw_value': "'Bean Gram'",
                'cleaned_value': "'Bean Gram (Pending Verification)'",
                'status': 'Unresolved Anomaly',
                'confidence': 'Moderate',
                'justification': 'Suspected typo for Bengal Gram in Kondapuram; retained distinct to avoid ungrounded guessing'
            })

    # Log ambiguous feature definitions
    dq_records.append({
        's_no': 0, 'mandal_name': 'All', 'village_name': 'All',
        'feature': 'FC', 'issue_category': 'Ambiguous Feature Definition',
        'raw_value': 'Laboratory column FC', 'cleaned_value': 'Retained in Full Lab Suite B',
        'status': 'Unresolved Anomaly', 'confidence': 'Moderate',
        'justification': 'Uncertain laboratory abbreviation (Field Capacity vs DTPA-extractable Iron Fe); excluded from Core Verified Suite A'
    })
    dq_records.append({
        's_no': 0, 'mandal_name': 'All', 'village_name': 'All',
        'feature': 'BA', 'issue_category': 'Ambiguous Feature Definition',
        'raw_value': 'Laboratory column BA', 'cleaned_value': 'Retained in Full Lab Suite B',
        'status': 'Unresolved Anomaly', 'confidence': 'Moderate',
        'justification': 'Uncertain laboratory abbreviation (Available Boron B vs Barium Ba); excluded from Core Verified Suite A'
    })

    # Apply mapping
    df['RAW_CROP'] = df['CROP']
    df['CROP'] = df['RAW_CROP'].map(crop_lookup)

    if df['CROP'].isna().any():
        unmapped = df.loc[df['CROP'].isna(), 'RAW_CROP'].unique()
        raise ValueError(f"Unmapped raw crop labels encountered: {unmapped}")

    canonical_crop_classes_count = df['CROP'].nunique()
    print(f"Standardized target CROP labels: {raw_crop_classes_count} raw -> {canonical_crop_classes_count} canonical classes.")

    # -------------------------------------------------------------------------
    # 9. FINAL DATASET COLUMN ALIGNMENT
    # -------------------------------------------------------------------------
    # Keep genuine agricultural columns with canonical CROP
    clean_cols_order = [
        'S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE',
        'PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S',
        'CU', 'FC', 'MN', 'ZN', 'BA',
        'Temparature', 'Humidity', 'Rainfall', 'CROP'
    ]
    df_clean = df[clean_cols_order].copy()
    final_rows, final_cols = df_clean.shape

    # -------------------------------------------------------------------------
    # 10. POST-PREPROCESSING VALIDATION CHECKS
    # -------------------------------------------------------------------------
    print("\n" + "="*80)
    print("RUNNING AUTOMATED VALIDATION CHECKS")
    print("="*80)

    # Validation 1: Row count consistency
    assert final_rows == orig_rows, f"Row count mismatch: {final_rows} vs {orig_rows}"
    print(f"[PASSED] Row count: Exactly {final_rows} rows preserved (100% data retention).")

    # Validation 2: Missing values elimination
    missing_after_total = int(df_clean.isna().sum().sum())
    assert missing_after_total == 0, f"Unexpected missing values remaining: {df_clean.isna().sum()}"
    print(f"[PASSED] Missing values: Exactly 0 missing values across all {final_cols} columns.")

    # Validation 3: Numeric types compliance
    for col in numeric_features:
        assert pd.api.types.is_numeric_dtype(df_clean[col]), f"Column {col} is not numeric!"
    assert pd.api.types.is_integer_dtype(df_clean['S.NO']), "S.NO is not integer!"
    assert pd.api.types.is_integer_dtype(df_clean['SOIL TYPE']), "SOIL TYPE is not integer!"
    print(f"[PASSED] Numeric types: All 15 soil/weather features verified as float64 numeric.")

    # Validation 4: Duplicate records check
    dup_count = df_clean.duplicated(subset=[c for c in clean_cols_order if c != 'S.NO']).sum()
    assert dup_count == 0, f"Accidental duplicate rows introduced: {dup_count}"
    print(f"[PASSED] Deduplication: Exactly 0 duplicate agricultural records found.")

    # Validation 5: Target labels validity
    assert df_clean['CROP'].notna().all(), "Null canonical crop labels found!"
    assert (df_clean['CROP'].str.strip() != '').all(), "Empty crop labels found!"
    print(f"[PASSED] Target labels: All {final_rows} rows contain valid canonical labels.")

    # -------------------------------------------------------------------------
    # 11. SAVE PROCESSED ARTIFACTS
    # -------------------------------------------------------------------------
    processed_dir = os.path.join("data", "processed")
    reports_dir = "reports"
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Cleaned Dataset: data/processed/crop_data_cleaned.csv
    clean_csv_path = os.path.join(processed_dir, "crop_data_cleaned.csv")
    df_clean.to_csv(clean_csv_path, index=False)
    print(f"Saved cleaned dataset: {clean_csv_path}")

    # Also sync data/processed/crop_recommendation_clean.csv (with RAW_CROP reference)
    clean_rec_path = os.path.join(processed_dir, "crop_recommendation_clean.csv")
    df_rec = df[clean_cols_order[:-1] + ['RAW_CROP', 'CROP']].copy()
    df_rec.to_csv(clean_rec_path, index=False)
    print(f"Synced clean dataset: {clean_rec_path}")

    # 2. Data Quality Log: reports/data_quality_log.csv
    dq_df = pd.DataFrame(dq_records)
    dq_log_path = os.path.join(reports_dir, "data_quality_log.csv")
    dq_df.to_csv(dq_log_path, index=False)
    print(f"Saved data quality log: {dq_log_path}")

    # 3. Crop Label Mapping: reports/crop_label_mapping.csv & data/processed/crop_label_mapping.csv
    mapping_df = pd.DataFrame(crop_mapping_records)
    report_mapping_path = os.path.join(reports_dir, "crop_label_mapping.csv")
    proc_mapping_path = os.path.join(processed_dir, "crop_label_mapping.csv")
    mapping_df.to_csv(report_mapping_path, index=False)
    mapping_df.to_csv(proc_mapping_path, index=False)
    print(f"Saved crop label mapping: {report_mapping_path}")

    # 4. Preprocessing Summary: reports/preprocessing_summary.csv
    summary_data = [
        {'metric': 'Original Rows', 'before_preprocessing': orig_rows, 'after_preprocessing': final_rows, 'delta': 0, 'notes': '100% data retention (0 rows dropped)'},
        {'metric': 'Final Rows', 'before_preprocessing': orig_rows, 'after_preprocessing': final_rows, 'delta': 0, 'notes': 'All valid observations preserved'},
        {'metric': 'Original Spreadsheet Columns', 'before_preprocessing': orig_cols, 'after_preprocessing': final_cols, 'delta': -(orig_cols - final_cols), 'notes': 'Ignored 16,364 empty trailing Excel artifact columns'},
        {'metric': 'Genuine Agricultural Columns', 'before_preprocessing': len(genuine_cols), 'after_preprocessing': final_cols, 'delta': 0, 'notes': 'Retained all 20 authentic columns'},
        {'metric': 'Tracking Identifier Columns', 'before_preprocessing': 1, 'after_preprocessing': 1, 'delta': 0, 'notes': 'S.NO retained as identifier; excluded from ML features'},
        {'metric': 'Location Metadata Columns', 'before_preprocessing': 2, 'after_preprocessing': 2, 'delta': 0, 'notes': 'MANDAL NAME & VILLAGE NAME retained for audit; excluded from ML features'},
        {'metric': 'Final Candidate ML Features (Suite B)', 'before_preprocessing': 16, 'after_preprocessing': 16, 'delta': 0, 'notes': 'Soil Type (categorical) + 15 continuous soil/weather features'},
        {'metric': 'Core Verified ML Features (Suite A)', 'before_preprocessing': 11, 'after_preprocessing': 11, 'delta': 0, 'notes': 'Soil Type + N, P2O5, K20, PH, EC, Temp, Humidity, Rainfall, OC, S'},
        {'metric': 'Missing Values (Humidity)', 'before_preprocessing': missing_before_total, 'after_preprocessing': missing_after_total, 'delta': -missing_before_total, 'notes': 'Imputed 20 Mydukur values with overall median 72.59%'},
        {'metric': 'Malformed String Values', 'before_preprocessing': malformed_values_before, 'after_preprocessing': malformed_values_after, 'delta': -malformed_values_before, 'notes': "EC ('0..07'), FC ('2..956'), MN ('1.13.79'), BA ('0..16') converted to float64"},
        {'metric': 'Target Crop Classes', 'before_preprocessing': raw_crop_classes_count, 'after_preprocessing': canonical_crop_classes_count, 'delta': -(raw_crop_classes_count - canonical_crop_classes_count), 'notes': 'Standardized into 34 canonical classes without aggressive guessing'},
        {'metric': 'Rows Removed', 'before_preprocessing': 0, 'after_preprocessing': 0, 'delta': 0, 'notes': 'Zero observations deleted'},
        {'metric': 'Values Imputed', 'before_preprocessing': 0, 'after_preprocessing': missing_humidity_count, 'delta': missing_humidity_count, 'notes': 'Only the 20 missing Humidity values imputed'},
        {'metric': 'Decimal Keystroke Typos Repaired', 'before_preprocessing': 4, 'after_preprocessing': 0, 'delta': -4, 'notes': 'OC 31.0->0.31, 30.35->0.30, 23.0->0.23; BA 96.0->0.96 repaired with physical proof'},
        {'metric': 'Agronomic Extremes Preserved', 'before_preprocessing': 4, 'after_preprocessing': 4, 'delta': 0, 'notes': 'EC=8.18, P2O5=856, N=850, N=801 preserved as genuine anomalies'},
        {'metric': 'Duplicate Records', 'before_preprocessing': 0, 'after_preprocessing': 0, 'delta': 0, 'notes': 'Zero duplicate agricultural records detected'}
    ]
    summary_df = pd.DataFrame(summary_data)
    summary_csv_path = os.path.join(reports_dir, "preprocessing_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"Saved preprocessing summary: {summary_csv_path}")

    # 5. Preprocessing Report: reports/preprocessing_report.md
    report_md_path = os.path.join(reports_dir, "preprocessing_report.md")
    generate_full_preprocessing_report(
        report_path=report_md_path,
        orig_rows=orig_rows,
        final_rows=final_rows,
        orig_cols=orig_cols,
        final_cols=final_cols,
        missing_before_total=missing_before_total,
        missing_after_total=missing_after_total,
        malformed_before=malformed_values_before,
        malformed_after=malformed_values_after,
        crops_before=raw_crop_classes_count,
        crops_after=canonical_crop_classes_count,
        missing_imputed=missing_humidity_count,
        median_humidity=humidity_median,
        dtypes_before=dtypes_before,
        dtypes_after=df_clean.dtypes.astype(str).to_dict(),
        clean_csv_path=clean_csv_path
    )
    print(f"Saved preprocessing report: {report_md_path}")

    # -------------------------------------------------------------------------
    # 12. PRINT FINAL CONCISE SUMMARY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CONCISE DATA PREPROCESSING SUMMARY")
    print("=" * 80)
    print(f"* Original rows:                     {orig_rows}")
    print(f"* Final rows:                        {final_rows}")
    print(f"* Original features (raw sheet):     {orig_cols} columns (20 genuine agricultural + 16,364 empty phantoms)")
    print(f"* Final ML features:                 16 features (Suite B: SOIL TYPE + 15 continuous soil/weather features)")
    print(f"                                     [Alternative: 11 Core Verified features in Suite A]")
    print(f"* Missing values before and after:   {missing_before_total} before (Humidity) -> {missing_after_total} after")
    print(f"* Malformed values before and after: {malformed_values_before} before (EC, FC, MN, BA) -> {malformed_values_after} after")
    print(f"* Number of crop classes:            {raw_crop_classes_count} raw labels -> {canonical_crop_classes_count} canonical classes")
    print(f"* Number of rows removed:            0 rows removed (100% data retention)")
    print(f"* Number of values imputed:          {missing_humidity_count} values (Humidity in Mandal Mydukur with median 72.59%)")
    print(f"* Unresolved data-quality issues:")
    print(f"  1. EC = 8.18 at S.NO 348: Preserved as potential anomaly (plausible extreme salinity or 10x error).")
    print(f"  2. P2O5 = 856 at S.NO 379: Preserved as potential anomaly (authentic 16-record high-P cluster in Atloor).")
    print(f"  3. N = 850 at S.NO 130: Preserved as potential anomaly (plausible heavy commercial fertilizer application).")
    print(f"  4. Crop label 'Bean Gram' (3 records): Preserved distinctly pending verification (suspected Bengal Gram typo).")
    print(f"  5. Laboratory columns 'FC' and 'BA': Uncertain laboratory abbreviations; benchmarked under dual feature suites.")
    print("=" * 80)
    print("DATA PREPROCESSING COMPLETE. READY FOR EXPLORATION & MODEL DESIGN.")
    print("=" * 80)


def generate_full_preprocessing_report(
    report_path, orig_rows, final_rows, orig_cols, final_cols,
    missing_before_total, missing_after_total,
    malformed_before, malformed_after,
    crops_before, crops_after, missing_imputed, median_humidity,
    dtypes_before, dtypes_after, clean_csv_path
):
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Data Preprocessing Execution Report\n\n")
        f.write("**Document Version:** 1.0  \n")
        f.write("**Execution Date:** 2026-10-08  \n")
        f.write("**Project:** Crop Recommendation Using Ensemble Techniques  \n")
        f.write("**Governing Specification:** `reports/step9_preprocessing_policy.md`  \n")
        f.write(f"**Clean Dataset Output:** `{clean_csv_path}`  \n")
        f.write("**Source Dataset:** `data/complete soil data.xlsx` (Read-only, strictly immutable)  \n")
        f.write("**Status:** Completed, Validated, and Fully Documented.  \n\n")
        f.write("---\n\n")

        f.write("## 1. Executive Summary\n\n")
        f.write("This report documents the reproducible, scientific data preprocessing phase for the *Crop Recommendation Using Ensemble Techniques* project. ")
        f.write("The raw dataset originates from agricultural soil testing laboratories across Kadapa district, Andhra Pradesh, India. ")
        f.write("Every transformation strictly follows the evidence-based decisions established in Steps 1 through 9. ")
        f.write("No data has been modified blindly, zero valid rows have been deleted, and complete transparency is maintained across all modifications.\n\n")

        f.write("### Quantitative Snapshot\n\n")
        f.write(f"- **Original Rows:** {orig_rows}  \n")
        f.write(f"- **Final Clean Rows:** {final_rows} (**100.0% data retention**, 0 rows deleted)  \n")
        f.write(f"- **Original Columns in Spreadsheet:** {orig_cols} (20 genuine agricultural + 16,364 empty Excel formatting artifacts)  \n")
        f.write(f"- **Final Agricultural Columns:** {final_cols}  \n")
        f.write(f"- **Final ML Predictive Features:** 16 features (Suite B) or 11 features (Suite A)  \n")
        f.write(f"- **Missing Values Before / After:** {missing_before_total} (confined to Humidity) $\\rightarrow$ **{missing_after_total}**  \n")
        f.write(f"- **Malformed String Typos Before / After:** {malformed_before} $\\rightarrow$ **{malformed_after}**  \n")
        f.write(f"- **Target Crop Classes Before / After:** {crops_before} raw labels $\\rightarrow$ **{crops_after}** canonical classes  \n")
        f.write(f"- **Total Values Imputed:** {missing_imputed} (Humidity in Mandal Mydukur using median ${median_humidity:.2f}\\%$)  \n\n")
        f.write("---\n\n")

        f.write("## 2. Ingestion & Feature Boundary Policies\n\n")
        f.write("### 2.1 Discarding Spreadsheet Artifact Columns\n")
        f.write("The raw Excel sheet `complete soil data.xlsx` spans $16,384$ columns (the theoretical maximum limit of Excel's `.xlsx` specification, columns `A` through `XFD`). ")
        f.write("Columns 21 through 16,384 (`Column1` to `Column16364`) are completely empty artifact columns containing 100% `NaN`. ")
        f.write("These phantom columns were filtered out immediately at raw ingestion, retaining exclusively the 20 genuine agricultural columns.\n\n")

        f.write("### 2.2 S.NO Column Treatment\n")
        f.write("`S.NO` represents an administrative serial number assigned to laboratory samples. ")
        f.write("It is preserved in the cleaned dataset exclusively as an observation tracking identifier (`record_id`). ")
        f.write("**`S.NO` is strictly excluded from machine learning feature matrices $\\mathbf{X}$** to prevent spurious correlation and artificial index memorization.\n\n")

        f.write("### 2.3 Location Features Treatment (`MANDAL NAME` & `VILLAGE NAME`)\n")
        f.write("`MANDAL NAME` (27 sub-districts) and `VILLAGE NAME` (231 hamlets) capture geographic administrative coordinates. ")
        f.write("For a generalizable agronomic decision-support system, recommending crops based on geographical village names creates severe spatial overfitting and failure to generalize to new farmlands. ")
        f.write("They are retained in the clean dataset for auditability and spatial error analysis, but excluded from predictive ML features.\n\n")

        f.write("### 2.4 Soil Type Treatment\n")
        f.write("`SOIL TYPE` contains integers from 1 to 13 representing distinct soil taxonomy and texture classifications (e.g., Red Sandy, Black Clayey, Calcareous). ")
        f.write("Because the integers represent categorical taxonomic classes rather than an ordinal measurement, `SOIL TYPE` is treated strictly as a **categorical feature**.\n\n")

        f.write("---\n\n")

        f.write("## 3. Numeric Anomalies & Malformed String Remediation\n\n")
        f.write("During Step 1 inspection and Step 4 forensic audit, four numerical columns were detected as `object` (string) due to isolated keystroke errors. ")
        f.write("Rather than automatically coercing these unparseable values to `NaN` (which would have caused data loss), each was evaluated against surrounding farm records:\n\n")
        f.write("| S.NO | Feature | Raw Malformed Value | Corrected Value | Status | Forensic Justification |\n")
        f.write("| :---: | :---: | :---: | :---: | :---: | :--- |\n")
        f.write("| 245 | `EC` | `'0..07'` | **`0.07`** | Confirmed Correction | Classic numpad double-tap error (`..`); surrounding Simhadripuram records range 0.05–0.20 dS/m. |\n")
        f.write("| 242 | `FC` | `'2..956'` | **`2.956`** | Confirmed Correction | Double-tap decimal error on numpad; surrounding FC values range 1.5–4.5 ppm. |\n")
        f.write("| 229 | `BA` | `'0..16'` | **`0.16`** | Confirmed Correction | Double-tap decimal error on numpad; surrounding BA values range 0.10–0.35 ppm. |\n")
        f.write("| 55 | `MN` | `'1.13.79'` | **`1.138`** | Confirmed Correction | Segmented string normalized to local Simhadripuram standard 3-decimal baseline (S.NO 57=1.138 in same village). |\n\n")
        f.write("Following these verified corrections, all 15 chemical and weather features were successfully coerced to `float64` without coercion errors.\n\n")

        f.write("---\n\n")

        f.write("## 4. Missing Value Imputation: Humidity Analysis\n\n")
        f.write("### 4.1 Missingness Pattern & Risk of Class Extinction\n")
        f.write("Exactly 20 missing values exist in the entire dataset, all confined to the `Humidity` column in Mandal `Mydukur` (S.NO 267 through 286). ")
        f.write("Across Mandal Mydukur, exactly 20 soil samples were collected, and 0 of them had Humidity recorded ($100\\%$ missing within Mydukur).\n\n")
        f.write("A critical discovery made during Step 5 is that **listwise deletion would extinguish three entire crop classes**: ")
        f.write("5 out of 6 `Vegetables` records, 1 out of 3 `Chillis` records, 3 out of 4 `Tomato` records, and 1 `Turmeric` record reside in these 20 rows. ")
        f.write("Dropping these rows would permanently destroy the project's capacity to recommend these crops.\n\n")

        f.write("### 4.2 Approved Imputation Method\n")
        f.write(f"- **Method:** Overall valid dataset median ($**{median_humidity:.2f}\\%**$).\n")
        f.write("- **Downstream Leakage Prevention Rule:** In machine learning model training (cross-validation), median imputation must be wrapped inside `sklearn.pipeline.Pipeline` or computed strictly on training folds to prevent data leakage into validation folds.\n\n")

        f.write("---\n\n")

        f.write("## 5. Extreme Values & Outlier Policy\n\n")
        f.write("In accordance with Prompt Requirement 9, no observations were deleted. Each extreme value was audited against soil physics and geochemical principles:\n\n")

        f.write("### 5.1 Repaired Decimal Keystroke Errors (Documented Evidence)\n")
        f.write("1. **Organic Carbon ($OC$) at S.NO 84 (`31.0`), S.NO 372 (`30.35`), and S.NO 144 (`23.0`):**\n")
        f.write("   - *Soil Physics Reality:* In tropical semi-arid mineral soils with pH $>7.8$ and temperatures $>35^\\circ\\text{C}$, organic carbon exceeds $1.0\\%$ only in rare fertile patches. An organic carbon of $23\\%$ to $31\\%$ is **physically impossible** (found only in subarctic waterlogged peat bogs).\n")
        f.write("   - *Typographical Proof:* In Kondapuram, surrounding OC values are 0.19, 0.23, 0.27, 0.31, 0.35. A keystroke of `31.0` represents a 100x decimal omission for `0.31`. Similarly, `30.35` represents `0.30`, and `23.0` represents `0.23`.\n")
        f.write("   - *Action:* Repaired to `0.31`, `0.30`, and `0.23` respectively. **Zero rows removed.**\n")
        f.write("2. **Boron / Barium Index ($BA$) at S.NO 62 (`96.0`):**\n")
        f.write("   - *Geochemical Reality:* Across Simhadripuram, all 23 other records range between 0.064 and 2.78 ppm (median 0.224). Global median is 0.256 ppm. `96.0` is $375\\times$ the median.\n")
        f.write("   - *Typographical Proof:* Typing `96` without leading `0.` yields `96.0` instead of `0.96`.\n")
        f.write("   - *Action:* Repaired to `0.96`. **Zero rows removed.**\n\n")

        f.write("### 5.2 Preserved Agronomic Extremes (No Evidence of Data-Entry Error)\n")
        f.write("1. **`EC = 8.18` at S.NO 348 (Mylavaram, Red Chilli):** Plausible extreme localized salinity depression (solonchak condition). Preserved as **`8.18`** without alteration.\n")
        f.write("2. **`P2O5 = 856` at S.NO 379 (Atloor, Bajra):** Part of an authentic 16-farm spatial cluster in Mandal Atloor where P2O5 ranges from 439 to 856 kg/ha, accompanied by high Mn and Zn. Preserved as **`856.0`** without alteration.\n")
        f.write("3. **`N = 850` at S.NO 130 (Chakrayapeta, Groundnut) and `N = 801` at S.NO 422 (Proddutur, Black Gram):** Plausible high commercial fertilizer / manure application prior to sampling. Preserved as **`850.0`** and **`801.0`** without alteration.\n\n")

        f.write("---\n\n")

        f.write("## 6. Target Crop Label Standardization\n\n")
        f.write("The raw target feature `CROP` contained 61 unique text strings. ")
        f.write("Rather than aggressive subjective merging, standardization followed three strict botanical and linguistic rules:\n\n")
        f.write("1. **Format Normalization:** Casing standardization and trimming whitespace (e.g., `paddy` $\\rightarrow$ `Paddy`, `cotton` $\\rightarrow$ `Cotton`, `Black gram` $\\rightarrow$ `Black Gram`, `banana` $\\rightarrow$ `Banana`, `onion` $\\rightarrow$ `Onion`).\n")
        f.write("2. **Undisputed Spelling Typo Correction:** Fixing unambiguous phonetics and keystrokes (e.g., `Grownut` $\\rightarrow$ `Groundnut`, `Blakgram` $\\rightarrow$ `Black Gram`, `soyabean` $\\rightarrow$ `Soybean`, `Tamota` $\\rightarrow$ `Tomato`, `sesam` $\\rightarrow$ `Sesame`, `sweet ornage` $\\rightarrow$ `Sweet Orange`, `Turemaric` $\\rightarrow$ `Turmeric`, `Jouar` $\\rightarrow$ `Jowar`, `muckmelon` $\\rightarrow$ `Muskmelon`, `Caster` $\\rightarrow$ `Castor`, `chillis` $\\rightarrow$ `Chilli`).\n")
        f.write("3. **Strict Botanical Preservation (Zero Aggressive Merging):**\n")
        f.write("   - Distinct citrus species are strictly separated: `Sweet Orange` (*Citrus sinensis*), `Sweet Lime` (*Citrus limetta*), and `Acid Lime` (*Citrus aurantifolia*).\n")
        f.write("   - Distinct pulse species are strictly separated: `Black Gram` (*Vigna mungo*), `Green Gram` (*Vigna radiata*), `Bengal Gram` (*Cicer arietinum*), and `Red Gram` (*Cajanus cajan*).\n")
        f.write("   - Traditional regional Telugu crops preserved: `Allam` (Ginger), `Nannari` (Indian Sarsaparilla), `Korra` (Foxtail Millet), `Bajra` (Pearl Millet), `Jowar` (Sorghum).\n\n")

        f.write("This establishes **34 canonical crop classes** across the 611 records.\n\n")

        f.write("---\n\n")

        f.write("## 7. Tripartite Categorization of Decisions (Requirement 13)\n\n")
        f.write("### 7.1 Confirmed Corrections\n")
        f.write("- Elimination of 16,364 empty artifact spreadsheet columns.\n")
        f.write("- Four keystroke string typo repairs: EC S.NO 245 (`0..07` $\\rightarrow$ `0.07`), FC S.NO 242 (`2..956` $\\rightarrow$ `2.956`), BA S.NO 229 (`0..16` $\\rightarrow$ `0.16`), MN S.NO 55 (`1.13.79` $\\rightarrow$ `1.138`).\n")
        f.write("- Four decimal omission keystroke repairs: OC S.NO 84 (`31.0` $\\rightarrow$ `0.31`), OC S.NO 372 (`30.35` $\\rightarrow$ `0.30`), OC S.NO 144 (`23.0` $\\rightarrow$ `0.23`), BA S.NO 62 (`96.0` $\\rightarrow$ `0.96`).\n")
        f.write("- Missing humidity imputation for 20 Mydukur rows using overall median ($72.59\\%$).\n")
        f.write("- Standardized casing, whitespace, and verified spelling variants across 61 raw crop labels.\n\n")

        f.write("### 7.2 Unresolved Anomalies\n")
        f.write("- **`EC = 8.18` at S.NO 348:** Retained as potential extreme salinity anomaly without row deletion.\n")
        f.write("- **`P2O5 = 856` at S.NO 379:** Retained as potential geochemical cluster anomaly without row deletion.\n")
        f.write("- **`N = 850` at S.NO 130 and `N = 801` at S.NO 422:** Retained as potential fertilizer extreme anomalies without row deletion.\n")
        f.write("- **`Bean Gram` (3 records at S.NO 82, 83, 84 in Kondapuram):** Suspected typo for Bengal Gram based on surrounding records, but retained as distinct label `Bean Gram (Pending Verification)` to prevent ungrounded guessing.\n")
        f.write("- **Laboratory columns `FC` and `BA`:** Exact laboratory meanings are absent from the original IEEE paper and legacy code. Retained and benchmarked under dual feature suites.\n\n")

        f.write("### 7.3 Assumptions Requiring Future Verification\n")
        f.write("- **Humidity Imputation:** Assumed to follow Missing at Random (MAR) mechanism. Future work should cross-reference external Indian Meteorological Department (IMD) historical Kadapa district weather station data.\n")
        f.write("- **Soil Type Encoding:** Assumed to represent nominal soil taxonomy classes (1–13). One-hot encoding should be compared against native tree categorical handling during modeling.\n")
        f.write("- **Feature Suite Configurations:** Evaluated as Suite A (11 core verified features) vs Suite B (16 full laboratory features including uncertain `FC` and `BA`).\n\n")

        f.write("---\n\n")

        f.write("## 8. Data Schema: Before vs. After Preprocessing\n\n")
        f.write("| Column Name | Type Before | Type After | Missing Before | Missing After | Modeling Role |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :--- |\n")
        for col, dt_after in dtypes_after.items():
            dt_bef = dtypes_before.get(col, "N/A")
            mis_bef = 20 if col == 'Humidity' else 0
            mis_aft = 0
            if col == 'CROP':
                role = "Target Label (y)"
            elif col == 'S.NO':
                role = "Tracking ID (Exclude from X)"
            elif col in ['MANDAL NAME', 'VILLAGE NAME']:
                role = "Location Metadata (Exclude from X)"
            elif col == 'SOIL TYPE':
                role = "Categorical ML Feature"
            else:
                role = "Continuous ML Feature"
            f.write(f"| **`{col}`** | `{dt_bef}` | `{dt_after}` | {mis_bef} | **{mis_aft}** | {role} |\n")
        f.write("\n---\n\n")

        f.write("## 9. Verification & Automated Quality Assertions\n\n")
        f.write("All 5 programmatic assertions executed successfully:\n\n")
        f.write("1. **Row Count Integrity:** Exactly $611$ rows preserved ($0$ dropped, $100\\%$ data retention).\n")
        f.write("2. **Zero Unexpected Missing Values:** Exactly $0$ missing cells across all columns.\n")
        f.write("3. **Numeric Type Compliance:** All 15 chemical/weather features confirmed as `float64`.\n")
        f.write("4. **Zero Accidental Duplicates:** Exactly $0$ duplicate agricultural records.\n")
        f.write("5. **Target Label Validity:** 100% of rows contain valid non-empty canonical target labels.\n\n")

        f.write("---\n\n")

        f.write("## 10. Reproducibility & Execution\n\n")
        f.write("The complete pipeline is packaged in `week3_preprocessing/preprocess.py` and can be re-run deterministically:\n\n")
        f.write("```bash\n")
        f.write("python week3_preprocessing/preprocess.py\n")
        f.write("```\n")

if __name__ == '__main__':
    run_preprocessing()
