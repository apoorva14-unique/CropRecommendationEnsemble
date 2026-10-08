"""
Script for Step 5: Missing Humidity Analysis & Decision
Conducts a comprehensive statistical, meteorological, and machine learning audit
of the 20 missing humidity rows in 'data/complete soil data.xlsx'
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer

def run_analysis():
    excel_path = os.path.join("data", "complete soil data.xlsx")
    df_raw = pd.read_excel(excel_path)
    
    # Non-empty columns
    cols = [c for c in df_raw.columns if not c.startswith('Unnamed:') and not c.startswith('Column') and df_raw[c].notna().any()]
    df = df_raw[cols].copy()
    
    print(f"Total dataset shape: {df.shape}")
    
    # 1. Identify rows with missing Humidity
    missing_mask = df['Humidity'].isna()
    df_missing = df[missing_mask]
    df_valid = df[~missing_mask]
    
    print(f"\nMissing Humidity Count: {len(df_missing)}")
    print(f"Valid Humidity Count:   {len(df_valid)}")
    print(f"Missing row indices:    {list(df_missing.index)}")
    print(f"Missing S.NO values:    {list(df_missing['S.NO'])}")
    print(f"Mandals in missing:     {df_missing['MANDAL NAME'].value_counts().to_dict()}")
    
    # 2. Check weather constancy within Mandals
    weather_cols = ['Temparature', 'Humidity', 'Rainfall']
    print("\nWeather Variance within Mandals (Standard Deviations):")
    mandal_weather = df.groupby('MANDAL NAME')[weather_cols].agg(['count', 'std', 'min', 'max'])
    print(mandal_weather.to_string())
    
    # 3. Overall Humidity Distribution (Valid samples)
    h_valid = pd.to_numeric(df_valid['Humidity'])
    print("\n--- Overall Dataset Humidity Distribution (N=591) ---")
    print(f"Min:      {h_valid.min():.4f}")
    print(f"Q1 (25%): {h_valid.quantile(0.25):.4f}")
    print(f"Median:   {h_valid.median():.4f}")
    print(f"Mean:     {h_valid.mean():.4f}")
    print(f"Q3 (75%): {h_valid.quantile(0.75):.4f}")
    print(f"Max:      {h_valid.max():.4f}")
    print(f"Std:      {h_valid.std():.4f}")
    print(f"IQR:      {h_valid.quantile(0.75) - h_valid.quantile(0.25):.4f}")
    print(f"Skew:     {h_valid.skew():.4f}")
    print(f"Kurtosis: {h_valid.kurt():.4f}")
    
    # 4. Mandal-level weather profiles (Mandal Level Table)
    print("\n--- Unique Weather Profile per Mandal ---")
    mandal_profiles = df.groupby('MANDAL NAME')[['Temparature', 'Rainfall', 'Humidity']].agg(
        Temp=('Temparature', 'first'),
        Rain=('Rainfall', 'first'),
        Humidity=('Humidity', 'first'),
        Count=('Temparature', 'count')
    ).sort_values('Temp')
    print(mandal_profiles.to_string())
    
    # 5. Geographically & Meteorologically Related Mandals to Mydukur
    # Mydukur coordinates / neighbors in Kadapa: Chapadu, Duvvuru, Khajipeta, Proddutur, Badvel
    neighbors = ['Chapadu', 'Duvvuru', 'Khajipeta', 'Proddutur', 'Badvel', 'Chennur', 'Siddavatam']
    print("\n--- Neighboring/Climatically Close Mandals to Mydukur (Temp=31.0, Rain=658.5) ---")
    neigh_df = mandal_profiles.loc[mandal_profiles.index.intersection(neighbors)]
    print(neigh_df.to_string())
    
    # 6. Comparison of environmental & soil variables: Mydukur vs. District
    num_features = ['PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S', 'CU', 'FC', 'MN', 'ZN', 'BA', 'Temparature', 'Rainfall']
    # Coerce numeric
    df_num = df.copy()
    for col in num_features:
        df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
        
    print("\n--- Feature Mean Comparison: Mydukur (N=20) vs Rest of Dataset (N=591) ---")
    comp_rows = []
    for f in num_features:
        m_mean = df_num[df_num['MANDAL NAME'] == 'Mydukur'][f].mean()
        m_median = df_num[df_num['MANDAL NAME'] == 'Mydukur'][f].median()
        r_mean = df_num[df_num['MANDAL NAME'] != 'Mydukur'][f].mean()
        r_median = df_num[df_num['MANDAL NAME'] != 'Mydukur'][f].median()
        comp_rows.append({
            'Feature': f,
            'Mydukur Mean': m_mean,
            'Mydukur Median': m_median,
            'Rest Mean': r_mean,
            'Rest Median': r_median
        })
    print(pd.DataFrame(comp_rows).to_string(index=False))
    
    # 7. Crop breakdown in Mydukur and across dataset
    print("\n--- Crops in Mydukur and Extinction Risk ---")
    crop_comp = []
    for c, cnt in df_missing['CROP'].value_counts().items():
        tot = (df['CROP'] == c).sum()
        other = tot - cnt
        pct_lost = (cnt / tot) * 100
        crop_comp.append({
            'Crop': c,
            'Mydukur Count': cnt,
            'Other Count': other,
            'Total Count': tot,
            'Pct Lost if Dropped': f"{pct_lost:.1f}%"
        })
    print(pd.DataFrame(crop_comp).to_string(index=False))
    
    # 8. Candidate Imputation Strategies Calculation
    print("\n" + "="*80)
    print("CALCULATION OF CANDIDATE IMPUTATION VALUES")
    print("="*80)
    
    # Strategy 1: Overall Median
    overall_median = h_valid.median()
    overall_mean = h_valid.mean()
    print(f"1. Overall Median Imputation Value: {overall_median:.4f} % (Mean: {overall_mean:.4f} %)")
    
    # Strategy 2: Mydukur Median
    mydukur_valid_count = df[df['MANDAL NAME'] == 'Mydukur']['Humidity'].dropna().count()
    print(f"2. Mydukur Median Imputation: UNDEFINED (Valid Mydukur records = {mydukur_valid_count})")
    
    # Strategy 3: Crop-Group Median
    print("\n3. Crop-Group Median Analysis:")
    for item in crop_comp:
        c = item['Crop']
        c_h = pd.to_numeric(df[(df['CROP'] == c) & (df['Humidity'].notna())]['Humidity'])
        if len(c_h) > 0:
            print(f"  Crop '{c}': N={len(c_h)}, Median={c_h.median():.2f}%, Mean={c_h.mean():.2f}%, Min={c_h.min():.2f}%, Max={c_h.max():.2f}%")
        else:
            print(f"  Crop '{c}': N=0 valid observations elsewhere! (CANNOT IMPUTE VIA CROP MEDIAN)")

    # Strategy 4: Climate / Weather Neighbors Median
    # Mandals with similar Temp (30 - 32 C) and similar Rain (600 - 850 mm)
    sim_mandals = mandal_profiles[(mandal_profiles['Temp'].between(30.0, 32.0)) & (mandal_profiles['Humidity'].notna())]
    print("\n4. Similar Climate Mandals (Temp between 30-32 C):")
    print(sim_mandals[['Temp', 'Rain', 'Humidity']])
    climate_median = sim_mandals['Humidity'].median()
    climate_mean = sim_mandals['Humidity'].mean()
    print(f"  Climate-matched Median: {climate_median:.2f}% | Mean: {climate_mean:.2f}%")
    
    # Strategy 5: Model-Based Imputation (Weather Regressor)
    # Train on distinct mandals (or all valid rows) predicting Humidity from Temp & Rain
    # Since weather is constant per mandal, mandal-level regression:
    valid_mandal_weather = mandal_profiles[mandal_profiles['Humidity'].notna()].copy()
    X_mandal = valid_mandal_weather[['Temp', 'Rain']].values
    y_mandal = valid_mandal_weather['Humidity'].values
    
    # Linear Regression on Temp & Rain
    lr = LinearRegression().fit(X_mandal, y_mandal)
    mydukur_weather = np.array([[31.0, 658.5]])
    lr_pred = lr.predict(mydukur_weather)[0]
    
    # Ridge Regression
    ridge = Ridge(alpha=1.0).fit(X_mandal, y_mandal)
    ridge_pred = ridge.predict(mydukur_weather)[0]
    
    # KNN Regressor (k=3)
    knn3 = KNeighborsRegressor(n_neighbors=3, weights='distance').fit(X_mandal, y_mandal)
    knn3_pred = knn3.predict(mydukur_weather)[0]
    
    # KNN Regressor (k=5)
    knn5 = KNeighborsRegressor(n_neighbors=5, weights='distance').fit(X_mandal, y_mandal)
    knn5_pred = knn5.predict(mydukur_weather)[0]

    # IterativeImputer / MICE on weather features across all valid rows
    X_rows = df_num[['Temparature', 'Rainfall', 'Humidity']].copy()
    it_imp = IterativeImputer(random_state=42)
    X_rows_imp = it_imp.fit_transform(X_rows)
    mice_pred = X_rows_imp[df_missing.index, 2].mean()
    
    print("\n5. Model-Based Estimations for Mydukur (Temp=31.0, Rain=658.5):")
    print(f"  Linear Regression (Temp + Rain):  {lr_pred:.2f} % (R2={lr.score(X_mandal, y_mandal):.4f})")
    print(f"  Ridge Regression (Temp + Rain):   {ridge_pred:.2f} %")
    print(f"  KNN Regressor (k=3, distance):    {knn3_pred:.2f} %")
    print(f"  KNN Regressor (k=5, distance):    {knn5_pred:.2f} %")
    print(f"  IterativeImputer / MICE:          {mice_pred:.2f} %")

    # Generate diagnostic visualizations
    print("\nGenerating diagnostic figure for Step 5...")
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    
    # Plot 1: Humidity distribution across Mandals (sorted)
    ax1 = axes[0, 0]
    mandal_h_sorted = valid_mandal_weather.sort_values('Humidity')
    sns.barplot(x=mandal_h_sorted['Humidity'], y=mandal_h_sorted.index, ax=ax1, palette='Blues_r')
    ax1.axvline(overall_median, color='red', linestyle='--', label=f'Overall Median ({overall_median:.1f}%)')
    ax1.axvline(climate_median, color='green', linestyle=':', label=f'Climate-matched Median ({climate_median:.1f}%)')
    ax1.set_title('Recorded Humidity across 26 Complete Mandals', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Humidity (%)')
    ax1.legend(loc='lower right')
    
    # Plot 2: Scatter plot of Temp vs Humidity with Mydukur Temp indicated
    ax2 = axes[0, 1]
    sns.scatterplot(data=valid_mandal_weather, x='Temp', y='Humidity', size='Rain', sizes=(40, 200), ax=ax2, color='#2b83ba', alpha=0.8)
    ax2.axvline(31.0, color='orange', linestyle='--', linewidth=2, label='Mydukur Temp (31.0°C)')
    ax2.scatter([31.0], [overall_median], color='red', s=120, zorder=5, marker='X', label=f'Overall Median ({overall_median:.1f}%)')
    ax2.scatter([31.0], [climate_median], color='green', s=120, zorder=5, marker='^', label=f'Climate-matched ({climate_median:.1f}%)')
    ax2.scatter([31.0], [knn3_pred], color='purple', s=120, zorder=5, marker='s', label=f'KNN-3 Model ({knn3_pred:.1f}%)')
    ax2.set_title('Mandal Weather Space: Temperature vs. Humidity', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Temperature (°C)')
    ax2.set_ylabel('Humidity (%)')
    ax2.legend(loc='upper right', fontsize=8)
    
    # Plot 3: Crop Distribution in Mydukur (showing extinction risk)
    ax3 = axes[1, 0]
    crop_counts = df_missing['CROP'].value_counts()
    colors = ['#d7191c' if c in ['Vegetables', 'Turemeric', 'Chillis'] else '#fdae61' if c in ['Tamota', 'Jowar'] else '#abd9e9' for c in crop_counts.index]
    sns.barplot(x=crop_counts.values, y=crop_counts.index, ax=ax3, palette=colors)
    ax3.set_title('Crops in Mandal Mydukur (Red=100% Extinction, Orange=75% Lost if Dropped)', fontsize=10, fontweight='bold')
    ax3.set_xlabel('Number of Farms')
    
    # Plot 4: Imputation Candidates Comparison Bar Plot
    ax4 = axes[1, 1]
    cand_names = [
        'Overall Median',
        'Overall Mean',
        'Climate-Matched Median',
        'KNN-3 Weather Model',
        'Linear Regression',
        'IterativeImputer (MICE)'
    ]
    cand_vals = [
        overall_median,
        overall_mean,
        climate_median,
        knn3_pred,
        lr_pred,
        mice_pred
    ]
    sns.barplot(x=cand_vals, y=cand_names, ax=ax4, palette='viridis')
    for i, v in enumerate(cand_vals):
        ax4.text(v + 0.5, i, f"{v:.2f}%", va='center', fontsize=9, fontweight='bold')
    ax4.set_xlim(0, 85)
    ax4.set_title('Candidate Imputation Values for Mydukur Humidity', fontsize=11, fontweight='bold')
    ax4.set_xlabel('Estimated Humidity (%)')
    
    plt.tight_layout()
    os.makedirs('reports/figures', exist_ok=True)
    fig_path = os.path.join('reports', 'figures', 'missing_humidity_decision_analysis.png')
    plt.savefig(fig_path, dpi=300)
    print(f"Diagnostic plot saved to: {fig_path}")

if __name__ == '__main__':
    run_analysis()
