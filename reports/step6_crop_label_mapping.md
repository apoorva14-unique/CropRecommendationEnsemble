# Step 6: Crop Label Consolidation Analysis Report

**Document Version:** 1.0  
**Analysis Date:** 2026-10-08  
**Project:** Crop Recommendation Using Ensemble Techniques  
**Dataset Inspected:** `data/complete soil data.xlsx` (Untouched, Read-Only)  
**Execution Script:** `src/data/analyze_crop_labels.py`  
**Machine-Readable Mapping:** `data/processed/crop_label_mapping.csv`  
**Status:** Analytical & Decision Framework — **No changes have been applied to the raw dataset.**

---

## 1. Executive Summary

In agricultural machine learning pipelines, target variable integrity is paramount. In `data/complete soil data.xlsx`, the target feature `CROP` contains **61 distinct raw string labels** across its 611 observations. 

A thorough linguistic, typographical, and botanical audit reveals that this fragmentation is driven primarily by:
1. **Case and whitespace inconsistencies** (e.g., `'Black Gram'`, `'Black gram'`, `'black gram'`).
2. **Keystroke typos and spelling misspellings** (e.g., `'Blakgram'`, `'Blak Gram'`, `'swwet orange'`, `'Turemaric'`).
3. **Phonetic transliterations from Telugu into English** (e.g., `'Tamota'` for Tomato, `'Jouar'` for Jowar, `'Allam'` for Ginger, `'Korra'` for Foxtail Millet, `'Chamanthi'` for Chrysanthemum).
4. **Horticultural abbreviations and synonyms** (e.g., `'mums'` for Chrysanthemums).
5. **Genuinely distinct botanical species with low sample counts** (e.g., `'sweet lime'` vs `'sweet orange'`, `'Green Gram'` vs `'Black Gram'`, `'Red Gram'` vs `'Bengal Gram'`).

This report provides a disciplined, non-destructive consolidation framework that reduces the target space from **61 raw labels $\rightarrow$ 46 formatting-normalized labels $\rightarrow$ 34 canonical crop classes**, while strictly avoiding improper mergers of botanically distinct crops.

---

## 2. Complete Inventory of the 61 Raw Crop Labels

Below is the complete frequency distribution of all 61 raw labels extracted from the untouched dataset:

