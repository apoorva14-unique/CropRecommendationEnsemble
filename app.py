"""
Crop Recommendation Web Application
====================================
IEEE Final Year Academic Project:
"Crop Recommendation Using Ensemble Techniques"

Deployed Inference Model:
- Champion Architecture: Extra Trees Classifier (Tuned: 200 trees, balanced weights)
- Preprocessing Pipeline: Scikit-Learn ColumnTransformer (SimpleImputer + OneHotEncoder)
- Geographic Context: Kadapa District (YSR District), Andhra Pradesh, India
"""

import warnings
warnings.filterwarnings("ignore")
import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Crop Recommendation Using Ensemble Techniques",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional academic aesthetic
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e3d2f;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #4a6b57;
        margin-bottom: 1.5rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: 2px solid #81c784;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .prediction-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2e7d32;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .prediction-crop {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1b5e20;
        margin: 0;
    }
    .prob-badge {
        font-size: 0.95rem;
        font-weight: 600;
        color: #2e7d32;
        background-color: #ffffff;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
        border: 1px solid #a5d6a7;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOAD TRAINED ARTIFACTS (CACHED, NO RETRAINING)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_ml_artifacts():
    """Load the pre-trained Extra Trees model and fitted preprocessing pipeline."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "best_model.joblib")
    pipeline_path = os.path.join(base_dir, "models", "ml_preprocessor_pipeline.joblib")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Champion model not found at {model_path}")
    if not os.path.exists(pipeline_path):
        raise FileNotFoundError(f"Preprocessing pipeline not found at {pipeline_path}")

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)
    return model, pipeline

try:
    best_model, preprocessor_pipeline = load_ml_artifacts()
except Exception as e:
    st.error(f"Error loading model artifacts: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 3. SIDEBAR: RESEARCH & SYSTEM INFORMATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🌾 Project Information")
    st.markdown("**IEEE Research Project:**  \n*Crop Recommendation Using Ensemble Techniques*")
    st.markdown("**Geographic Context:**  \nKadapa District (YSR District), Andhra Pradesh, India")
    
    st.markdown("---")
    st.markdown("### 🏆 Champion Model Card")
    st.markdown("- **Algorithm:** Extra Trees Classifier")
    st.markdown("- **Ensemble Size:** 200 Trees")
    st.markdown("- **Split Strategy:** Randomized Thresholds")
    st.markdown("- **Class Weighting:** Balanced")
    st.markdown("- **Inference Latency:** < 5 ms")

    st.markdown("---")
    st.markdown("### 📊 Benchmark Metrics")
    st.markdown("- **Top-1 Test Accuracy:** 53.72%")
    st.markdown("- **Top-3 Recommendation:** **79.34%**")
    st.markdown("- **Top-5 Recommendation:** **85.12%**")
    st.markdown("- **Weighted F1-Score:** 51.70%")

    st.markdown("---")
    st.markdown("### 📋 Quick Demo Presets")
    st.caption("Load verified Kadapa basin field samples:")
    preset = st.selectbox(
        "Choose sample soil profile:",
        ["Custom Input", "Paddy Field (Wetland)", "Cotton Field (Black Soil)", "Groundnut Field (Red Loam)"]
    )

    st.info("💡 Note: In field advisory, Top-3 recommendations provide viable alternative crop portfolios.")

# Set presets based on user selection
if preset == "Paddy Field (Wetland)":
    defaults = {
        'ph': 7.80, 'ec': 0.18, 'oc': 0.35, 'n': 260.0, 'p2o5': 45.0, 'k20': 420.0,
        's': 14.0, 'cu': 0.95, 'fc': 5.20, 'mn': 9.50, 'zn': 0.85, 'ba': 0.32,
        'temp': 33.0, 'hum': 78.0, 'rain': 880.0, 'soil': 3
    }
elif preset == "Cotton Field (Black Soil)":
    defaults = {
        'ph': 8.20, 'ec': 0.14, 'oc': 0.22, 'n': 210.0, 'p2o5': 28.0, 'k20': 380.0,
        's': 11.0, 'cu': 0.65, 'fc': 3.40, 'mn': 6.20, 'zn': 0.45, 'ba': 0.24,
        'temp': 35.5, 'hum': 68.0, 'rain': 710.0, 'soil': 1
    }
elif preset == "Groundnut Field (Red Loam)":
    defaults = {
        'ph': 7.40, 'ec': 0.08, 'oc': 0.18, 'n': 180.0, 'p2o5': 22.0, 'k20': 310.0,
        's': 8.5, 'cu': 0.50, 'fc': 2.80, 'mn': 4.80, 'zn': 0.38, 'ba': 0.20,
        'temp': 34.0, 'hum': 64.0, 'rain': 660.0, 'soil': 11
    }
else:
    # Standard median defaults
    defaults = {
        'ph': 8.02, 'ec': 0.12, 'oc': 0.20, 'n': 226.0, 'p2o5': 28.5, 'k20': 392.0,
        's': 10.0, 'cu': 0.74, 'fc': 3.73, 'mn': 6.89, 'zn': 0.50, 'ba': 0.26,
        'temp': 34.59, 'hum': 72.59, 'rain': 751.4, 'soil': 1
    }

# -----------------------------------------------------------------------------
# 4. MAIN USER INTERFACE
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">🌱 Crop Recommendation Using Ensemble Techniques</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-based crop recommendation using soil and weather conditions</div>', unsafe_allow_html=True)

# Wrap inputs inside a form for clean submission
with st.form("recommendation_form"):
    
    # --- SECTION 1: SOIL & NUTRIENT PARAMETERS ---
    st.markdown("### 🧪 1. Soil & Nutrient Parameters")
    st.caption("Laboratory soil chemistry values tested per Indian Soil Health Card standards:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ph = st.number_input("Soil pH", min_value=4.0, max_value=11.0, value=float(defaults['ph']), step=0.05,
                             help="Soil reaction: Acidic (<6.5), Neutral (6.5-7.5), Alkaline (>7.5)")
        n = st.number_input("Nitrogen (N) [kg/ha]", min_value=0.0, max_value=1200.0, value=float(defaults['n']), step=5.0,
                            help="Available Nitrogen content in kg per hectare")
        s = st.number_input("Sulfur (S) [ppm]", min_value=0.0, max_value=150.0, value=float(defaults['s']), step=0.5,
                            help="Available secondary nutrient Sulfur in parts per million")
    with col2:
        ec = st.number_input("Electrical Cond. (EC) [dS/m]", min_value=0.0, max_value=15.0, value=float(defaults['ec']), step=0.01,
                             help="Salinity indicator: Normal (<1.0 dS/m), Saline (>2.0 dS/m)")
        p2o5 = st.number_input("Phosphorus (P₂O₅) [kg/ha]", min_value=0.0, max_value=1200.0, value=float(defaults['p2o5']), step=1.0,
                               help="Available Phosphorus content in kg per hectare")
        cu = st.number_input("Copper (CU) [ppm]", min_value=0.0, max_value=25.0, value=float(defaults['cu']), step=0.05,
                             help="DTPA-extractable Copper micronutrient")
    with col3:
        oc = st.number_input("Organic Carbon (OC) [%]", min_value=0.0, max_value=5.0, value=float(defaults['oc']), step=0.01,
                             help="Soil organic carbon percentage (Low: <0.5%, Medium: 0.5-0.75%)")
        k20 = st.number_input("Potassium (K₂O) [kg/ha]", min_value=0.0, max_value=1500.0, value=float(defaults['k20']), step=5.0,
                              help="Available Potassium content in kg per hectare")
        fc = st.number_input("Ferric / Iron Index (FC) [ppm]", min_value=0.0, max_value=80.0, value=float(defaults['fc']), step=0.1,
                             help="DTPA-extractable Iron / Ferric content")
    with col4:
        mn = st.number_input("Manganese (MN) [ppm]", min_value=0.0, max_value=80.0, value=float(defaults['mn']), step=0.1,
                             help="Available Manganese micronutrient")
        zn = st.number_input("Zinc (ZN) [ppm]", min_value=0.0, max_value=30.0, value=float(defaults['zn']), step=0.05,
                             help="Available Zinc micronutrient (Deficient <0.6 ppm)")
        ba = st.number_input("Boron Index (BA) [ppm]", min_value=0.0, max_value=15.0, value=float(defaults['ba']), step=0.02,
                             help="Available Boron micronutrient index")

    st.markdown("---")

    # --- SECTION 2: WEATHER PARAMETERS ---
    st.markdown("### 🌦️ 2. Weather Parameters")
    st.caption("Localized agro-climatic conditions during the crop growing cycle:")
    
    wcol1, wcol2, wcol3 = st.columns(3)
    with wcol1:
        temperature = st.number_input("Temperature [°C]", min_value=10.0, max_value=55.0, value=float(defaults['temp']), step=0.5,
                                      help="Mean ambient growing temperature")
    with wcol2:
        humidity = st.number_input("Relative Humidity [%]", min_value=10.0, max_value=100.0, value=float(defaults['hum']), step=1.0,
                                   help="Mean atmospheric relative humidity percentage")
    with wcol3:
        rainfall = st.number_input("Annual Rainfall [mm]", min_value=100.0, max_value=2500.0, value=float(defaults['rain']), step=10.0,
                                   help="Annual / seasonal cumulative rainfall in millimeters")

    st.markdown("---")

    # --- SECTION 3: SOIL TYPE ---
    st.markdown("### 🌍 3. Soil Type")
    st.caption("Physical textural classification of the farmland:")
    
    # Available soil types matching training partition
    soil_options = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13]
    soil_labels = {
        1: "Soil Type 1 — Black Clay Soil (Heavy Vertisol)",
        2: "Soil Type 2 — Deep Clayey Alluvial Soil",
        3: "Soil Type 3 — Clay Loam (Mixed Black/Red)",
        4: "Soil Type 4 — Sandy Clay Loam",
        5: "Soil Type 5 — Red Sandy Soil",
        7: "Soil Type 7 — Mixed Red Gravelly Soil",
        8: "Soil Type 8 — Silt Clay Wetland Soil",
        9: "Soil Type 9 — Saline / Alkaline Heavy Soil",
        10: "Soil Type 10 — Sandy Loam (Light Riverbed)",
        11: "Soil Type 11 — Red Loamy Soil (Dryland)",
        12: "Soil Type 12 — Colluvial Red Gravelly Loam",
        13: "Soil Type 13 — Calcareous Black Soil"
    }
    
    selected_soil = st.selectbox(
        "Select Soil Textural Category:",
        options=soil_options,
        index=soil_options.index(defaults['soil']),
        format_func=lambda x: soil_labels.get(x, f"Soil Type {x}")
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🌱 Recommend Crop")

# -----------------------------------------------------------------------------
# 5. MODEL INFERENCE & RESULTS DISPLAY
# -----------------------------------------------------------------------------
if submitted:
    # 1. Structure input row matching exact training preprocessor schema
    input_data = {
        'SOIL TYPE': selected_soil,
        'PH': ph,
        'EC': ec,
        'OC': oc,
        'N': n,
        'P2O5': p2o5,
        'K20': k20,
        'S': s,
        'CU': cu,
        'FC': fc,
        'MN': mn,
        'ZN': zn,
        'BA': ba,
        'Temparature': temperature,
        'Humidity': humidity,
        'Rainfall': rainfall
    }
    
    input_df = pd.DataFrame([input_data])
    
    try:
        # 2. Transform input using fitted ColumnTransformer pipeline
        input_transformed = preprocessor_pipeline.transform(input_df)
        
        # 3. Align feature names with fitted model
        input_trans_df = pd.DataFrame(input_transformed, columns=best_model.feature_names_in_)
        
        # 4. Predict Top Crop and Probabilities
        predicted_crop = best_model.predict(input_trans_df)[0]
        prediction_probas = best_model.predict_proba(input_trans_df)[0]
        classes = best_model.classes_
        
        # Sort top predictions
        top_indices = np.argsort(prediction_probas)[::-1]
        top3_crops = [(classes[i], prediction_probas[i]) for i in top_indices[:3]]
        top_prob = top3_crops[0][1]

        # 5. Display Primary Result
        st.markdown(f"""
        <div class="prediction-card">
            <div class="prediction-title">🌱 Recommended Crop</div>
            <div class="prediction-crop">{predicted_crop.upper()}</div>
            <div class="prob-badge">Prediction Probability: {top_prob:.1%}</div>
        </div>
        """, unsafe_allow_html=True)

        # 6. Display Top Predictions Table & Probability Bars
        res_col1, res_col2 = st.columns([1, 1])
        
        with res_col1:
            st.markdown("### 📊 Top Predictions")
            st.caption("Prediction Probability distribution across top candidate crops:")
            for rank, (crop_name, prob_val) in enumerate(top3_crops, 1):
                prob_pct = prob_val * 100
                st.markdown(f"**{rank}. {crop_name}** — `{prob_pct:.1f}%`")
                st.progress(float(prob_val))
            st.caption("*Values labeled as Prediction Probability (not guaranteed confidence).*")

        with res_col2:
            st.markdown("### 📋 Entered Input Summary")
            st.caption("Summary of all 16 parameters submitted for inference:")
            summary_table = pd.DataFrame({
                "Parameter": [
                    "Soil pH (PH)", "Electrical Cond. (EC)", "Organic Carbon (OC)",
                    "Nitrogen (N)", "Phosphorus (P₂O₅)", "Potassium (K₂O)",
                    "Sulfur (S)", "Copper (CU)", "Ferric / Iron Index (FC)",
                    "Manganese (MN)", "Zinc (ZN)", "Boron Index (BA)",
                    "Temperature (Temparature)", "Relative Humidity (Humidity)",
                    "Annual Rainfall (Rainfall)", "Soil Textural Class (SOIL TYPE)"
                ],
                "Submitted Value": [
                    f"{ph:.2f}", f"{ec:.2f} dS/m", f"{oc:.2f} %",
                    f"{n:.1f} kg/ha", f"{p2o5:.1f} kg/ha", f"{k20:.1f} kg/ha",
                    f"{s:.1f} ppm", f"{cu:.2f} ppm", f"{fc:.2f} ppm",
                    f"{mn:.2f} ppm", f"{zn:.2f} ppm", f"{ba:.2f} ppm",
                    f"{temperature:.1f} °C", f"{humidity:.1f} %",
                    f"{rainfall:.1f} mm", f"Soil Type {selected_soil}"
                ]
            })
            st.dataframe(summary_table, hide_index=True)

    except Exception as err:
        st.error(f"Inference error: {err}")

# -----------------------------------------------------------------------------
# 6. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d; font-size: 0.88rem;'>"
    "Crop Recommendation Using Ensemble Techniques | IEEE Final Year Project | Kadapa District Soil & Agro-Climatic Dataset"
    "</div>",
    unsafe_allow_html=True
)
