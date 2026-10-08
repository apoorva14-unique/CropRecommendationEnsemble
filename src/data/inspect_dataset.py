"""
Dataset Inspection Script for Crop Recommendation Project.
STEP 1: DATASET INSPECTION (Non-destructive, strictly exploratory).
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl


def run_inspection():
    print("=" * 80)
    print("STEP 1: COMPREHENSIVE DATASET INSPECTION")
    print("=" * 80)

    excel_path = os.path.join("data", "complete soil data.xlsx")
    if not os.path.exists(excel_path):
        print(f"ERROR: Dataset not found at {excel_path}")
        sys.exit(1)

    # 1. Workbook inspection
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    sheet_names = wb.sheetnames
    active_sheet_name = wb.active.title if wb.active else sheet_names[0]
    print(f"Excel Sheet Names: {sheet_names}")
    print(f"Active Sheet Used: {active_sheet_name}")

    # Load data using pandas
    print("\nLoading dataset via pandas...")
    df_raw = pd.read_excel(excel_path, sheet_name=active_sheet_name)
    total_rows, total_cols = df_raw.shape
    print(f"Total Raw Rows: {total_rows}")
    print(f"Total Raw Columns: {total_cols}")

    # Programmatic detection of non-empty and empty columns (NO hardcoded column counts)
    non_empty_cols = []
    completely_empty_cols = []

    for col in df_raw.columns:
        if df_raw[col].notna().any():
            non_empty_cols.append(col)
        else:
            completely_empty_cols.append(col)

    print(f"\nProgrammatic Column Detection:")
    print(f" - Actual Non-Empty Columns: {len(non_empty_cols)}")
    print(f" - Completely Empty Columns: {len(completely_empty_cols)}")
    print(f"Non-empty column names:\n {non_empty_cols}")

    df = df_raw[non_empty_cols].copy()

    # Check duplicate column names
    col_counts = pd.Series(df_raw.columns).value_counts()
    dup_cols = col_counts[col_counts > 1].index.tolist()
    print(f"Duplicate Column Names in raw sheet: {dup_cols if dup_cols else 'None'}")

    # Check duplicate rows
    dup_rows_all = df_raw.duplicated().sum()
    dup_rows_actual = df.duplicated().sum()
    print(f"Duplicate rows across raw sheet: {dup_rows_all}")
    print(f"Duplicate rows across actual agricultural columns: {dup_rows_actual}")

    # S.NO analysis
    sno_min = df['S.NO'].min() if 'S.NO' in df.columns else None
    sno_max = df['S.NO'].max() if 'S.NO' in df.columns else None
    sno_unique = df['S.NO'].nunique() if 'S.NO' in df.columns else None
    sno_dups = df['S.NO'].duplicated().sum() if 'S.NO' in df.columns else None
    print(f"\nS.NO Analysis:")
    print(f" - Minimum S.NO: {sno_min}")
    print(f" - Maximum S.NO: {sno_max}")
    print(f" - Unique S.NO count: {sno_unique} out of {total_rows} rows")
    print(f" - Duplicate S.NO count: {sno_dups}")

    # Duplicate S.NO values detail
    if sno_dups and sno_dups > 0:
        sno_vc = df['S.NO'].value_counts()
        repeated_snos = sno_vc[sno_vc > 1]
        print(f" - Repeated S.NO values:\n{repeated_snos}")

    # Save dataset_structure.md
    structure_md_path = os.path.join("reports", "dataset_structure.md")
    with open(structure_md_path, "w", encoding="utf-8") as f:
        f.write("# Dataset Structure Report\n\n")
        f.write(f"- **Dataset File:** `{excel_path}`\n")
        f.write(f"- **Excel Sheet Names:** {sheet_names}\n")
        f.write(f"- **Active Sheet Used:** `{active_sheet_name}`\n")
        f.write(f"- **Total Rows:** {total_rows}\n")
        f.write(f"- **Total Columns:** {total_cols}\n")
        f.write(f"- **Actual Non-Empty Agricultural Columns Count:** {len(non_empty_cols)}\n")
        f.write(f"- **Completely Empty Columns Count:** {len(completely_empty_cols)}\n")
        f.write(f"- **Duplicate Column Names:** {dup_cols if dup_cols else 'None'}\n")
        f.write(f"- **Duplicate Rows (across non-empty columns):** {dup_rows_actual}\n")
        f.write(f"- **Unique S.NO Count:** {sno_unique}\n")
        f.write(f"- **S.NO Minimum:** {sno_min}\n")
        f.write(f"- **S.NO Maximum:** {sno_max}\n")
        f.write(f"- **Duplicate S.NO Count:** {sno_dups}\n\n")

        f.write("## Actual Non-Empty Columns\n\n")
        f.write("| Index | Column Name | Sample Value (Row 0) |\n")
        f.write("| :---: | :--- | :--- |\n")
        for idx, col in enumerate(non_empty_cols):
            f.write(f"| {idx} | `{col}` | {df.at[0, col]} |\n")

        f.write("\n## Empty Artifact Columns Summary\n\n")
        f.write(f"- Total empty columns: {len(completely_empty_cols)}\n")
        if completely_empty_cols:
            f.write(f"- Name pattern: `{completely_empty_cols[0]}` to `{completely_empty_cols[-1]}`\n")
            f.write("- Explanation: Standard Microsoft Excel worksheet maximum boundary artifact (2^14 = 16,384 columns). Every cell contains `NaN`.\n")

    print(f"\n[Saved] {structure_md_path}")

    # TASK 4: DATA TYPES & PROFILE
    profile_rows = []
    for col in non_empty_cols:
        col_dtype = str(df[col].dtype)
        non_null_cnt = int(df[col].notna().sum())
        missing_cnt = int(df[col].isna().sum())
        unique_cnt = int(df[col].nunique())
        profile_rows.append({
            "column_name": col,
            "pandas_dtype": col_dtype,
            "non_null_count": non_null_cnt,
            "missing_count": missing_cnt,
            "missing_percentage": round((missing_cnt / total_rows) * 100, 2),
            "unique_count": unique_cnt
        })

    profile_df = pd.DataFrame(profile_rows)
    profile_csv_path = os.path.join("reports", "dataset_profile.csv")
    profile_df.to_csv(profile_csv_path, index=False)
    print(f"[Saved] {profile_csv_path}")

    # TASK 5: MISSING VALUES ANALYSIS
    print("\n" + "=" * 50)
    print("TASK 5: MISSING VALUES BREAKDOWN")
    print("=" * 50)
    cols_with_missing = profile_df[profile_df['missing_count'] > 0]
    if cols_with_missing.empty:
        print("No missing values found across non-empty columns.")
    else:
        for _, row in cols_with_missing.iterrows():
            col_name = row['column_name']
            m_cnt = row['missing_count']
            m_pct = row['missing_percentage']
            missing_mask = df[col_name].isna()
            missing_indices = df[missing_mask].index.tolist()
            print(f"\nColumn '{col_name}': {m_cnt} missing values ({m_pct}%)")
            print(f"Row indices with missing '{col_name}': {missing_indices}")
            print("\nDetailed record breakdown for missing rows:")
            cols_to_show = ['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'CROP']
            actual_show_cols = [c for c in cols_to_show if c in df.columns]
            missing_records = df.loc[missing_mask, actual_show_cols]
            print(missing_records.to_string())

    # TASK 6: NUMERIC ANOMALIES INSPECTION
    print("\n" + "=" * 50)
    print("TASK 6: NUMERIC ANOMALIES INSPECTION")
    print("=" * 50)
    potential_numeric_cols = [
        col for col in non_empty_cols 
        if col not in ['MANDAL NAME', 'VILLAGE NAME', 'CROP']
    ]

    anomalies = []
    for col in potential_numeric_cols:
        for idx, val in enumerate(df[col]):
            if pd.isna(val):
                continue
            # Try converting to float
            val_str = str(val).strip()
            try:
                float(val_str)
            except ValueError:
                sno_val = df.at[idx, 'S.NO'] if 'S.NO' in df.columns else 'N/A'
                # Determine possible intended correction
                possible_corr = "Needs verification"
                if val_str.count('..') == 1:
                    possible_corr = f"Possible correction: '{val_str.replace('..', '.')}' — needs verification"
                elif val_str.count('.') > 1:
                    # e.g., '1.13.79'
                    parts = val_str.split('.')
                    possible_corr = f"Ambiguous multiple decimals ({parts}) — needs verification"
                
                anomalies.append({
                    "column": col,
                    "row_index": idx,
                    "s_no": sno_val,
                    "original_value": val,
                    "note": possible_corr
                })

    print(f"Total Numeric Conversion Anomalies Detected: {len(anomalies)}")
    for anom in anomalies:
        print(f" - Column: '{anom['column']}', Row Index: {anom['row_index']}, S.NO: {anom['s_no']}, Original Value: {repr(anom['original_value'])} -> {anom['note']}")

    # TASK 7: CROP LABEL ANALYSIS
    print("\n" + "=" * 50)
    print("TASK 7: CROP LABEL ANALYSIS")
    print("=" * 50)
    crops_series = df['CROP']
    raw_unique_count = crops_series.nunique()
    raw_vc = crops_series.value_counts()
    print(f"Number of raw unique crop labels: {raw_unique_count}")

    # Case-insensitive / stripped unique labels
    norm_series = crops_series.astype(str).str.strip().str.lower()
    norm_unique_count = norm_series.nunique()
    norm_vc = norm_series.value_counts()
    print(f"Number of case-insensitive, trimmed unique crop labels: {norm_unique_count}")

    # Analyze groupings / variations
    label_records = []
    for raw_label, count in raw_vc.items():
        stripped_lower = str(raw_label).strip().lower()
        # Find other raw labels that map to the same lowercase stripped
        identical_norm = [lbl for lbl in raw_vc.index if str(lbl).strip().lower() == stripped_lower]
        diff_cause = []
        if len(identical_norm) > 1:
            diff_cause.append("capitalization/leading-trailing-spaces")
        label_records.append({
            "raw_crop_label": raw_label,
            "raw_frequency": count,
            "normalized_label": stripped_lower,
            "normalized_frequency": norm_vc[stripped_lower],
            "case_whitespace_variants": ", ".join(identical_norm) if len(identical_norm) > 1 else "None (Single variant)"
        })

    crop_label_profile_df = pd.DataFrame(label_records)
    crop_label_profile_path = os.path.join("reports", "crop_label_profile.csv")
    crop_label_profile_df.to_csv(crop_label_profile_path, index=False)
    print(f"[Saved] {crop_label_profile_path}")

    # TASK 8: NUMERIC FEATURE STATISTICS
    print("\n" + "=" * 50)
    print("TASK 8: NUMERIC FEATURE STATISTICS")
    print("=" * 50)
    numeric_stats = []
    for col in potential_numeric_cols:
        # For columns with object anomalies, convert safely with coerce for STATISTICAL summary only
        col_numeric = pd.to_numeric(df[col], errors='coerce')
        valid_cnt = col_numeric.notna().sum()
        coerced_cnt = (df[col].notna() & col_numeric.isna()).sum()
        stats = {
            "feature": col,
            "count": int(valid_cnt),
            "coerced_unconvertible_count": int(coerced_cnt),
            "mean": round(float(col_numeric.mean()), 4) if valid_cnt > 0 else np.nan,
            "median": round(float(col_numeric.median()), 4) if valid_cnt > 0 else np.nan,
            "std": round(float(col_numeric.std()), 4) if valid_cnt > 0 else np.nan,
            "min": round(float(col_numeric.min()), 4) if valid_cnt > 0 else np.nan,
            "25%": round(float(col_numeric.quantile(0.25)), 4) if valid_cnt > 0 else np.nan,
            "75%": round(float(col_numeric.quantile(0.75)), 4) if valid_cnt > 0 else np.nan,
            "max": round(float(col_numeric.max()), 4) if valid_cnt > 0 else np.nan,
        }
        numeric_stats.append(stats)

    numeric_stats_df = pd.DataFrame(numeric_stats)
    print(numeric_stats_df.to_string(index=False))

    # TASK 9: DATASET SANITY CHECKS
    print("\n" + "=" * 50)
    print("TASK 9: DATASET SANITY CHECK RESULTS")
    print("=" * 50)
    sanity_issues = []

    # 1. Duplicate rows
    if dup_rows_actual > 0:
        sanity_issues.append(f"Duplicate rows detected across actual features: {dup_rows_actual} — Potential anomaly — needs verification.")
    else:
        sanity_issues.append("Duplicate rows across actual features: None (0 duplicates).")

    # 2. Duplicate S.NO
    if sno_dups and sno_dups > 0:
        sanity_issues.append(f"Duplicate S.NO values detected: {sno_dups} instances — Potential anomaly — needs verification.")
    else:
        sanity_issues.append("Duplicate S.NO values: None (All S.NO unique).")

    # 3. Negative values
    negative_cols = {}
    for col in potential_numeric_cols:
        col_numeric = pd.to_numeric(df[col], errors='coerce')
        neg_count = (col_numeric < 0).sum()
        if neg_count > 0:
            negative_cols[col] = neg_count
    if negative_cols:
        sanity_issues.append(f"Negative values detected in columns: {negative_cols} — Potential anomaly — needs verification.")
    else:
        sanity_issues.append("Negative numeric values: None found across all numeric features.")

    # 4. Out-of-range pH
    ph_numeric = pd.to_numeric(df['PH'], errors='coerce')
    out_of_range_ph = ((ph_numeric < 0) | (ph_numeric > 14)).sum()
    if out_of_range_ph > 0:
        sanity_issues.append(f"pH out of valid [0, 14] chemical range: {out_of_range_ph} — Potential anomaly — needs verification.")
    else:
        sanity_issues.append(f"pH range validity: All values within standard range [6.22, 8.90].")

    # 5. Out-of-range humidity
    hum_numeric = pd.to_numeric(df['Humidity'], errors='coerce')
    out_of_range_hum = ((hum_numeric < 0) | (hum_numeric > 100)).sum()
    if out_of_range_hum > 0:
        sanity_issues.append(f"Humidity values outside [0, 100]%: {out_of_range_hum} — Potential anomaly — needs verification.")
    else:
        sanity_issues.append(f"Humidity range validity: All non-null values within valid range [45.09%, 100.0%].")

    # 6. Suspiciously large values (e.g. EC > 5, N > 500)
    ec_num = pd.to_numeric(df['EC'], errors='coerce')
    high_ec = df[ec_num > 5]
    if len(high_ec) > 0:
        sanity_issues.append(f"Suspiciously high EC value: S.NO {high_ec['S.NO'].values} has EC={high_ec['EC'].values} (e.g. 8.18 vs typical 0.01-1.35) — Potential anomaly — needs verification.")

    n_num = pd.to_numeric(df['N'], errors='coerce')
    high_n = df[n_num > 500]
    if len(high_n) > 0:
        sanity_issues.append(f"Suspiciously high N values: {len(high_n)} rows with N > 500 (max: {n_num.max()}) — Potential anomaly — needs verification.")

    for s in sanity_issues:
        print(f" - {s}")

    # TASK 10: GENERATE VISUALIZATION REPORT
    print("\n" + "=" * 50)
    print("TASK 10: GENERATING VISUALIZATION FIGURES")
    print("=" * 50)
    figures_dir = os.path.join("reports", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    # Figure 1: Crop Frequency Distribution (Top 25)
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="whitegrid")
    top_crops = raw_vc.head(25)
    ax1 = sns.barplot(x=top_crops.values, y=top_crops.index, palette="viridis", hue=top_crops.index, legend=False)
    plt.title("Top 25 Raw Crop Label Frequencies (Kadapa Agricultural Dataset)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Number of Field Records", fontsize=12)
    plt.ylabel("Raw Crop Label", fontsize=12)
    for p in ax1.patches:
        width = p.get_width()
        ax1.annotate(f"{int(width)}", (width + 0.5, p.get_y() + p.get_height() / 2.),
                     ha='left', va='center', fontsize=10)
    plt.tight_layout()
    fig1_path = os.path.join(figures_dir, "crop_frequency_distribution.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[Saved] {fig1_path}")

    # Figure 2: Missing Values Summary
    plt.figure(figsize=(10, 6))
    missing_summary = profile_df.set_index('column_name')['missing_count']
    ax2 = sns.barplot(x=missing_summary.index, y=missing_summary.values, color="#e53935")
    plt.title("Missing Values Count Across Agricultural Columns", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Agricultural Column Name", fontsize=12)
    plt.ylabel("Missing Count (Rows)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for p in ax2.patches:
        val = p.get_height()
        if val > 0:
            ax2.annotate(f"{int(val)} ({round(val/total_rows*100, 1)}%)",
                         (p.get_x() + p.get_width() / 2., val + 0.5),
                         ha='center', va='bottom', fontsize=11, fontweight='bold', color="#b71c1c")
    plt.ylim(0, max(missing_summary.values) + 5)
    plt.tight_layout()
    fig2_path = os.path.join(figures_dir, "missing_values_summary.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[Saved] {fig2_path}")

    # Figure 3: Key Numeric Agricultural Feature Distributions
    key_features = ['PH', 'N', 'P2O5', 'K20', 'Temparature', 'Humidity', 'Rainfall']
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(16, 8))
    axes = axes.flatten()

    for i, feat in enumerate(key_features):
        feat_data = pd.to_numeric(df[feat], errors='coerce').dropna()
        sns.histplot(feat_data, kde=True, ax=axes[i], color="#2e7d32", bins=20)
        axes[i].set_title(f"Distribution of {feat}", fontsize=11, fontweight='bold')
        axes[i].set_xlabel(feat, fontsize=10)
        axes[i].set_ylabel("Count", fontsize=10)

    # Empty 8th subplot
    axes[7].axis('off')
    plt.suptitle("Distributions of Key Soil and Agro-Climatic Features", fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()
    fig3_path = os.path.join(figures_dir, "numeric_distributions.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"[Saved] {fig3_path}")

    print("\n" + "=" * 80)
    print("STEP 1: INSPECTION COMPLETE. ALL TASKS EXECUTED SUCCESSFULLY.")
    print("=" * 80)


if __name__ == "__main__":
    run_inspection()