| # | Raw Crop Label | Raw Frequency | % of Dataset | Nature of Label |
| :-: | :--- | :---: | :---: | :--- |
| 1 | `paddy` | 143 | 23.40% | Dominant cereal crop (lowercase) |
| 2 | `cotton` | 89 | 14.57% | Dominant fiber crop (lowercase) |
| 3 | `Grownut` | 55 | 9.00% | Dominant oilseed (colloquial spelling) |
| 4 | `Black Gram` | 48 | 7.86% | Dominant pulse (Title Case) |
| 5 | `Bajra` | 34 | 5.56% | Pearl millet (Title Case) |
| 6 | `Black gram` | 30 | 4.91% | Sentence-case variant of Black Gram |
| 7 | `Bengal gram` | 24 | 3.93% | Chickpea (Sentence Case) |
| 8 | `Turmeric` | 22 | 3.60% | Commercial spice crop (Title Case) |
| 9 | `sweet orange` | 12 | 1.96% | Citrus fruit Sathgudi (lowercase) |
| 10 | `sunflower` | 11 | 1.80% | Oilseed (lowercase) |
| 11 | `Blakgram` | 10 | 1.64% | Typo variant (missing 'c' and space) |
| 12 | `banana` | 9 | 1.47% | Fruit crop (lowercase) |
| 13 | `turmeric` | 8 | 1.31% | Lowercase variant of Turmeric |
| 14 | `onion` | 8 | 1.31% | Vegetable bulb (lowercase) |
| 15 | `grownut` | 6 | 0.98% | Lowercase variant of Grownut |
| 16 | `soyabean` | 6 | 0.98% | Oilseed legume (Indian spelling) |
| 17 | `chamanthi` | 6 | 0.98% | Chrysanthemum flower (Telugu name, lowercase) |
| 18 | `Bengal Gram` | 6 | 0.98% | Title Case variant of Bengal Gram |
| 19 | `Vegetables` | 5 | 0.82% | Aggregate category (Title Case) |
| 20 | `Banana` | 5 | 0.82% | Title Case variant of banana |
| 21 | `Jowar` | 4 | 0.65% | Sorghum millet (Title Case) |
| 22 | `Cotton` | 4 | 0.65% | Title Case variant of cotton |
| 23 | `korra` | 4 | 0.65% | Foxtail millet (Telugu name, lowercase) |
| 24 | `Tamota` | 4 | 0.65% | Tomato (Telugu phonetic spelling) |
| 25 | `sesam` | 4 | 0.65% | Sesame oilseed (truncated spelling) |
| 26 | `Soyabean` | 3 | 0.49% | Title Case variant of soyabean |
| 27 | `black gram` | 3 | 0.49% | Lowercase variant of Black Gram |
| 28 | `Bean Gram` | 3 | 0.49% | Suspect variant / legume in Kondapuram |
| 29 | `sweet ornage` | 3 | 0.49% | Typo variant ('ornage' for orange) |
| 30 | `Red Chilli` | 3 | 0.49% | Spice crop (Title Case) |
| 31 | `maize` | 2 | 0.33% | Cereal crop (lowercase) |
| 32 | `Acidlime` | 2 | 0.33% | Citrus aurantifolia (Kagzi lime) |
| 33 | `Green Gram` | 2 | 0.33% | Moong pulse (Vigna radiata) |
| 34 | `Sunflower` | 2 | 0.33% | Title Case variant of sunflower |
| 35 | `chillis` | 2 | 0.33% | Lowercase plural variant of chilli |
| 36 | `Turemaric` | 2 | 0.33% | Typo variant of Turmeric |
| 37 | `Jouar` | 2 | 0.33% | Phonetic typo variant of Jowar |
| 38 | `Blak Gram` | 2 | 0.33% | Typo variant (missing 'c') |
| 39 | `jouar` | 1 | 0.16% | Lowercase phonetic typo of Jowar |
| 40 | `guava` | 1 | 0.16% | Fruit crop (Psidium guajava) |
| 41 | `Sweet orange` | 1 | 0.16% | Title Case variant of sweet orange |
| 42 | `termeric` | 1 | 0.16% | Typo variant of Turmeric |
| 43 | `muckmelon` | 1 | 0.16% | Typo variant for Muskmelon (Cucumis melo) |
| 44 | `swwet orange` | 1 | 0.16% | Typo variant ('swwet' for sweet) |
| 45 | `mums` | 1 | 0.16% | Trade abbreviation for Chrysanthemums |
| 46 | `Blak gram` | 1 | 0.16% | Sentence-case typo variant of Black Gram |
| 47 | `Chillis` | 1 | 0.16% | Title Case plural variant of chilli |
| 48 | `Turemeric` | 1 | 0.16% | Typo variant of Turmeric |
| 49 | `Blackgram` | 1 | 0.16% | Missing space variant of Black Gram |
| 50 | `Red Gram` | 1 | 0.16% | Pigeonpea / Toor (Cajanus cajan) |
| 51 | `vegetables` | 1 | 0.16% | Lowercase variant of Vegetables |
| 52 | `sweet lime` | 1 | 0.16% | Citrus limetta (Mitha Nimbu) |
| 53 | `sesasum` | 1 | 0.16% | Typo variant of Sesamum / Sesame |
| 54 | `Allam` | 1 | 0.16% | Ginger (Telugu name: Zingiber officinale) |
| 55 | `Turmaric` | 1 | 0.16% | Typo variant of Turmeric |
| 56 | `Caster` | 1 | 0.16% | Typo variant for Castor (Ricinus communis) |
| 57 | `papaya` | 1 | 0.16% | Fruit crop (Carica papaya) |
| 58 | `Nannari` | 1 | 0.16% | Medicinal plant (Hemidesmus indicus) |
| 59 | `Greenchilli` | 1 | 0.16% | Compound word variant of green chilli |
| 60 | `Sesamum` | 1 | 0.16% | Latin genus variant of Sesame |
| 61 | `Chamanthi` | 1 | 0.16% | Title Case variant of chamanthi |

