"""
Script for Step 8: Comprehensive Extreme Outlier Investigation
Calculates IQR, z-scores, percentiles, detects multi-feature outliers,
investigates S.NO 348, OC=31.0, BA=96.0, N=850, P2O5=856, EC=8.18.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def run_outlier_audit():
    excel_path = os.path.join("data", "complete soil data.xlsx")
    df = pd.read_excel(excel_path)
    cols = [c for c in df.columns if not c.startswith('Unnamed:') and not c.startswith('Column') and df[c].notna().any()]
    df = df[cols].copy()
    
    num_features = ['PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S', 'CU', 'FC', 'MN', 'ZN', 'BA', 'Temparature', 'Humidity', 'Rainfall']
    
    # Coerce numeric values (excluding malformed strings gracefully)
    df_num = df.copy()
    for col in num_features:
        df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
        
    print("="*80)
    print("1. STATISTICAL OUTLIER BOUNDS PER FEATURE")
    print("="*80)
    
    stats_table = []
    outlier_masks_mild = {}
    outlier_masks_extreme = {}
    z_masks_3 = {}
    
    for f in num_features:
        s = df_num[f].dropna()
        q1 = s.quantile(0.25)
        med = s.median()
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        mean = s.mean()
        std = s.std()
        
        mild_low = q1 - 1.5 * iqr
        mild_high = q3 + 1.5 * iqr
        ext_low = q1 - 3.0 * iqr
        ext_high = q3 + 3.0 * iqr
        
        z_scores = (df_num[f] - mean) / std
        
        mask_mild = (df_num[f] < mild_low) | (df_num[f] > mild_high)
        mask_ext = (df_num[f] < ext_low) | (df_num[f] > ext_high)
        mask_z3 = z_scores.abs() > 3.0
        
        outlier_masks_mild[f] = mask_mild
        outlier_masks_extreme[f] = mask_ext
        z_masks_3[f] = mask_z3
        
        stats_table.append({
            'Feature': f,
            'Min': s.min(),
            'Q1': q1,
            'Median': med,
            'Q3': q3,
            'Max': s.max(),
            'IQR': iqr,
            'Mild Upper (>Q3+1.5*IQR)': mild_high,
            'Extreme Upper (>Q3+3*IQR)': ext_high,
            'Mild Outlier Count': mask_mild.sum(),
            'Extreme Outlier Count': mask_ext.sum(),
            'Z>3 Count': mask_z3.sum()
        })
        
    stats_df = pd.DataFrame(stats_table)
    print(stats_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("2. DISENTANGLING THE TARGET EXTREME OBSERVATIONS")
    print("="*80)
    
    target_checks = [
        ('EC = 8.18', df_num['EC'] >= 8.0),
        ('OC = 31.0', df_num['OC'] >= 20.0),
        ('N = 850', df_num['N'] >= 800.0),
        ('P2O5 = 856', df_num['P2O5'] >= 800.0),
        ('BA = 96.0', df_num['BA'] >= 50.0),
        ('S.NO 348 record', df_num['S.NO'] == 348)
    ]
    
    for label, mask in target_checks:
        sub = df_num[mask]
        print(f"\n--- {label} (Found {len(sub)} rows) ---")
        for idx, row in sub.iterrows():
            print(f"Row Index: {idx} | S.NO: {row['S.NO']} | Mandal: {row['MANDAL NAME']} | Village: {row['VILLAGE NAME']} | Crop: {row['CROP']}")
            print(f"  PH: {row['PH']}, EC: {row['EC']}, OC: {row['OC']}, N: {row['N']}, P2O5: {row['P2O5']}, K20: {row['K20']}, S: {row['S']}")
            print(f"  CU: {row['CU']}, FC: {row['FC']}, MN: {row['MN']}, ZN: {row['ZN']}, BA: {row['BA']}")
            print(f"  Temp: {row['Temparature']}, Rain: {row['Rainfall']}, Humidity: {row['Humidity']}")

    print("\n" + "="*80)
    print("3. MULTI-FEATURE OUTLIER ASSESSMENT (Simultaneous Extremes)")
    print("="*80)
    
    # Calculate how many features exceed extreme IQR (> Q3 + 3*IQR) per row
    ext_df = pd.DataFrame(outlier_masks_extreme)
    df_num['extreme_feature_count'] = ext_df.sum(axis=1)
    
    z3_df = pd.DataFrame(z_masks_3)
    df_num['z3_feature_count'] = z3_df.sum(axis=1)
    
    multi_ext = df_num[df_num['extreme_feature_count'] >= 2].sort_values('extreme_feature_count', ascending=False)
    print(f"\nRows with 2 or more EXTREME IQR outliers (> Q3 + 3*IQR): {len(multi_ext)}")
    for idx, row in multi_ext.iterrows():
        ext_cols = [c for c in num_features if ext_df.loc[idx, c]]
        print(f"S.NO: {row['S.NO']:3d} | Mandal: {row['MANDAL NAME']:<15} | Village: {row['VILLAGE NAME']:<18} | Crop: {row['CROP']:<12} | Ext Count: {row['extreme_feature_count']} | Features: {ext_cols}")

    # S.NO 348 feature count
    r348_ext = df_num[df_num['S.NO'] == 348]['extreme_feature_count'].iloc[0]
    r348_z3 = df_num[df_num['S.NO'] == 348]['z3_feature_count'].iloc[0]
    print(f"\nS.NO 348 Multi-Feature Outlier Summary:")
    print(f"  Extreme IQR count: {r348_ext}")
    print(f"  Z > 3 count:       {r348_z3}")

    print("\n" + "="*80)
    print("4. DETAILED BREAKDOWN OF THE NOTABLE ANOMALOUS RECORDS")
    print("="*80)
    
    # Detailed check of S.NO 84 (OC = 31.0)
    print("\n--- Deep Dive: S.NO 84 (OC = 31.0) ---")
    s84 = df_num[df_num['S.NO'] == 84].iloc[0]
    konda_oc = df_num[df_num['MANDAL NAME'] == 'Kondapuram']['OC'].dropna()
    print(f"Mandal: {s84['MANDAL NAME']} | Village: {s84['VILLAGE NAME']} | Crop: {s84['CROP']}")
    print(f"Kondapuram OC values: {sorted(konda_oc.tolist())}")
    
    # Detailed check of S.NO 372 (OC = 30.35) and S.NO 144 (OC = 23.0)
    print("\n--- Deep Dive: S.NO 372 (OC = 30.35) and S.NO 144 (OC = 23.0) ---")
    s372 = df_num[df_num['S.NO'] == 372].iloc[0]
    atloor_oc = df_num[df_num['MANDAL NAME'] == 'Atloor']['OC'].dropna()
    print(f"S.NO 372: Mandal {s372['MANDAL NAME']} | Village {s372['VILLAGE NAME']} | Atloor OC values: {sorted(atloor_oc.tolist())}")
    
    s144 = df_num[df_num['S.NO'] == 144].iloc[0]
    thondur_oc = df_num[df_num['MANDAL NAME'] == 'Thondur']['OC'].dropna()
    print(f"S.NO 144: Mandal {s144['MANDAL NAME']} | Village {s144['VILLAGE NAME']} | Thondur OC values: {sorted(thondur_oc.tolist())}")

    # Detailed check of S.NO 62 (BA = 96.0)
    print("\n--- Deep Dive: S.NO 62 (BA = 96.0) ---")
    s62 = df_num[df_num['S.NO'] == 62].iloc[0]
    sim_ba = df_num[df_num['MANDAL NAME'] == 'Simhadripuram']['BA'].dropna()
    print(f"Mandal: {s62['MANDAL NAME']} | Village {s62['VILLAGE NAME']} | Crop: {s62['CROP']}")
    print(f"Simhadripuram BA values: {sorted(sim_ba.tolist())}")

    # Detailed check of S.NO 379 (P2O5 = 856) and Atloor P2O5 cluster
    print("\n--- Deep Dive: S.NO 379 (P2O5 = 856) and Atloor P2O5 Cluster ---")
    atloor_p = df_num[df_num['MANDAL NAME'] == 'Atloor']['P2O5'].dropna()
    print(f"Atloor P2O5 values (N={len(atloor_p)}): {sorted(atloor_p.tolist())}")

    # Generate diagnostic plot
    print("\nGenerating diagnostic figure for Step 8...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # 1. EC Outlier (S.NO 348)
    ax1 = axes[0, 0]
    sns.boxplot(y=df_num['EC'], ax=ax1, color='#6baed6')
    ax1.scatter([0], [8.18], color='red', s=100, zorder=5, label='S.NO 348 (8.18 dS/m)')
    ax1.set_title('EC Distribution & S.NO 348 Spike', fontweight='bold')
    ax1.legend()
    
    # 2. OC Outliers (31.0, 30.35, 23.0)
    ax2 = axes[0, 1]
    sns.boxplot(y=df_num['OC'], ax=ax2, color='#74c476')
    ax2.scatter([0, 0, 0], [31.0, 30.35, 23.0], color='red', s=100, zorder=5, label='OC Decimal Errors (>20%)')
    ax2.set_title('OC Distribution & 100x Decimal Shifting', fontweight='bold')
    ax2.legend()
    
    # 3. BA Outlier (S.NO 62 = 96.0)
    ax3 = axes[0, 2]
    sns.boxplot(y=df_num['BA'], ax=ax3, color='#fd8d3c')
    ax3.scatter([0], [96.0], color='red', s=100, zorder=5, label='S.NO 62 (96.0 ppm)')
    ax3.set_title('BA Distribution & S.NO 62 Missing Dot', fontweight='bold')
    ax3.legend()
    
    # 4. N Outliers (850, 801)
    ax4 = axes[1, 0]
    sns.boxplot(y=df_num['N'], ax=ax4, color='#bcbddc')
    ax4.scatter([0, 0], [850.0, 801.0], color='purple', s=100, zorder=5, label='N Spikes (850, 801 kg/ha)')
    ax4.set_title('Nitrogen (N) Outliers', fontweight='bold')
    ax4.legend()
    
    # 5. P2O5 Outliers (Atloor Cluster)
    ax5 = axes[1, 1]
    sns.boxplot(y=df_num['P2O5'], ax=ax5, color='#fa9fb5')
    ax5.scatter([0], [856], color='darkred', s=100, zorder=5, label='S.NO 379 (856 kg/ha)')
    ax5.set_title('P2O5 Distribution (Atloor Regional Cluster)', fontweight='bold')
    ax5.legend()
    
    # 6. Multi-Feature Outlier Distribution
    ax6 = axes[1, 2]
    counts = df_num['extreme_feature_count'].value_counts().sort_index()
    sns.barplot(x=counts.index, y=counts.values, ax=ax6, palette='viridis')
    for i, v in enumerate(counts.values):
        ax6.text(i, v + 2, str(v), ha='center', fontweight='bold')
    ax6.set_title('Count of Extreme (>Q3+3*IQR) Features per Row', fontweight='bold')
    ax6.set_xlabel('Number of Extreme Features in Record')
    ax6.set_ylabel('Number of Records')
    
    plt.tight_layout()
    os.makedirs('reports/figures', exist_ok=True)
    fig_path = os.path.join('reports', 'figures', 'extreme_outliers_investigation.png')
    plt.savefig(fig_path, dpi=300)
    print(f"Diagnostic plot saved to: {fig_path}")

if __name__ == '__main__':
    run_outlier_audit()
