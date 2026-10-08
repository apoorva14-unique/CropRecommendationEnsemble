"""
Verification Script for Step 4: Numeric Anomalies Verification
Reproducible, non-destructive data science analysis on 'data/complete soil data.xlsx'
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def run_verification():
    excel_path = os.path.join("data", "complete soil data.xlsx")
    df_raw = pd.read_excel(excel_path)
    
    # Filter genuine non-empty columns (exclude phantom Excel columns)
    cols = [c for c in df_raw.columns if not c.startswith('Unnamed:') and not c.startswith('Column') and df_raw[c].notna().any()]
    df = df_raw[cols].copy()
    
    print(f"Total rows: {len(df)}")
    print(f"Genuine Columns ({len(cols)}): {cols}")
    
    # Coerce numeric columns to float for statistical evaluation (purely in-memory)
    num_cols = ['PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S', 'CU', 'FC', 'MN', 'ZN', 'BA', 'Temparature', 'Humidity', 'Rainfall']
    df_num = df.copy()
    for col in num_cols:
        df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
        
    print("\n" + "="*80)
    print("STEP 4: VERIFICATION OF THE FOUR NUMERIC STRING ANOMALIES")
    print("="*80)
    
    anomalies = [
        {'sno': 245, 'col': 'EC', 'raw': '0..07', 'feature_name': 'Electrical Conductivity (EC)'},
        {'sno': 242, 'col': 'FC', 'raw': '2..956', 'feature_name': 'Field Capacity / Iron Index (FC)'},
        {'sno': 55,  'col': 'MN', 'raw': '1.13.79', 'feature_name': 'Manganese (MN)'},
        {'sno': 229, 'col': 'BA', 'raw': '0..16', 'feature_name': 'Boron / Barium Index (BA)'}
    ]
    
    for item in anomalies:
        sno = item['sno']
        col = item['col']
        raw_val = item['raw']
        feat = item['feature_name']
        
        idx = df[df['S.NO'] == sno].index[0]
        row = df.loc[idx]
        mandal = row['MANDAL NAME']
        village = row['VILLAGE NAME']
        crop = row['CROP']
        soil_type = row['SOIL TYPE']
        
        print("\n" + "#"*80)
        print(f"ANOMALY: {feat} at S.NO {sno} (Row index {idx})")
        print(f"Raw Value: '{raw_val}' | Mandal: {mandal} | Village: {village} | Crop: {crop} | Soil Type: {soil_type}")
        print("#"*80)
        
        # 1. Exact Row Display (all 20 attributes)
        print("\n--- EXACT ROW ATTRIBUTES ---")
        for c in df.columns:
            print(f"  {c}: {row[c]}")
            
        # 2. Surrounding rows (5 before and 5 after)
        start_idx = max(0, idx - 5)
        end_idx = min(len(df), idx + 6)
        print(f"\n--- SURROUNDING ROWS (indices {start_idx} to {end_idx - 1}) ---")
        surround_cols = ['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', col, 'PH', 'CROP']
        surround_df = df.loc[start_idx:end_idx - 1, surround_cols]
        print(surround_df.to_string())
        
        # 3. Global feature statistics (coerced numeric)
        s_glob = df_num[col].dropna()
        q1_g = s_glob.quantile(0.25)
        q3_g = s_glob.quantile(0.75)
        iqr_g = q3_g - q1_g
        print(f"\n--- GLOBAL FEATURE STATISTICS for {col} (N={len(s_glob)}) ---")
        print(f"  Min:    {s_glob.min():.4f}")
        print(f"  Q1:     {q1_g:.4f}")
        print(f"  Median: {s_glob.median():.4f}")
        print(f"  Mean:   {s_glob.mean():.4f}")
        print(f"  Q3:     {q3_g:.4f}")
        print(f"  Max:    {s_glob.max():.4f}")
        print(f"  Std:    {s_glob.std():.4f}")
        print(f"  IQR:    {iqr_g:.4f}")
        
        # 4. Mandal-level statistics
        df_mandal = df_num[df_num['MANDAL NAME'] == mandal]
        s_mandal = df_mandal[col].dropna()
        q1_m = s_mandal.quantile(0.25)
        q3_m = s_mandal.quantile(0.75)
        iqr_m = q3_m - q1_m
        print(f"\n--- MANDAL LEVEL STATISTICS ({mandal}, N={len(s_mandal)}) ---")
        print(f"  Min:    {s_mandal.min():.4f}")
        print(f"  Q1:     {q1_m:.4f}")
        print(f"  Median: {s_mandal.median():.4f}")
        print(f"  Mean:   {s_mandal.mean():.4f}")
        print(f"  Q3:     {q3_m:.4f}")
        print(f"  Max:    {s_mandal.max():.4f}")
        print(f"  Std:    {s_mandal.std():.4f}")
        print(f"  IQR:    {iqr_m:.4f}")
        print(f"  All values in {mandal}:")
        print(f"  {sorted(s_mandal.tolist())}")
        
        # 5. Village-level values if any
        df_village = df_num[(df_num['MANDAL NAME'] == mandal) & (df_num['VILLAGE NAME'] == village)]
        s_village = df_village[col].dropna()
        print(f"\n--- VILLAGE LEVEL VALUES ({village}, N={len(s_village)}) ---")
        print(f"  Values: {sorted(s_village.tolist())}")

    # Special in-depth investigation for MN = '1.13.79'
    print("\n" + "="*80)
    print("SPECIAL IN-DEPTH INVESTIGATION: MN = '1.13.79' (S.NO 55)")
    print("="*80)
    
    sim_mn = df_num[df_num['MANDAL NAME'] == 'Simhadripuram']['MN'].dropna()
    glob_mn = df_num['MN'].dropna()
    sun_sim_mn = df_num[(df_num['MANDAL NAME'] == 'Simhadripuram') & (df_num['CROP'] == 'sunflower')]['MN'].dropna()
    sun_glob_mn = df_num[df_num['CROP'].str.strip().str.lower() == 'sunflower']['MN'].dropna()
    soil3_sim_mn = df_num[(df_num['MANDAL NAME'] == 'Simhadripuram') & (df_num['SOIL TYPE'] == 3)]['MN'].dropna()

    candidates = [
        ('1.1379 / 1.138', 1.1379),
        ('11.379', 11.379),
        ('1.13', 1.13),
        ('13.79', 13.79),
        ('Simhadripuram Median (2.014)', 2.014)
    ]
    
    print("\nZ-Score and Outlier Assessment across Candidate Interpretations:")
    for name, val in candidates:
        z_sim = (val - sim_mn.mean()) / sim_mn.std()
        z_glob = (val - glob_mn.mean()) / glob_mn.std()
        z_sun_sim = (val - sun_sim_mn.mean()) / sun_sim_mn.std()
        z_sun_glob = (val - sun_glob_mn.mean()) / sun_glob_mn.std()
        print(f"\nCandidate: {name} (val = {val})")
        print(f"  Simhadripuram Mandal (Mean={sim_mn.mean():.4f}, Std={sim_mn.std():.4f}, Range=[{sim_mn.min()}, {sim_mn.max()}]):")
        print(f"    z-score: {z_sim:+.2f} | Within local range? {'YES' if sim_mn.min() <= val <= sim_mn.max() else 'NO (OUTLIER)'}")
        print(f"  Global Dataset (Mean={glob_mn.mean():.4f}, Std={glob_mn.std():.4f}, Range=[{glob_mn.min()}, {glob_mn.max()}]):")
        print(f"    z-score: {z_glob:+.2f} | Within global range? {'YES' if glob_mn.min() <= val <= glob_mn.max() else 'NO'}")
        print(f"  Sunflower Crop in Simhadripuram (Mean={sun_sim_mn.mean():.4f}, Std={sun_sim_mn.std():.4f}):")
        print(f"    z-score: {z_sun_sim:+.2f}")
        print(f"  Sunflower Crop Globally (Mean={sun_glob_mn.mean():.4f}, Std={sun_glob_mn.std():.4f}):")
        print(f"    z-score: {z_sun_glob:+.2f}")

    # Generate diagnostic plot
    print("\nGenerating diagnostic figure...")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. EC in Vempalli
    ax1 = axes[0, 0]
    vemp_ec = df_num[df_num['MANDAL NAME'] == 'Vempalli']['EC'].dropna()
    sns.boxplot(y=vemp_ec, ax=ax1, color='#6baed6', width=0.4)
    sns.stripplot(y=vemp_ec, ax=ax1, color='#08519c', size=6, jitter=0.2, alpha=0.7)
    ax1.axhline(0.07, color='red', linestyle='--', linewidth=2, label='Candidate: 0.07')
    ax1.set_title('EC in Mandal Vempalli (S.NO 245 raw: 0..07)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Electrical Conductivity (EC, dS/m)')
    ax1.legend()

    # 2. FC in Vempalli
    ax2 = axes[0, 1]
    vemp_fc = df_num[df_num['MANDAL NAME'] == 'Vempalli']['FC'].dropna()
    sns.boxplot(y=vemp_fc, ax=ax2, color='#74c476', width=0.4)
    sns.stripplot(y=vemp_fc, ax=ax2, color='#006d2c', size=6, jitter=0.2, alpha=0.7)
    ax2.axhline(2.956, color='red', linestyle='--', linewidth=2, label='Candidate: 2.956')
    ax2.set_title('FC in Mandal Vempalli (S.NO 242 raw: 2..956)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Field Capacity (FC)')
    ax2.legend()

    # 3. BA in Lingala
    ax3 = axes[1, 0]
    ling_ba = df_num[df_num['MANDAL NAME'] == 'Lingala']['BA'].dropna()
    sns.boxplot(y=ling_ba, ax=ax3, color='#fd8d3c', width=0.4)
    sns.stripplot(y=ling_ba, ax=ax3, color='#a63603', size=6, jitter=0.2, alpha=0.7)
    ax3.axhline(0.16, color='red', linestyle='--', linewidth=2, label='Candidate: 0.16')
    ax3.set_title('BA in Mandal Lingala (S.NO 229 raw: 0..16)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Boron / Barium Index (BA, ppm)')
    ax3.legend()

    # 4. MN in Simhadripuram & Candidate Interpretations
    ax4 = axes[1, 1]
    sns.boxplot(y=sim_mn, ax=ax4, color='#bcbddc', width=0.4)
    sns.stripplot(y=sim_mn, ax=ax4, color='#54278f', size=6, jitter=0.2, alpha=0.7)
    ax4.axhline(1.1379, color='green', linestyle='-', linewidth=2, label='Cand A: 1.1379 / 1.138 (z = -0.80)')
    ax4.axhline(2.014, color='blue', linestyle=':', linewidth=2, label='Cand D: Mandal Median 2.014')
    ax4.axhline(11.379, color='red', linestyle='--', linewidth=2, label='Cand B: 11.379 (z = +5.27, extreme outlier)')
    ax4.set_ylim(-1, 14)
    ax4.set_title('MN in Mandal Simhadripuram (S.NO 55 raw: 1.13.79)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Manganese (MN, ppm)')
    ax4.legend(loc='upper right')

    plt.tight_layout()
    os.makedirs('reports/figures', exist_ok=True)
    fig_path = os.path.join('reports', 'figures', 'numeric_anomalies_verification.png')
    plt.savefig(fig_path, dpi=300)
    print(f"Figure successfully saved to: {fig_path}")
    print("\nVerification complete!")

if __name__ == '__main__':
    run_verification()