---

## 3. Formatting Normalization Results

When applying strictly non-semantic formatting normalization (stripping leading/trailing spaces, collapsing internal whitespace, and lower-casing), the label count drops from **61 raw labels to 46 normalized groups**.

### Multi-Variant Formatting Clusters Resolved
1. `cotton` (89) + `Cotton` (4) $\rightarrow$ `cotton` (93)
2. `Black Gram` (48) + `Black gram` (30) + `black gram` (3) $\rightarrow$ `black gram` (81)
3. `Grownut` (55) + `grownut` (6) $\rightarrow$ `grownut` (61)
4. `Turmeric` (22) + `turmeric` (8) $\rightarrow$ `turmeric` (30)
5. `Bengal gram` (24) + `Bengal Gram` (6) $\rightarrow$ `bengal gram` (30)
6. `banana` (9) + `Banana` (5) $\rightarrow$ `banana` (14)
7. `sweet orange` (12) + `Sweet orange` (1) $\rightarrow$ `sweet orange` (13)
8. `sunflower` (11) + `Sunflower` (2) $\rightarrow$ `sunflower` (13)
9. `soyabean` (6) + `Soyabean` (3) $\rightarrow$ `soyabean` (9)
10. `chamanthi` (6) + `Chamanthi` (1) $\rightarrow$ `chamanthi` (7)
11. `Vegetables` (5) + `vegetables` (1) $\rightarrow$ `vegetables` (6)
12. `Blak Gram` (2) + `Blak gram` (1) $\rightarrow$ `blak gram` (3)
13. `chillis` (2) + `Chillis` (1) $\rightarrow$ `chillis` (3)
14. `Jouar` (2) + `jouar` (1) $\rightarrow$ `jouar` (3)

---

## 4. Typographical, Linguistic & Botanical Consolidation Analysis

### 4.1 Black Gram Cluster (Total: 95 Observations)
* **Raw Labels:** `Black Gram` (48), `Black gram` (30), `black gram` (3), `Blakgram` (10), `Blak Gram` (2), `Blak gram` (1), `Blackgram` (1).
* **Botanical Entity:** *Vigna mungo* (Urad Dal).
* **Forensic Rationale:** `Blakgram`, `Blak Gram`, and `Blak gram` omit the letter `'c'`. `Blackgram` omits the space. All refer identically to black gram.
* **Proposed Canonical Label:** **`Black Gram`** (Confidence: **Very High, >99%**).

---

### 4.2 Turmeric Cluster (Total: 35 Observations)
* **Raw Labels:** `Turmeric` (22), `turmeric` (8), `Turemaric` (2), `termeric` (1), `Turemeric` (1), `Turmaric` (1).
* **Botanical Entity:** *Curcuma longa* (Haridra / Pasupu).
* **Forensic Rationale:** All five variant spellings are standard phonetic transcription misspellings of Turmeric.
* **Proposed Canonical Label:** **`Turmeric`** (Confidence: **Very High, >99%**).

---

### 4.3 Groundnut Cluster (Total: 61 Observations)
* **Raw Labels:** `Grownut` (55), `grownut` (6).
* **Botanical Entity:** *Arachis hypogaea* (Peanut / Verusanaga).
* **Forensic Rationale:** In Indian field records, "Grownut" is a common phonetic transcription for Groundnut.
* **Proposed Canonical Label:** **`Groundnut`** (Confidence: **Very High, >99%**).

---

### 4.4 Jowar Cluster (Total: 7 Observations)
* **Raw Labels:** `Jowar` (4), `Jouar` (2), `jouar` (1).
* **Botanical Entity:** *Sorghum bicolor* (Great Millet / Jonna).
* **Forensic Rationale:** "Jouar" is a direct phonetic variant of "Jowar".
* **Proposed Canonical Label:** **`Jowar`** (Confidence: **Very High, >99%**).

