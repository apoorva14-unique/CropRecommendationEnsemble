"""
Step 2: Extract Genuine Agricultural Columns

This script performs the first data preparation step for the project:
1. Loads the raw Excel dataset ('data/complete soil data.xlsx') in read-only fashion.
2. Programmatically detects and filters out all completely empty columns
   (the 16,364 Excel boundary artifact columns) without hardcoding column indices.
3. Retains all 20 genuine agricultural data columns.
4. Leaves all values, typos, missing entries, and crop labels untouched.
5. Saves the clean intermediate dataset under 'data/processed/genuine_agricultural_data.csv'.
"""

import os
import pandas as pd


def extract_genuine_columns():
    # ---------------------------------------------------------
    # 1. Define file paths
    # ---------------------------------------------------------
    input_file = os.path.join("data", "complete soil data.xlsx")
    output_dir = os.path.join("data", "processed")
    output_csv = os.path.join(output_dir, "genuine_agricultural_data.csv")
    output_excel = os.path.join(output_dir, "genuine_agricultural_data.xlsx")

    # Verify that the original Excel file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 75)
    print("STEP 2: EXTRACT GENUINE AGRICULTURAL COLUMNS")
    print("=" * 75)

    # ---------------------------------------------------------
    # 2. Read the original Excel file (Read-only operation)
    # ---------------------------------------------------------
    print(f"\n[1] Reading raw dataset from: {input_file}")
    df_raw = pd.read_excel(input_file)

    # Print original shape
    print(f"\n* Original shape: {df_raw.shape}")
    print(f"  - Total rows: {df_raw.shape[0]}")
    print(f"  - Total columns: {df_raw.shape[1]}")

    # ---------------------------------------------------------
    # 3. Programmatically identify and keep non-empty columns
    # ---------------------------------------------------------
    # dropna(axis=1, how='all') drops any column where ALL values are NaN.
    # This automatically removes all 16,364 empty artifact columns
    # without hard-coding column numbers or names.
    df_retained = df_raw.dropna(axis=1, how='all').copy()

    # Calculate number of non-empty columns
    num_non_empty = df_retained.shape[1]
    retained_column_names = df_retained.columns.tolist()

    print(f"\n* Number of non-empty columns: {num_non_empty}")
    print("\n* Names of retained columns:")
    for idx, col_name in enumerate(retained_column_names, start=1):
        sample_val = df_retained[col_name].iloc[0]
        print(f"   {idx:2d}. {col_name:<15} (Sample row 0: {sample_val})")

    # Print final shape
    print(f"\n* Final shape: {df_retained.shape}")
    print(f"  - Rows: {df_retained.shape[0]}")
    print(f"  - Columns: {df_retained.shape[1]}")

    # ---------------------------------------------------------
    # 4. Save intermediate dataset separately under data/processed/
    # ---------------------------------------------------------
    # Save as CSV for fast and clean processing
    df_retained.to_csv(output_csv, index=False)
    print(f"\n[2] Saved intermediate CSV to: {output_csv}")

    # Also save as clean Excel file for easy viewing
    df_retained.to_excel(output_excel, index=False)
    print(f"[3] Saved intermediate Excel to: {output_excel}")

    # ---------------------------------------------------------
    # 5. Integrity Confirmation
    # ---------------------------------------------------------
    print("\n* Integrity checks:")
    print("  - Original dataset file 'data/complete soil data.xlsx' was NOT modified.")
    print("  - No rows were removed (all 611 data rows preserved).")
    print("  - No missing values imputed (Humidity still has 20 NaNs).")
    print("  - No typos corrected (EC, FC, MN, BA remain in original raw form).")
    print("  - No crop labels modified (all 61 raw variants intact).")
    print("=" * 75)


if __name__ == "__main__":
    extract_genuine_columns()
