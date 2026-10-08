"""
Script to build and verify crop label consolidation mapping for Step 6.
Generates 'data/processed/crop_label_mapping.csv'
"""

import os
import pandas as pd

def build_mapping():
    excel_path = os.path.join("data", "complete soil data.xlsx")
    df = pd.read_excel(excel_path)
    cols = [c for c in df.columns if not c.startswith('Unnamed:') and not c.startswith('Column') and df[c].notna().any()]
    df = df[cols].copy()
    
    raw_vc = df['CROP'].value_counts()
    print(f"Total rows in dataset: {len(df)}")
    print(f"Total raw distinct labels: {len(raw_vc)}")
    
    # Detailed mapping dictionary:
    # raw_label: (canonical_label, reason, confidence, action)
    mapping_rules = {
        # Paddy
        'paddy': ('Paddy', 'Title-case capitalization', 'High', 'format_normalization'),
        
        # Cotton
        'cotton': ('Cotton', 'Title-case capitalization', 'High', 'format_normalization'),
        'Cotton': ('Cotton', 'Preserve valid title-case', 'High', 'keep_as_is'),
        
        # Groundnut (Grownut is common Indian transcription for Groundnut)
        'Grownut': ('Groundnut', 'Standardize colloquial spelling Grownut to Groundnut', 'High', 'spelling_correction'),
        'grownut': ('Groundnut', 'Standardize colloquial spelling Grownut to Groundnut and capitalize', 'High', 'spelling_correction'),
        
        # Black Gram
        'Black Gram': ('Black Gram', 'Standard canonical title-case', 'High', 'keep_as_is'),
        'Black gram': ('Black Gram', 'Standardize casing to Title Case', 'High', 'format_normalization'),
        'black gram': ('Black Gram', 'Standardize lowercase to Title Case', 'High', 'format_normalization'),
        'Blakgram': ('Black Gram', 'Correct spelling typo missing c and space', 'High', 'spelling_correction'),
        'Blak Gram': ('Black Gram', 'Correct spelling typo missing c', 'High', 'spelling_correction'),
        'Blak gram': ('Black Gram', 'Correct spelling typo missing c and casing', 'High', 'spelling_correction'),
        'Blackgram': ('Black Gram', 'Insert missing space between words', 'High', 'spelling_correction'),
        
        # Bajra
        'Bajra': ('Bajra', 'Preserve valid canonical name (Pearl Millet)', 'High', 'keep_as_is'),
        
        # Bengal Gram
        'Bengal gram': ('Bengal Gram', 'Standardize casing to Title Case', 'High', 'format_normalization'),
        'Bengal Gram': ('Bengal Gram', 'Standard canonical title-case', 'High', 'keep_as_is'),
        'Bean Gram': ('Bean Gram (Pending Verification)', 'Investigate potential typo for Bengal Gram vs distinct legume', 'Moderate', 'source_verification_required'),
        
        # Turmeric
        'Turmeric': ('Turmeric', 'Standard canonical title-case', 'High', 'keep_as_is'),
        'turmeric': ('Turmeric', 'Capitalize standard name', 'High', 'format_normalization'),
        'Turemaric': ('Turmeric', 'Correct phonetic spelling typo', 'High', 'spelling_correction'),
        'termeric': ('Turmeric', 'Correct phonetic spelling typo', 'High', 'spelling_correction'),
        'Turemeric': ('Turmeric', 'Correct phonetic spelling typo', 'High', 'spelling_correction'),
        'Turmaric': ('Turmeric', 'Correct phonetic spelling typo', 'High', 'spelling_correction'),
        
        # Banana
        'banana': ('Banana', 'Capitalize standard name', 'High', 'format_normalization'),
        'Banana': ('Banana', 'Preserve valid title-case', 'High', 'keep_as_is'),
        
        # Sweet Orange & Citrus
        'sweet orange': ('Sweet Orange', 'Standardize lowercase to Title Case', 'High', 'format_normalization'),
        'Sweet orange': ('Sweet Orange', 'Standardize casing to Title Case', 'High', 'format_normalization'),
        'sweet ornage': ('Sweet Orange', 'Correct spelling typo ornage to orange', 'High', 'spelling_correction'),
        'swwet orange': ('Sweet Orange', 'Correct spelling typo swwet to sweet', 'High', 'spelling_correction'),
        'sweet lime': ('Sweet Lime', 'Preserve botanically distinct species Citrus limetta', 'High', 'keep_separate_species'),
        'Acidlime': ('Acid Lime', 'Standardize to Title Case space-separated Citrus aurantifolia', 'High', 'format_normalization'),
        
        # Sunflower
        'sunflower': ('Sunflower', 'Capitalize standard name', 'High', 'format_normalization'),
        'Sunflower': ('Sunflower', 'Preserve valid title-case', 'High', 'keep_as_is'),
        
        # Soybean
        'soyabean': ('Soybean', 'Standardize Indian English soyabean to Soybean', 'High', 'spelling_correction'),
        'Soyabean': ('Soybean', 'Standardize Indian English Soyabean to Soybean', 'High', 'spelling_correction'),
        
        # Onion
        'onion': ('Onion', 'Capitalize standard name', 'High', 'format_normalization'),
        
        # Chamanthi & Floriculture
        'chamanthi': ('Chamanthi', 'Capitalize regional Telugu name for Chrysanthemum', 'High', 'format_normalization'),
        'Chamanthi': ('Chamanthi', 'Preserve valid title-case Chrysanthemum', 'High', 'keep_as_is'),
        'mums': ('Chamanthi (Mums)', 'Horticultural synonym for Chrysanthemum/Chamanthi', 'Moderate', 'synonym_consolidation'),
        
        # Vegetables
        'Vegetables': ('Vegetables', 'Preserve aggregate horticultural category', 'High', 'keep_as_is'),
        'vegetables': ('Vegetables', 'Capitalize aggregate category', 'High', 'format_normalization'),
        
        # Jowar (Sorghum)
        'Jowar': ('Jowar', 'Preserve valid title-case', 'High', 'keep_as_is'),
        'Jouar': ('Jowar', 'Correct phonetic spelling typo Jouar to Jowar', 'High', 'spelling_correction'),
        'jouar': ('Jowar', 'Correct phonetic spelling typo and casing', 'High', 'spelling_correction'),
        
        # Korra (Foxtail Millet)
        'korra': ('Korra', 'Capitalize regional Telugu name for Foxtail Millet', 'High', 'format_normalization'),
        
        # Tomato
        'Tamota': ('Tomato', 'Standardize colloquial Telugu phonetic Tamota to Tomato', 'High', 'spelling_correction'),
        
        # Sesame
        'sesam': ('Sesame', 'Standardize truncated spelling sesam to Sesame', 'High', 'spelling_correction'),
        'sesasum': ('Sesame', 'Correct spelling typo sesasum to Sesame', 'High', 'spelling_correction'),
        'Sesamum': ('Sesame', 'Standardize Latin genus name to common name Sesame', 'High', 'spelling_correction'),
        
        # Chillies
        'chillis': ('Chilli', 'Standardize spelling and capitalize', 'High', 'format_normalization'),
        'Chillis': ('Chilli', 'Standardize plural spelling to singular canonical Chilli', 'High', 'format_normalization'),
        'Red Chilli': ('Red Chilli', 'Mature harvested chilli (or consolidate under Chilli)', 'Moderate', 'evaluate_subclass'),
        'Greenchilli': ('Green Chilli', 'Immature fresh chilli (or consolidate under Chilli)', 'Moderate', 'evaluate_subclass'),
        
        # Maize
        'maize': ('Maize', 'Capitalize standard name', 'High', 'format_normalization'),
        
        # Pulses / Legumes
        'Green Gram': ('Green Gram', 'Preserve distinct botanical species Vigna radiata (Moong)', 'High', 'keep_separate_species'),
        'Red Gram': ('Red Gram', 'Preserve distinct botanical species Cajanus cajan (Toor)', 'High', 'keep_separate_species'),
        
        # Horticultural Singletons
        'guava': ('Guava', 'Capitalize standard fruit name Psidium guajava', 'High', 'format_normalization'),
        'papaya': ('Papaya', 'Capitalize standard fruit name Carica papaya', 'High', 'format_normalization'),
        'muckmelon': ('Muskmelon', 'Correct typo muckmelon to Muskmelon Cucumis melo', 'High', 'spelling_correction'),
        'Caster': ('Castor', 'Correct typo Caster to Castor Ricinus communis', 'High', 'spelling_correction'),
        'Allam': ('Allam (Ginger)', 'Preserve Telugu regional crop name for Ginger', 'High', 'keep_as_is'),
        'Nannari': ('Nannari', 'Preserve Telugu regional medicinal crop Hemidesmus indicus', 'High', 'keep_as_is'),
    }
    
    # Verify all 61 raw labels are accounted for
    missing_in_mapping = [k for k in raw_vc.index if k not in mapping_rules]
    if missing_in_mapping:
        print(f"ERROR: Missing rules for: {missing_in_mapping}")
    else:
        print("ALL 61 RAW LABELS SUCCESSFULLY MAPPED!")
        
    records = []
    for raw, freq in raw_vc.items():
        canonical, reason, conf, action = mapping_rules[raw]
        records.append({
            'raw_label': raw,
            'frequency': freq,
            'canonical_label': canonical,
            'reason': reason,
            'confidence': conf,
            'action': action
        })
        
    map_df = pd.DataFrame(records)
    
    # Save CSV
    out_dir = os.path.join("data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, "crop_label_mapping.csv")
    map_df.to_csv(out_csv, index=False)
    print(f"\nSaved mapping file to: {out_csv}")
    print(f"Total rows in mapping CSV: {len(map_df)}")
    
    # Summary statistics
    print("\n" + "="*80)
    print("MAPPING SUMMARY STATISTICS")
    print("="*80)
    print(f"Original Raw Labels: {len(raw_vc)}")
    
    # Formatting normalization count
    norm_labels = [clean_str(x) for x in raw_vc.index]
    print(f"Formatting-Normalized Distinct Labels: {len(set(norm_labels))}")
    
    # Consolidated canonical labels count
    canonical_unique = map_df['canonical_label'].nunique()
    print(f"Proposed Canonical Labels Count: {canonical_unique}")
    
    print("\nCanonical Classes and their Aggregate Frequencies:")
    canon_vc = map_df.groupby('canonical_label')['frequency'].sum().sort_values(ascending=False)
    for i, (c, cnt) in enumerate(canon_vc.items(), 1):
        raw_members = map_df[map_df['canonical_label'] == c]['raw_label'].tolist()
        print(f"{i:2d}. {c:<32} : {cnt:3d} rows <- {raw_members}")

def clean_str(s):
    return ' '.join(str(s).strip().split()).lower()

if __name__ == '__main__':
    build_mapping()