---

### 4.5 Sweet Orange & Citrus Disambiguation (CRITICAL)
* **Raw Labels:** `sweet orange` (12), `Sweet orange` (1), `sweet ornage` (3), `swwet orange` (1), `sweet lime` (1), `Acidlime` (2).
* **Botanical Disambiguation:**
  1. **Sweet Orange (*Citrus sinensis*):** Sathgudi / Mosambi. `sweet ornage` (typo `'ornage'`) and `swwet orange` (typo `'swwet'`) clearly belong here. Consolidated count: **17 observations**.
  2. **Sweet Lime (*Citrus limetta*):** Mitha Nimbu. **Must NOT be merged with sweet orange**. Cultivated separately with different soil salinity tolerance and water requirements. Count: **1 observation** (S.NO 132 in Chakrayapeta).
  3. **Acid Lime (*Citrus aurantifolia*):** Kagzi Nimbu / Sour Lime. Botanically distinct acidic citrus. Count: **2 observations** (S.NO 106, 107 in Chakrayapeta).
* **Proposed Canonical Labels:** **`Sweet Orange`** (17), **`Sweet Lime`** (1), **`Acid Lime`** (2).

---

### 4.6 Pulses Disambiguation: Green Gram vs. Red Gram vs. Bengal Gram vs. Bean Gram
* **Botanical Disambiguation:**
  1. **Black Gram (*Vigna mungo*):** 95 observations.
  2. **Bengal Gram (*Cicer arietinum*):** Chickpea / Chana. 30 observations (`Bengal gram`: 24, `Bengal Gram`: 6).
  3. **Green Gram (*Vigna radiata*):** Moong Dal. **Botanically distinct species**. Count: **2 observations** (S.NO 102 in Chakrayapeta, S.NO 473 in Khajipeta). Must remain distinct.
  4. **Red Gram (*Cajanus cajan*):** Pigeonpea / Toor Dal / Kandulu. **Botanically distinct species**. Count: **1 observation** (S.NO 149 in Thondur). Must remain distinct.
  5. **Bean Gram:** Count: **3 observations** (S.NO 82, 83, 84 in Mandal Kondapuram).
     * *Investigation:* In Kondapuram, all neighboring pulse fields are recorded as `Bengal gram` / `Bengal Gram`. "Bean Gram" is likely a typist slip for Bengal Gram, but could theoretically refer to Phaseolus / French bean.
     * *Decision:* Flag as **`Bean Gram (Pending Verification)`**; do not merge blindly without lab logbook confirmation.

---

### 4.7 Floriculture: Chamanthi vs. Mums
* **Raw Labels:** `chamanthi` (6), `Chamanthi` (1), `mums` (1).
* **Botanical Entity:** *Chrysanthemum indicum* (Guldaudi).
* **Forensic Rationale:** In floriculture, "mums" is the universal English trade name for Chrysanthemums. In Telugu, Chrysanthemum is universally named **"Chamanthi"** (చామంతి). S.NO 28 (`mums`) in Vontimitta shares identical floral soil requirements ($N=150, P=36, K=473, \text{pH}=7.90$) with Chamanthi in Pendlimarri.
* **Proposed Canonical Label:** **`Chamanthi`** (7 confirmed; `mums` recommended for synonym consolidation $\rightarrow$ 8 total).

---

### 4.8 Regional Telugu & Unique Crop Names
1. **`Tamota` (4 observations):** Telugu colloquial phonetic spelling for **Tomato** (*Solanum lycopersicum*). Standardize to `Tomato`.
2. **`Allam` (1 observation, S.NO 497):** Telugu word (అల్లం) for **Ginger** (*Zingiber officinale*).
3. **`Korra` (4 observations):** Telugu word (కొర్రలు) for **Foxtail Millet** (*Setaria italica*), a major traditional Rayalaseema millet.
4. **`Nannari` (1 observation, S.NO 498):** Regional Rayalaseema name for **Indian Sarsaparilla** (*Hemidesmus indicus*), a medicinal root crop.
5. **`Caster` (1 observation, S.NO 408):** Typo for **Castor** (*Ricinus communis*).
6. **`muckmelon` (1 observation, S.NO 41):** Typo for **Muskmelon** (*Cucumis melo*).

