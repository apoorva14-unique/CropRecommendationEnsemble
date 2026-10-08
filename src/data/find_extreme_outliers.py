"""
Locate and analyze the extreme values mentioned in Step 8.
"""

import os
import pandas as pd
import numpy as np

def find_extremes():
    excel_path = os.path.join("data", "complete soil data.xlsx")
    df = pd.read_excel(excel_path)
    cols = [c for c in df.columns if not c.startswith('Unnamed:') and not c.startswith('Column') and df[c].notna().any()]
    df = df[cols].copy()
    
    # Coerce numeric features for checking
    num_cols = ['PH', 'EC', 'OC', 'N', 'P2O5', 'K20', 'S', 'CU', 'FC', 'MN', 'ZN', 'BA', 'Temparature', 'Humidity', 'Rainfall']
    for c in num_cols:
        df[c + '_num'] = pd.to_numeric(df[c], errors='coerce')
        
    print("=== SEARCHING SPECIFIC TARGET EXTREMES ===")
    
    # 1. EC = 8.18
    ec_818 = df[df['EC_num'] >= 8.0]
    print(f"\nEC >= 8.0 (Found {len(ec_818)}):")
    print(ec_818[['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', 'EC', 'PH', 'CROP']].to_string())
    
    # 2. OC extremes
    print(f"\nTop 5 OC values:")
    top_oc = df.sort_values('OC_num', ascending=False).head(5)
    print(top_oc[['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', 'OC', 'N', 'P2O5', 'CROP']].to_string())
    
    # 3. N extremes
    print(f"\nTop 5 N values:")
    top_n = df.sort_values('N_num', ascending=False).head(5)
    print(top_n[['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', 'N', 'OC', 'P2O5', 'K20', 'CROP']].to_string())
    
    # 4. P2O5 extremes
    print(f"\nTop 5 P2O5 values:")
    top_p = df.sort_values('P2O5_num', ascending=False).head(5)
    print(top_p[['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', 'P2O5', 'N', 'K20', 'CROP']].to_string())
    
    # 5. BA extremes
    print(f"\nTop 5 BA values:")
    top_ba = df.sort_values('BA_num', ascending=False).head(5)
    print(top_ba[['S.NO', 'MANDAL NAME', 'VILLAGE NAME', 'SOIL TYPE', 'BA', 'CU', 'MN', 'ZN', 'CROP']].to_string())

    # 6. S.NO 348 full check
    r348 = df[df['S.NO'] == 348]
    print("\nS.NO 348 complete row:")
    print(r348[cols].to_dict(orient='records'))

if __name__ == '__main__':
    find_extremes()
