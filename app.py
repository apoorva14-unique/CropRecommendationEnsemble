"""
Crop Recommendation System — Streamlit Web Application
======================================================
Academic / IEEE Research Project:
"Crop Recommendation Using Ensemble Techniques"

Architecture & ML Pipeline:
- Deployed Model: Champion Extra Trees Classifier (200 trees, balanced weights)
- Feature Pipeline: Fitted ColumnTransformer (Median Imputer + OneHotEncoder)
- Features: 15 Soil Chemistry & Weather Features + 1 Categorical Soil Textural Class
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
    page_title="Crop Recommendation System — AI Decision Support",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Subtle, targeted styling strictly following the agricultural color palette:
# Primary: #176B3A | Secondary: #4F9D69 | Light Green: #EAF5EC | Dark Text: #173B2A | Muted: #66736B | Border: #D9E5DC
st.markdown("""
<style>
    /* Hero Header */
    .hero-title {
        font-size: 2.15rem;
        font-weight: 700;
        color: #176B3A;
        letter-spacing: -0.5px;
        margin-bottom: 0.15rem;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 500;
        color: #4F9D69;
        margin-bottom: 0.35rem;
    }
    .hero-supporting {
        font-size: 0.92rem;
        color: #66736B;
        margin-bottom: 1.25rem;
    }
    
    /* Result Card */
    .result-card {
        background-color: #EAF5EC;
        border: 1.5px solid #D9E5DC;
        border-radius: 10px;
        padding: 22px;
        text-align: center;
        margin: 12px 0 18px 0;
    }
    .result-badge {
        font-size: 0.85rem;
        font-weight: 700;
        color: #176B3A;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .result-crop {
        font-size: 2.5rem;
        font-weight: 800;
        color: #173B2A;
        margin: 4px 0 8px 0;
        letter-spacing: -0.5px;
    }
    .result-prob {
        display: inline-block;
        background-color: #FFFFFF;
        color: #176B3A;
        border: 1px solid #D9E5DC;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.92rem;
    }

    /* Section Subheaders */
    .section-header {
        font-size: 1.08rem;
        font-weight: 600;
        color: #173B2A;
        margin-bottom: 2px;
    }
    .section-caption {
        font-size: 0.85rem;
        color: #66736B;
        margin-bottom: 12px;
    }

    /* Primary button spacing */
    div.stButton > button:first-child {
        width: 100%;
        padding: 10px 24px;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 8px;
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
    st.markdown("### 🌾 Research Information")
    st.markdown("**IEEE Research Project:**  \n*Crop Recommendation Using Ensemble Techniques*")
    st.markdown("**Geographic Context:**  \nKadapa District (YSR District), Andhra Pradesh, India")
    
    st.markdown("---")
    st.markdown("### 🏆 Champion Model Card")
    st.markdown("- **Algorithm:** Extra Trees Classifier")
    st.markdown("- **Ensemble Size:** 200 Decision Trees")
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
    st.caption("Load verified Kadapa basin field samples for fast demonstration:")
    preset = st.selectbox(
        "Choose sample soil profile:",
        [
            "Custom Input",
            "Kadapa Cotton Profile (IEEE Benchmark)",
            "Paddy Field (Wetland)",
            "Cotton Field (Black Soil)",
            "Groundnut Field (Red Loam)"
        ]
    )

    st.caption("In agricultural advisory, Top-3 recommendations offer farmers a viable, diversified crop portfolio.")

# Populate preset defaults based on user selection
if preset == "Kadapa Cotton Profile (IEEE Benchmark)":
    defaults = {
        'ph': 8.01, 'ec': 0.12, 'oc': 0.23, 'n': 150.0, 'p2o5': 14.0, 'k20': 270.0,
        's': 7.0, 'cu': 0.03, 'fc': 16.72, 'mn': 16.69, 'zn': 1.32, 'ba': 0.26,
        'temp': 34.59, 'hum': 77.40, 'rain': 834.30, 'soil': 1
    }
elif preset == "Paddy Field (Wetland)":
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
    # Standard median dataset defaults
    defaults = {
        'ph': 8.02, 'ec': 0.12, 'oc': 0.20, 'n': 226.0, 'p2o5': 28.5, 'k20': 392.0,
        's': 10.0, 'cu': 0.74, 'fc': 3.73, 'mn': 6.89, 'zn': 0.50, 'ba': 0.26,
        'temp': 34.59, 'hum': 72.59, 'rain': 751.4, 'soil': 1
    }

# -----------------------------------------------------------------------------
# 4. MAIN USER INTERFACE — HERO SECTION
# -----------------------------------------------------------------------------
st.markdown('<div class="hero-title">🌱 Crop Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-powered crop selection using soil and weather conditions</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-supporting">Ensemble machine learning model trained using agricultural soil and climatic parameters.</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. INPUT FORM SECTION (ORGANIZED INTO PROFESSIONAL CARDS)
# -----------------------------------------------------------------------------
with st.form("recommendation_form", clear_on_submit=False):

    # --- CARD 1: SOIL & NUTRIENT PARAMETERS ---
    with st.container(border=True):
        st.markdown('<div class="section-header">🧪 Soil & Nutrient Parameters</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Laboratory soil chemistry values tested per Indian Soil Health Card standards:</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            ph = st.number_input(
                "Soil pH",
                min_value=4.0, max_value=11.0, value=float(defaults['ph']), step=0.05,
                help="Soil reaction: Acidic (<6.5), Neutral (6.5-7.5), Alkaline (>7.5)"
            )
            n = st.number_input(
                "Nitrogen (N) [kg/ha]",
                min_value=0.0, max_value=1200.0, value=float(defaults['n']), step=5.0,
                help="Available Nitrogen content in kg per hectare"
            )
            s = st.number_input(
                "Sulfur (S) [ppm]",
                min_value=0.0, max_value=150.0, value=float(defaults['s']), step=0.5,
                help="Available secondary nutrient Sulfur in parts per million"
            )
        with col2:
            ec = st.number_input(
                "Electrical Conductivity (EC) [dS/m]",
                min_value=0.0, max_value=15.0, value=float(defaults['ec']), step=0.01,
                help="Salinity indicator: Normal (<1.0 dS/m), Saline (>2.0 dS/m)"
            )
            p2o5 = st.number_input(
                "Phosphorus (P2O5) [kg/ha]",
                min_value=0.0, max_value=1200.0, value=float(defaults['p2o5']), step=1.0,
                help="Available Phosphorus content in kg per hectare"
            )
            cu = st.number_input(
                "Copper (Cu) [ppm]",
                min_value=0.0, max_value=25.0, value=float(defaults['cu']), step=0.05,
                help="DTPA-extractable Copper micronutrient"
            )
        with col3:
            oc = st.number_input(
                "Organic Carbon (OC) [%]",
                min_value=0.0, max_value=5.0, value=float(defaults['oc']), step=0.01,
                help="Soil organic carbon percentage (Low: <0.5%, Medium: 0.5-0.75%)"
            )
            k20 = st.number_input(
                "Potassium (K2O) [kg/ha]",
                min_value=0.0, max_value=1500.0, value=float(defaults['k20']), step=5.0,
                help="Available Potassium content in kg per hectare"
            )
            fc = st.number_input(
                "Ferric/Iron Index (FC) [ppm]",
                min_value=0.0, max_value=80.0, value=float(defaults['fc']), step=0.1,
                help="DTPA-extractable Iron / Ferric content"
            )
        with col4:
            mn = st.number_input(
                "Manganese (MN) [ppm]",
                min_value=0.0, max_value=80.0, value=float(defaults['mn']), step=0.1,
                help="Available Manganese micronutrient"
            )
            zn = st.number_input(
                "Zinc (Zn) [ppm]",
                min_value=0.0, max_value=30.0, value=float(defaults['zn']), step=0.05,
                help="Available Zinc micronutrient (Deficient <0.6 ppm)"
            )
            ba = st.number_input(
                "Boron Index (BA) [ppm]",
                min_value=0.0, max_value=15.0, value=float(defaults['ba']), step=0.02,
                help="Available Boron micronutrient index"
            )

    # --- CARD 2: WEATHER PARAMETERS ---
    with st.container(border=True):
        st.markdown('<div class="section-header">🌦️ Weather Parameters</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Localized agro-climatic conditions during the crop growing cycle:</div>', unsafe_allow_html=True)

        wcol1, wcol2, wcol3 = st.columns(3)
        with wcol1:
            temperature = st.number_input(
                "Temperature [°C]",
                min_value=10.0, max_value=55.0, value=float(defaults['temp']), step=0.5,
                help="Mean ambient growing season temperature"
            )
        with wcol2:
            humidity = st.number_input(
                "Relative Humidity [%]",
                min_value=10.0, max_value=100.0, value=float(defaults['hum']), step=1.0,
                help="Mean atmospheric relative humidity percentage"
            )
        with wcol3:
            rainfall = st.number_input(
                "Annual Rainfall [mm]",
                min_value=100.0, max_value=2500.0, value=float(defaults['rain']), step=10.0,
                help="Annual / seasonal cumulative rainfall in millimeters"
            )

    # --- CARD 3: SOIL TYPE ---
    with st.container(border=True):
        st.markdown('<div class="section-header">🌍 Soil Type</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-caption">Physical textural classification of the farmland:</div>', unsafe_allow_html=True)

        soil_labels = {
            1: "Soil Type 1: Black Clay Soil (Heavy Vertisol)",
            2: "Soil Type 2: Deep Clayey Alluvial Soil",
            3: "Soil Type 3: Clay Loam (Mixed Black/Red)",
            4: "Soil Type 4: Sandy Clay Loam",
            5: "Soil Type 5: Red Sandy Soil",
            7: "Soil Type 7: Mixed Red Gravelly Soil",
            8: "Soil Type 8: Silt Clay Wetland Soil",
            9: "Soil Type 9: Saline / Alkaline Heavy Soil",
            10: "Soil Type 10: Sandy Loam (Light Riverbed)",
            11: "Soil Type 11: Red Loamy Soil (Dryland)",
            12: "Soil Type 12: Colluvial Red Gravelly Loam",
            13: "Soil Type 13: Calcareous Black Soil"
        }
        soil_options = list(soil_labels.values())
        default_label = soil_labels.get(defaults['soil'], soil_options[0])

        selected_label = st.selectbox(
            "Select Soil Textural Category:",
            options=soil_options,
            index=soil_options.index(default_label)
        )
        label_to_soil = {v: k for k, v in soil_labels.items()}
        selected_soil = label_to_soil[selected_label]

    # SUBMIT BUTTON (GREEN PRIMARY WITH GOOD SPACING)
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🌱 Recommend Crop", type="primary")

# -----------------------------------------------------------------------------
# 6. MODEL INFERENCE & RESULTS SECTION
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

        # 4. Predict Champion Crop and Probabilities
        predicted_crop = best_model.predict(input_trans_df)[0]
        prediction_probas = best_model.predict_proba(input_trans_df)[0]
        classes = best_model.classes_

        # Sort top predictions
        top_indices = np.argsort(prediction_probas)[::-1]
        top3_crops = [(classes[i], prediction_probas[i]) for i in top_indices[:3]]
        top_prob = top3_crops[0][1]

        # 5. RESULT SECTION: PRIMARY RECOMMENDATION CARD
        st.markdown(f"""
        <div class="result-card">
            <div class="result-badge">🌱 RECOMMENDED CROP</div>
            <div class="result-crop">{predicted_crop.upper()}</div>
            <div class="result-prob">Prediction Probability: {top_prob:.1%}</div>
        </div>
        """, unsafe_allow_html=True)

        # 6. TWO-COLUMN LAYOUT: TOP PREDICTIONS & INPUT SUMMARY
        res_col1, res_col2 = st.columns([1, 1], gap="medium")

        with res_col1:
            with st.container(border=True):
                st.markdown('<div class="section-header">📊 Top Crop Predictions</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-caption">Ensemble multi-class probability ranking across top candidate crops:</div>', unsafe_allow_html=True)

                for rank, (crop_name, prob_val) in enumerate(top3_crops, 1):
                    prob_pct = prob_val * 100
                    st.markdown(f"**{rank}. {crop_name}** — `{prob_pct:.1f}%`")
                    st.progress(float(prob_val))

                st.caption("Prediction probability is the model's estimated probability and should not be interpreted as a guarantee.")

        with res_col2:
            with st.container(border=True):
                st.markdown('<div class="section-header">📋 Entered Input Summary</div>', unsafe_allow_html=True)
                st.markdown('<div class="section-caption">Formal report of agronomic parameters submitted for inference:</div>', unsafe_allow_html=True)

                summary_table = pd.DataFrame({
                    "Parameter": [
                        "Soil pH", "Electrical Conductivity (EC)", "Organic Carbon (OC)",
                        "Nitrogen (N)", "Phosphorus (P2O5)", "Potassium (K2O)",
                        "Sulfur (S)", "Copper (Cu)", "Ferric/Iron Index (FC)",
                        "Manganese (MN)", "Zinc (Zn)", "Boron Index (BA)",
                        "Temperature", "Relative Humidity",
                        "Annual Rainfall", "Soil Type"
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

        # 7. INFORMATION & ADVISORY DISCLAIMER BOX
        with st.container(border=True):
            st.markdown("ℹ️ **About this prediction**")
            st.markdown(
                "This system predicts a suitable crop based on the submitted soil, nutrient, weather, "
                "and soil-type parameters using an ensemble machine-learning model."
            )
            st.caption(
                "**Disclaimer:** This prediction is a machine-learning recommendation and should be considered "
                "along with local agricultural expertise, soil testing, seasonal conditions, and farming practices."
            )

    except Exception as err:
        st.error(f"Inference error: {err}")

# -----------------------------------------------------------------------------
# 7. FOOTER
# -----------------------------------------------------------------------------
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #66736B; font-size: 0.85rem; padding-bottom: 20px;'>"
    "Crop Recommendation System | IEEE Final Year Project | Kadapa Basin Agricultural Soil & Climatic Dataset"
    "</div>",
    unsafe_allow_html=True
)