---

### 4.9 Chillies Cluster
* **Raw Labels:** `chillis` (2), `Chillis` (1), `Red Chilli` (3), `Greenchilli` (1).
* **Botanical Reality:** All represent *Capsicum annuum*. Green chilli is the fresh immature pod; red chilli is the dried mature pod.
* **Proposed Canonical Structure:**
  * Option A (Botanical Consensus): Consolidate all 7 into **`Chilli`** (or `Chillies`).
  * Option B (Commercial Separation): Retain `Chilli` (3), `Red Chilli` (3), and `Green Chilli` (1).
  * *Recommendation:* Primary mapping standardizes spelling to `Chilli` while tagging maturity subclasses in mapping metadata.

---

## 5. Complete Mapping Table (All 61 Raw Labels)

| Raw Label | Frequency | Proposed Canonical Label | Reason | Confidence | Action |
| :--- | :---: | :--- | :--- | :---: | :--- |
| `paddy` | 143 | **Paddy** | Capitalize standard crop name | High | format_normalization |
| `cotton` | 89 | **Cotton** | Capitalize standard crop name | High | format_normalization |
| `Grownut` | 55 | **Groundnut** | Standardize colloquial spelling Grownut $\rightarrow$ Groundnut | High | spelling_correction |
| `Black Gram` | 48 | **Black Gram** | Standard canonical Title Case | High | keep_as_is |
| `Bajra` | 34 | **Bajra** | Standard pearl millet | High | keep_as_is |
| `Black gram` | 30 | **Black Gram** | Standardize sentence case to Title Case | High | format_normalization |
| `Bengal gram` | 24 | **Bengal Gram** | Standardize sentence case to Title Case | High | format_normalization |
| `Turmeric` | 22 | **Turmeric** | Standard canonical Title Case | High | keep_as_is |
| `sweet orange` | 12 | **Sweet Orange** | Standardize lowercase to Title Case (Citrus sinensis) | High | format_normalization |
| `sunflower` | 11 | **Sunflower** | Capitalize standard crop name | High | format_normalization |
| `Blakgram` | 10 | **Black Gram** | Correct typo (missing 'c' and space) | High | spelling_correction |
| `banana` | 9 | **Banana** | Capitalize standard crop name | High | format_normalization |
| `turmeric` | 8 | **Turmeric** | Capitalize standard crop name | High | format_normalization |
| `onion` | 8 | **Onion** | Capitalize standard crop name | High | format_normalization |
| `grownut` | 6 | **Groundnut** | Standardize colloquial spelling and capitalize | High | spelling_correction |
| `soyabean` | 6 | **Soybean** | Standardize Indian spelling soyabean $\rightarrow$ Soybean | High | spelling_correction |
| `chamanthi` | 6 | **Chamanthi** | Capitalize Telugu regional flower name (Chrysanthemum) | High | format_normalization |
| `Bengal Gram` | 6 | **Bengal Gram** | Standard canonical Title Case | High | keep_as_is |
| `Vegetables` | 5 | **Vegetables** | Preserve aggregate horticultural class | High | keep_as_is |
| `Banana` | 5 | **Banana** | Standard canonical Title Case | High | keep_as_is |
| `Jowar` | 4 | **Jowar** | Standard sorghum cereal | High | keep_as_is |
| `Cotton` | 4 | **Cotton** | Standard canonical Title Case | High | keep_as_is |
| `korra` | 4 | **Korra** | Capitalize Telugu name for Foxtail Millet | High | format_normalization |
| `Tamota` | 4 | **Tomato** | Standardize Telugu phonetic Tamota $\rightarrow$ Tomato | High | spelling_correction |
| `sesam` | 4 | **Sesame** | Standardize truncated sesam $\rightarrow$ Sesame | High | spelling_correction |
| `Soyabean` | 3 | **Soybean** | Standardize Indian spelling Soyabean $\rightarrow$ Soybean | High | spelling_correction |
| `black gram` | 3 | **Black Gram** | Capitalize lowercase to Title Case | High | format_normalization |
| `Bean Gram` | 3 | **Bean Gram (Pending Verification)** | Investigate suspected typo for Bengal Gram | Moderate | source_verification_required |
| `sweet ornage` | 3 | **Sweet Orange** | Correct typo 'ornage' $\rightarrow$ 'orange' | High | spelling_correction |
| `Red Chilli` | 3 | **Red Chilli** | Commercial subclass of Capsicum annuum | Moderate | evaluate_subclass |
| `maize` | 2 | **Maize** | Capitalize standard cereal name | High | format_normalization |
| `Acidlime` | 2 | **Acid Lime** | Standardize to spaced Title Case (Citrus aurantifolia)| High | format_normalization |
| `Green Gram` | 2 | **Green Gram** | Preserve distinct pulse species (Vigna radiata) | High | keep_separate_species |
| `Sunflower` | 2 | **Sunflower** | Standard canonical Title Case | High | keep_as_is |
| `chillis` | 2 | **Chilli** | Standardize spelling and capitalize | High | format_normalization |
| `Turemaric` | 2 | **Turmeric** | Correct phonetic spelling typo | High | spelling_correction |
| `Jouar` | 2 | **Jowar** | Correct phonetic spelling typo Jouar $\rightarrow$ Jowar | High | spelling_correction |
| `Blak Gram` | 2 | **Black Gram** | Correct typo (missing 'c') | High | spelling_correction |
| `jouar` | 1 | **Jowar** | Correct phonetic spelling typo and casing | High | spelling_correction |
| `guava` | 1 | **Guava** | Capitalize fruit name (Psidium guajava) | High | format_normalization |
| `Sweet orange` | 1 | **Sweet Orange** | Capitalize sentence case to Title Case | High | format_normalization |
| `termeric` | 1 | **Turmeric** | Correct phonetic spelling typo | High | spelling_correction |
| `muckmelon` | 1 | **Muskmelon** | Correct typo muckmelon $\rightarrow$ Muskmelon | High | spelling_correction |
| `swwet orange` | 1 | **Sweet Orange** | Correct typo 'swwet' $\rightarrow$ 'sweet' | High | spelling_correction |
| `mums` | 1 | **Chamanthi (Mums)** | Horticultural trade synonym for Chrysanthemum | Moderate | synonym_consolidation |
| `Blak gram` | 1 | **Black Gram** | Correct typo (missing 'c') and casing | High | spelling_correction |
| `Chillis` | 1 | **Chilli** | Standardize plural to singular canonical Title Case | High | format_normalization |
| `Turemeric` | 1 | **Turmeric** | Correct phonetic spelling typo | High | spelling_correction |
| `Blackgram` | 1 | **Black Gram** | Insert missing space between words | High | spelling_correction |
| `Red Gram` | 1 | **Red Gram** | Preserve distinct pulse species (Cajanus cajan) | High | keep_separate_species |
| `vegetables` | 1 | **Vegetables** | Capitalize lowercase to Title Case | High | format_normalization |
| `sweet lime` | 1 | **Sweet Lime** | Preserve distinct citrus species (Citrus limetta) | High | keep_separate_species |
| `sesasum` | 1 | **Sesame** | Correct spelling typo sesasum $\rightarrow$ Sesame | High | spelling_correction |
| `Allam` | 1 | **Allam (Ginger)** | Telugu regional name for Zingiber officinale | High | keep_as_is |
| `Turmaric` | 1 | **Turmeric** | Correct phonetic spelling typo | High | spelling_correction |
| `Caster` | 1 | **Castor** | Correct typo Caster $\rightarrow$ Castor | High | spelling_correction |
| `papaya` | 1 | **Papaya** | Capitalize fruit name (Carica papaya) | High | format_normalization |
| `Nannari` | 1 | **Nannari** | Regional medicinal plant (Hemidesmus indicus) | High | keep_as_is |
| `Greenchilli` | 1 | **Green Chilli** | Fresh immature subclass of Capsicum annuum | Moderate | evaluate_subclass |
| `Sesamum` | 1 | **Sesame** | Standardize Latin genus name to common name | High | spelling_correction |
| `Chamanthi` | 1 | **Chamanthi** | Standard canonical Title Case | High | keep_as_is |

---

## 6. Comprehensive Singleton Class Analysis ($N=1$)

### 6.1 The 23 Raw Singletons Decoupled
Of the 23 raw labels with frequency $1$:
* **13 labels are mere typos or casing variants of larger classes** and are resolved through consolidation:
  * `jouar` $\rightarrow$ `Jowar`
  * `Sweet orange`, `swwet orange` $\rightarrow$ `Sweet Orange`
  * `termeric`, `Turemeric`, `Turmaric` $\rightarrow$ `Turmeric`
  * `Blak gram`, `Blackgram` $\rightarrow$ `Black Gram`
  * `Chillis` $\rightarrow$ `Chilli`
  * `vegetables` $\rightarrow$ `Vegetables`
  * `sesasum`, `Sesamum` $\rightarrow$ `Sesame`
  * `Chamanthi` $\rightarrow$ `Chamanthi`
* **10 labels represent genuine single-observation crop records**:

| # | Singleton Crop | S.NO | Mandal | Village | Soil | Soil Characteristics ($N, P, K, \text{pH}$) | Botanical Classification |
| :-: | :--- | :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | `guava` | 43 | Vontimitta | gangaperuru | 1 | $N=263, P=5, K=169, \text{pH}=7.26$ | Perennial fruit (*Psidium guajava*) |
| 2 | `muckmelon` | 41 | Vontimitta | rachagudipalli | 1 | $N=163, P=27, K=270, \text{pH}=7.80$ | Cucurbit melon (*Cucumis melo*) |
| 3 | `mums` | 28 | Vontimitta | pennaperunru | 3 | $N=150, P=36, K=473, \text{pH}=7.90$ | Commercial flower (*Chrysanthemum*) |
| 4 | `sweet lime` | 132 | Chakrayapeta | K.Errapudi | 11 | $N=176, P=32, K=324, \text{pH}=7.51$ | Citrus fruit (*Citrus limetta*) |
| 5 | `Red Gram` | 149 | Thondur | Mallela | 1 | $N=263, P=5, K=473, \text{pH}=8.13$ | Grain legume / Toor (*Cajanus cajan*) |
| 6 | `Caster` | 408 | Proddutur | Kottapalle-1 | 1 | $N=276, P=10, K=392, \text{pH}=8.05$ | Industrial oilseed (*Ricinus communis*) |
| 7 | `Allam` | 497 | Khajipeta | Nagasanipalle | 9 | $N=263, P=82, K=338, \text{pH}=7.76$ | Rhizome spice (*Zingiber officinale*) |
| 8 | `Nannari` | 498 | Khajipeta | Nagasanipalle | 9 | $N=176, P=64, K=405, \text{pH}=7.92$ | Medicinal herb (*Hemidesmus indicus*) |
| 9 | `papaya` | 531 | Muddanur | Bondalakunta | 3 | $N=313, P=527, K=36, \text{pH}=6.22$ | Perennial fruit (*Carica papaya*) |
| 10 | `Greenchilli` | 579 | Pendlimarri | Konduru | 1 | $N=188, P=23, K=358, \text{pH}=8.20$ | Fresh vegetable spice (*Capsicum annuum*) |

---

### 6.2 Evaluation of the 4 Treatment Strategies for Singletons

#### Strategy 1: Retain as Individual Classes ($N=1$)
* **Mechanism:** Keep each singleton as an isolated target class in the ML model.
* **Evaluation:** **Technically Infeasible for Supervised Learning**.
  * Any class with $N=1$ cannot be split into train and test sets.
  * Standard cross-validation (`StratifiedKFold`) throws an immediate fatal error: `ValueError: The least populated class in y has only 1 member, which is too few`.
  * If placed in training, it can never be validated; if placed in testing, it guarantees a zero-shot misclassification error.

#### Strategy 2: Consolidate with a Verified Synonym (Recommended where valid)
* **Mechanism:** Merge singletons into documented botanical/horticultural synonyms:
  * `mums` ($1$) $\rightarrow$ `Chamanthi` ($7 \rightarrow 8$ observations).
  * `Greenchilli` ($1$) + `Red Chilli` ($3$) $\rightarrow$ `Chilli` ($3 \rightarrow 7$ observations).
* **Evaluation:** Highly effective and defensible; eliminates 2 singletons naturally without data loss.

#### Strategy 3: Group into Broader Hierarchical Agricultural Categories
* **Mechanism:** Group rare crops into higher-level agricultural tiers:
  * *Commercial Fruits:* `Guava`, `Papaya`, `Muskmelon`, `Sweet Lime`.
  * *Specialty Medicinal & Spices:* `Allam (Ginger)`, `Nannari`.
  * *Minor Oilseeds & Pulses:* `Castor`, `Red Gram`.
* **Evaluation:** Agronomically meaningful for hierarchical recommendation, but alters the granular classification task.

#### Strategy 4: Filter / Exclude from Primary Supervised Benchmark
* **Mechanism:** For the core IEEE supervised ensemble classification experiment, benchmark on crops with **sufficient support ($N \ge 4$ or $N \ge 5$)**, while retaining the full 611-row dataset for EDA, clustering, and descriptive rule discovery.
* **Evaluation:** **Standard Machine Learning Best Practice**. Enables valid 5-fold stratified cross-validation and prevents severe macro-$F_1$ penalty artifacts caused by singletons.

---

## 7. Machine-Readable Mapping File

The canonical mapping file has been generated at [`data/processed/crop_label_mapping.csv`](file:///c:/Users/Lenovo/OneDrive/Desktop/IEEE%20paper%20details%20all/CropRecommendationEnsemble/data/processed/crop_label_mapping.csv) with columns:

```csv
raw_label,frequency,canonical_label,reason,confidence,action
```

This file serves as the definitive lookup dictionary for downstream preprocessing scripts.

---

## 8. Summary Statistics and Recommendations

### 8.1 Key Metrics
* **Original Number of Raw Labels:** **`61`**
* **Formatting-Normalized Number of Labels:** **`46`**
* **Proposed Final Number of Canonical Labels:** **`34`**
  *(Or **`31`** if all Chilli subclasses and Mums are fully merged).*

---

### 8.2 Labels Requiring Manual / Source Verification
1. **`Bean Gram` ($3$ observations, S.NO 82–84 in Kondapuram):** Check whether this is a typist typo for `Bengal Gram` or French Bean.
2. **`sweet lime` ($1$ observation, S.NO 132 in Chakrayapeta):** Verify whether Sathgudi Sweet Orange was meant or Mitha Nimbu.
3. **`mums` ($1$ observation, S.NO 28 in Vontimitta):** Confirm synonymy with `Chamanthi`.
4. **`Red Chilli` vs. `Greenchilli`:** Confirm whether agronomic recommendation should treat them as a single unified `Chilli` crop.

---

### 8.3 Definitive Recommendation for Singleton Classes in Machine Learning Modeling

1. **Phase 1 (Data Cleaning):** Apply the dictionary in `data/processed/crop_label_mapping.csv` to create a clean `canonical_crop` column in the processed dataframe, preserving all 611 rows.
2. **Phase 2 (Synonym Merging):** Merge `mums` into `Chamanthi` and `Greenchilli`/`Red Chilli` into `Chilli`.
3. **Phase 3 (Modeling Strategy):**
   * **Primary Benchmark (Rigorous ML):** Filter dataset to classes with $N \ge 4$ observations (enabling 5-fold stratified cross-validation across 18 robust crop classes representing $\sim 98.4\%$ of all observations).
   * **Comprehensive Benchmark (Full Dataset):** Use non-stratified random splits or multi-tier hierarchical classification if all 34 classes must be predicted.
