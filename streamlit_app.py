"""
Tomato Crop Disease Detection & Smart Agro-Advisor
A vibrant, multi-page Streamlit application featuring AI leaf diagnosis,
smart water and irrigation requirements, AI agronomist disease recommendations,
and disease encyclopedia.
"""

import os
import json
import time
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import streamlit as st
from PIL import Image
import numpy as np

# Suppress TensorFlow logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

# Local knowledge base
from disease_info import (
    DISEASE_DETAILS,
    get_disease_info,
    normalize_class_key,
    calculate_smart_water_plan,
    build_field_precautions,
    estimate_yield_forecast
)

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "tomato_disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "test")
CONFUSION_MATRIX_PATH = os.path.join(MODEL_DIR, "confusion_matrix.png")
TRAINING_HISTORY_PATH = os.path.join(MODEL_DIR, "training_history.png")

TARGET_IMAGE_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.60

st.set_page_config(
    page_title="AgroSense AI - Tomato Health & Irrigation Advisor",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom Vibrant CSS & Modern Aesthetics
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #10b981;
    --primary-dark: #047857;
    --primary-light: #ecfdf5;
    --tomato: #ef4444;
    --tomato-dark: #b91c1c;
    --tomato-light: #fef2f2;
    --water: #0ea5e9;
    --water-dark: #0369a1;
    --water-light: #f0f9ff;
    --amber: #f59e0b;
    --amber-light: #fffbeb;
    --bg-card: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #e2f8ef;
    background:
        radial-gradient(circle at top left, rgba(16, 185, 129, 0.18), transparent 25%),
        radial-gradient(circle at top right, rgba(59, 130, 246, 0.20), transparent 30%),
        linear-gradient(180deg, #071b18 0%, #0b1320 35%, #0d1728 100%);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    color: #ecfdf5;
}

/* Main Container Adjustments */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1320px;
}

/* Premium Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(7, 30, 26, 0.98) 0%, rgba(16, 185, 129, 0.9) 28%, rgba(14, 165, 233, 0.88) 72%, rgba(30, 64, 175, 0.9) 100%);
    border: 1px solid rgba(110, 231, 183, 0.35);
    border-radius: 28px;
    padding: 2.4rem 2.5rem;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 24px 60px -20px rgba(16, 185, 129, 0.5);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
}

.hero-banner::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, rgba(255,255,255,0.10), rgba(255,255,255,0.02), rgba(255,255,255,0.10));
    pointer-events: none;
}

.hero-banner::after {
    content: "🍅";
    position: absolute;
    right: 25px;
    bottom: -15px;
    font-size: 8.5rem;
    opacity: 0.16;
    pointer-events: none;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    margin: 0;
    line-height: 1.15;
    letter-spacing: -0.6px;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 1.06rem;
    margin-top: 0.7rem;
    opacity: 0.96;
    font-weight: 400;
    max-width: 820px;
    position: relative;
    z-index: 1;
}

/* Modern Premium Cards */
.agro-card {
    background: rgba(12, 21, 34, 0.9);
    border: 1px solid rgba(110, 231, 183, 0.22);
    border-radius: 22px;
    padding: 1.5rem;
    box-shadow: 0 18px 34px -14px rgba(16, 185, 129, 0.18);
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1.2rem;
}

.agro-card:hover {
    box-shadow: 0 18px 34px -12px rgba(15, 118, 110, 0.22);
    transform: translateY(-2px);
}

/* Premium pill badges */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
}

.badge-healthy {
    background: linear-gradient(135deg, #d1fae5, #bbf7d0);
    color: #065f46;
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.badge-warning {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    color: #92400e;
    border: 1px solid rgba(245, 158, 11, 0.2);
}

.badge-danger {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #991b1b;
    border: 1px solid rgba(239, 68, 68, 0.2);
}

.badge-water {
    background: linear-gradient(135deg, #e0f2fe, #bae6fd);
    color: #075985;
    border: 1px solid rgba(14, 165, 233, 0.18);
}

/* Water Decision Alert Boxes */
.water-banner-yes {
    background: linear-gradient(135deg, #0369a1 0%, #0ea5e9 100%);
    color: white;
    padding: 1.4rem 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    box-shadow: 0 18px 28px -16px rgba(14, 165, 233, 0.45);
}

.water-banner-no {
    background: linear-gradient(135deg, #991b1b 0%, #ef4444 100%);
    color: white;
    padding: 1.4rem 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    box-shadow: 0 18px 28px -16px rgba(239, 68, 68, 0.4);
}

.water-banner-caution {
    background: linear-gradient(135deg, #b45309 0%, #f59e0b 100%);
    color: white;
    padding: 1.4rem 1.8rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
    box-shadow: 0 18px 28px -16px rgba(245, 158, 11, 0.45);
}

/* Metric Pill Grid */
.stat-box {
    background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(236, 254, 255, 0.9));
    border: 1px solid rgba(14, 165, 233, 0.16);
    border-radius: 18px;
    padding: 1.1rem;
    text-align: center;
    box-shadow: 0 10px 18px rgba(14, 165, 233, 0.08);
}

.stat-val {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}

.stat-lbl {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* Premium chat / advisory cards */
.chat-doctor {
    background: linear-gradient(135deg, rgba(240, 253, 244, 0.9), rgba(236, 254, 255, 0.9));
    border: 1px solid rgba(16, 185, 129, 0.18);
    border-left: 5px solid #10b981;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 18px rgba(16, 185, 129, 0.08);
}

.chat-user {
    background: linear-gradient(135deg, rgba(248,250,252,0.9), rgba(239,246,255,0.9));
    border: 1px solid rgba(59, 130, 246, 0.16);
    border-right: 5px solid #3b82f6;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 18px rgba(59, 130, 246, 0.08);
}

/* Clean sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(248,250,252,0.96) 0%, rgba(240,253,244,0.96) 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.2);
    backdrop-filter: blur(10px);
}

/* Premium buttons */
.stButton>button {
    border-radius: 14px;
    font-weight: 800;
    padding: 0.72rem 1.3rem;
    transition: all 0.2s ease;
    background: linear-gradient(135deg, #10b981, #0ea5e9);
    color: white;
    border: none;
    box-shadow: 0 15px 30px rgba(16, 185, 129, 0.22);
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 18px 32px rgba(14, 165, 233, 0.24);
}

.metric-card {
    background: linear-gradient(135deg, rgba(236, 254, 255, 0.9), rgba(240, 253, 244, 0.9));
    border: 1px solid rgba(16, 185, 129, 0.16);
    border-radius: 20px;
    padding: 16px;
    height: 100%;
    box-shadow: 0 10px 18px rgba(14, 165, 233, 0.08);
}

.agent-card {
    background: linear-gradient(135deg, rgba(255,247,237,0.94), rgba(239,246,255,0.92), rgba(236,253,245,0.94));
    border: 1px solid rgba(251, 146, 60, 0.2);
    border-radius: 24px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 18px 34px rgba(249, 115, 22, 0.12);
}

/* Progress bar color */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #10b981, #22c55e, #0ea5e9, #f59e0b);
}

/* Premium card polish */
div[data-testid="stExpander"] > div {
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    background: rgba(7, 15, 23, 0.82);
    border: 1px solid rgba(110, 231, 183, 0.2);
    border-radius: 18px;
    padding: 12px 18px;
    margin-bottom: 18px;
    box-shadow: 0 18px 36px rgba(2, 5, 10, 0.35);
    backdrop-filter: blur(12px);
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    color: #ecfdf5;
}

.topbar-logo {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #10b981, #0ea5e9);
    color: white;
    font-size: 1.1rem;
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.22);
}

.analytics-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,253,244,0.82));
    border: 1px solid rgba(16, 185, 129, 0.18);
    border-radius: 20px;
    padding: 18px 20px;
    box-shadow: 0 12px 28px rgba(15, 118, 110, 0.08);
    margin-bottom: 18px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-logo">🍅</div>
        <span>AgroSense AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Cached Model & Metadata Loader
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading Deep Learning CNN Model...")
def load_detection_resources() -> Tuple[Optional[keras.Model], List[str], Optional[str]]:
    """
    Loads Keras CNN model and class names JSON with graceful fallback.
    """
    if not os.path.exists(MODEL_PATH):
        return None, [], f"Model file not found at: {MODEL_PATH}. Please run train_model.py first."

    if not os.path.exists(CLASS_NAMES_PATH):
        return None, [], f"Class mapping not found at: {CLASS_NAMES_PATH}."

    try:
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            class_names = json.load(f)

        model = keras.models.load_model(MODEL_PATH)
        return model, class_names, None
    except Exception as e:
        return None, [], f"Failed to initialize model: {str(e)}"


def preprocess_image_array(image: Image.Image, model: keras.Model) -> np.ndarray:
    """
    Preprocesses PIL image to match model input specs (224, 224, 3).
    """
    img_rgb = image.convert("RGB")
    img_resized = img_rgb.resize(TARGET_IMAGE_SIZE, Image.Resampling.BILINEAR)
    img_arr = np.array(img_resized, dtype=np.float32)

    has_rescaling = False
    if model is not None:
        has_rescaling = any(
            "rescaling" in layer.name.lower() or isinstance(layer, keras.layers.Rescaling)
            for layer in model.layers
        )

    if not has_rescaling:
        img_arr = img_arr / 255.0

    return np.expand_dims(img_arr, axis=0)


def discover_sample_images() -> Dict[str, str]:
    """
    Finds one sample image for each class from dataset/test if available.
    """
    samples = {}
    if not os.path.exists(DATASET_DIR):
        return samples

    for folder in sorted(os.listdir(DATASET_DIR)):
        folder_path = os.path.join(DATASET_DIR, folder)
        if os.path.isdir(folder_path):
            files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if files:
                display_label = folder.replace("___", " - ").replace("_", " ").title()
                samples[display_label] = os.path.join(folder_path, files[0])
    return samples


# Load model
cnn_model, class_names, load_error = load_detection_resources()
sample_images_dict = discover_sample_images()

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "scan_result" not in st.session_state:
    st.session_state.scan_result = None

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = [
        {
            "role": "doctor",
            "text": "Hello! I am your AI Agronomist & Tomato Crop Doctor. Upload a leaf photo in the Scanner or ask me any question about disease diagnosis, treatment remedies, or smart watering!"
        }
    ]

# -----------------------------------------------------------------------------
# Executive Summary Tiles
# -----------------------------------------------------------------------------

def get_summary_tiles():
    if st.session_state.scan_result:
        res = st.session_state.scan_result
        yield_forecast = estimate_yield_forecast(res["raw_class"], res["confidence"])
        return [
            {"label": "Detected", "value": res["disease_name"], "tone": "green"},
            {"label": "Confidence", "value": f"{res['confidence']:.1f}%", "tone": "blue"},
            {"label": "Yield Forecast", "value": f"{yield_forecast['yield_percent']:.1f}%", "tone": "amber"},
            {"label": "Field Status", "value": res["status"], "tone": "red" if res["status"] != "Healthy" else "green"},
        ]
    return [
        {"label": "Detected", "value": "No scan", "tone": "blue"},
        {"label": "Confidence", "value": "--", "tone": "green"},
        {"label": "Yield Forecast", "value": "--", "tone": "amber"},
        {"label": "Field Status", "value": "Awaiting", "tone": "red"},
    ]


# -----------------------------------------------------------------------------
# Sidebar Navigation & Quick Dashboard
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem 0;">
        <div style="font-size: 3.2rem; line-height: 1;">🍅🌱</div>
        <h2 style="margin: 6px 0 0 0; color: #047857; font-size: 1.5rem; font-weight: 800;">AgroSense AI</h2>
        <p style="color: #64748b; font-size: 0.85rem; margin: 2px 0 0 0;">Smart Tomato Crop Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    selected_page = st.radio(
        "Navigation",
        [
            "🌿 Leaf Disease Scanner",
            "💧 Smart Water & Irrigation Advisor",
            "🤖 AI Agronomist & Treatment Doctor",
            "📚 Disease Encyclopedia",
            "📊 Model Analytics & Architecture",
            "ℹ️ About & User Guide"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # System Status Card
    if cnn_model is not None:
        st.markdown(f"""
        <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #10b981; font-size: 1.2rem;">●</span>
                <strong style="color: #065f46; font-size: 0.88rem;">CNN Model Online</strong>
            </div>
            <div style="color: #047857; font-size: 0.78rem; margin-top: 4px;">
                10 Tomato Classes Active<br>
                Target Resolution: 224×224 px
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 12px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: #ef4444; font-size: 1.2rem;">●</span>
                <strong style="color: #991b1b; font-size: 0.88rem;">Model Offline</strong>
            </div>
            <div style="color: #b91c1c; font-size: 0.75rem; margin-top: 4px;">
                {load_error}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Active Scan Preview Pill
    if st.session_state.scan_result:
        sr = st.session_state.scan_result
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,253,244,0.9)); border: 1px solid rgba(16,185,129,0.18); border-radius: 16px; padding: 12px; box-shadow: 0 12px 24px rgba(15,118,110,0.08);">
            <span style="font-size: 0.75rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">Latest Diagnosis</span>
            <div style="font-weight: 800; color: #0f172a; font-size: 0.96rem; margin-top: 6px;">
                {sr['disease_name']}
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; gap: 8px;">
                <span style="font-size: 0.76rem; color: #10b981; font-weight: 700;">Confidence: {sr['confidence']:.1f}%</span>
                <span class="badge-pill" style="font-size: 0.7rem; background: {sr['badge_color']}; color: white; border: none;">
                    {sr['severity']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 2rem;">
        IBM Project • Advanced Agro-AI Suite<br>
        Version 2.0 (Streamlit Edition)
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# PAGE 1: 🌿 LEAF DISEASE SCANNER
# =============================================================================
if selected_page == "🌿 Leaf Disease Scanner":
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">Tomato Leaf Disease Scanner</h1>
        <p class="hero-subtitle">
            Upload a photograph of a tomato leaf or choose from sample specimens. Our deep learning CNN instantly analyzes foliar morphology, assesses disease severity, and calculates urgent moisture and treatment needs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if load_error:
        st.error(f"⚠️ Model Unavailable: {load_error}")
        st.info("Please train the model first by running: `python train_model.py`")

    summary_tiles = get_summary_tiles()
    summary_cols = st.columns(4)
    for i, tile in enumerate(summary_tiles):
        with summary_cols[i]:
            tone = tile["tone"]
            if tone == "green":
                bg = "linear-gradient(135deg, rgba(16,185,129,0.14), rgba(236,253,245,0.9))"
                border = "rgba(16,185,129,0.2)"
                text = "#065f46"
            elif tone == "blue":
                bg = "linear-gradient(135deg, rgba(14,165,233,0.12), rgba(239,246,255,0.9))"
                border = "rgba(14,165,233,0.2)"
                text = "#0f172a"
            elif tone == "amber":
                bg = "linear-gradient(135deg, rgba(251,146,60,0.12), rgba(255,247,237,0.9))"
                border = "rgba(251,146,60,0.2)"
                text = "#9a4d00"
            else:
                bg = "linear-gradient(135deg, rgba(239,68,68,0.12), rgba(254,242,242,0.9))"
                border = "rgba(239,68,68,0.2)"
                text = "#7f1d1d"

            st.markdown(f"""
            <div style="background: {bg}; border: 1px solid {border}; border-radius: 18px; padding: 14px 16px; min-height: 110px; box-shadow: 0 14px 28px rgba(15, 23, 42, 0.04);">
                <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; color: #475569;">{tile['label']}</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: {text}; margin-top: 10px; line-height: 1.2;">{tile['value']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1.2], gap="large")

    selected_image: Optional[Image.Image] = None
    image_source_label = ""

    with col_input:
        st.markdown("### 📸 Provide Leaf Image")

        input_tabs = st.tabs(["📁 File Upload", "📷 Camera Capture", "🧪 Sample Gallery"])

        with input_tabs[0]:
            uploaded_file = st.file_uploader(
                "Upload high-resolution leaf photo (JPG, JPEG, PNG)",
                type=["jpg", "jpeg", "png"],
                key="leaf_uploader"
            )
            if uploaded_file is not None:
                try:
                    selected_image = Image.open(uploaded_file)
                    image_source_label = f"Uploaded: {uploaded_file.name}"
                except Exception as e:
                    st.error(f"Failed to load image: {e}")

        with input_tabs[1]:
            camera_img = st.camera_input("Take a photo of a tomato leaf with your camera")
            if camera_img is not None:
                try:
                    selected_image = Image.open(camera_img)
                    image_source_label = "Live Camera Capture"
                except Exception as e:
                    st.error(f"Camera capture error: {e}")

        with input_tabs[2]:
            if sample_images_dict:
                st.caption("Select a verified dataset sample to test instantly:")
                chosen_sample = st.selectbox("Select sample specimen:", list(sample_images_dict.keys()))
                if chosen_sample:
                    sample_path = sample_images_dict[chosen_sample]
                    if os.path.exists(sample_path):
                        selected_image = Image.open(sample_path)
                        image_source_label = f"Sample: {chosen_sample}"
            else:
                st.info("No sample dataset images discovered in `dataset/test`.")

        if selected_image is not None:
            st.markdown(f"**Selected Image Preview** ({image_source_label})")
            st.image(selected_image, use_container_width=True, caption=image_source_label)

            scan_btn = st.button("🔬 Run Diagnostic AI Analysis", type="primary", use_container_width=True)
        else:
            scan_btn = False

    # Inference & Results
    with col_result:
        st.markdown("### 📋 Diagnostic & Water Assessment")

        # Perform inference on button click OR show existing session result
        run_prediction = scan_btn and (selected_image is not None) and (cnn_model is not None)

        if run_prediction:
            with st.spinner("Analyzing foliar cellular patterns & running CNN inference..."):
                try:
                    tensor = preprocess_image_array(selected_image, cnn_model)
                    raw_preds = cnn_model.predict(tensor, verbose=0)[0]
                    max_idx = int(np.argmax(raw_preds))
                    max_prob = float(raw_preds[max_idx])
                    conf_pct = max_prob * 100.0

                    predicted_class = class_names[max_idx] if max_idx < len(class_names) else f"Class_{max_idx}"
                    info = get_disease_info(predicted_class)

                    # Calculate probabilities breakdown
                    breakdown = []
                    for i, p in enumerate(raw_preds):
                        c_raw = class_names[i] if i < len(class_names) else f"Class_{i}"
                        c_lbl = c_raw.replace("___", " - ").replace("_", " ").title()
                        breakdown.append({"label": c_lbl, "prob": float(p) * 100.0})
                    breakdown.sort(key=lambda x: x["prob"], reverse=True)

                    # Calculate immediate water verdict
                    water_plan = calculate_smart_water_plan(
                        disease_key=predicted_class,
                        growth_stage="Vegetative Growth (Weeks 4-6)",
                        soil_type="Loamy Soil (Optimal moisture holding capacity)",
                        soil_moisture="Top 2 Inches Dry",
                        weather="Moderate & Sunny (22-29°C)"
                    )

                    # Save in session state
                    st.session_state.scan_result = {
                        "disease_name": info["name"],
                        "raw_class": predicted_class,
                        "scientific_name": info.get("scientific_name", "Solanum lycopersicum"),
                        "category": info.get("category", "General"),
                        "status": info["status"],
                        "severity": info["severity"],
                        "badge_color": info.get("accent_color", "#10b981"),
                        "confidence": conf_pct,
                        "confidence_ratio": max_prob,
                        "description": info["description"],
                        "symptoms": info["symptoms"],
                        "prevention": info["prevention"],
                        "immediate_action": info["immediate_action"],
                        "water_guidance": info.get("water_guidance", {}),
                        "treatment_guide": info.get("treatment_guide", {}),
                        "top_5": breakdown[:5],
                        "water_plan": water_plan,
                        "image": selected_image
                    }
                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

        # Display result if available in session
        if st.session_state.scan_result:
            res = st.session_state.scan_result
            wg = res.get("water_guidance", {})
            wp = res.get("water_plan", {})

            # Result Header Card
            status_bg = "#ecfdf5" if res["status"] == "Healthy" else "#fef2f2"
            status_border = "#a7f3d0" if res["status"] == "Healthy" else "#fecaca"
            badge_class = "badge-healthy" if res["status"] == "Healthy" else ("badge-warning" if res["severity"] == "Moderate" else "badge-danger")

            st.markdown(f"""
            <div style="background: {status_bg}; border: 1px solid {status_border}; border-radius: 16px; padding: 1.5rem; margin-bottom: 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span class="badge-pill {badge_class}">{res['status']} • {res['category']}</span>
                        <h2 style="margin: 8px 0 2px 0; color: #0f172a; font-size: 1.7rem;">{res['disease_name']}</h2>
                        <span style="font-style: italic; color: #475569; font-size: 0.9rem;">{res['scientific_name']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Confidence</span>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {res['badge_color']};">{res['confidence']:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Confidence Progress Bar
            st.progress(min(1.0, res["confidence_ratio"]))

            if res["confidence"] < 60.0:
                st.warning("⚠️ Low Diagnostic Confidence: Please ensure the leaf is clearly centered, well-lit, and in sharp focus.")

            # -----------------------------------------------------------------
            # EXPLICIT WATER REQUIREMENT VERDICT (User requirement)
            # -----------------------------------------------------------------
            water_verdict = wg.get("verdict", "CAUTION - Base Watering Only")
            water_method = wg.get("method", "Base Drip Irrigation")
            daily_vol = wg.get("daily_volume", "1.2 - 1.5 Liters / plant")

            st.markdown(f"""
            <div class="agro-card" style="border-left: 6px solid #0ea5e9; background: #f0f9ff;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.8rem;">💧</span>
                    <div>
                        <span style="font-size: 0.78rem; font-weight: 800; text-transform: uppercase; color: #0369a1; letter-spacing: 0.5px;">
                            Water & Irrigation Verdict For This Condition
                        </span>
                        <h4 style="margin: 2px 0 0 0; color: #0c4a6e; font-size: 1.25rem;">
                            {water_verdict}
                        </h4>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; padding-top: 10px; border-top: 1px dashed #bae6fd;">
                    <div>
                        <strong style="color: #0369a1; font-size: 0.85rem;">Approved Method:</strong>
                        <div style="color: #0f172a; font-size: 0.9rem;">{water_method}</div>
                    </div>
                    <div>
                        <strong style="color: #0369a1; font-size: 0.85rem;">Target Hydration:</strong>
                        <div style="color: #0f172a; font-size: 0.9rem;">{daily_vol}</div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 0.85rem; color: #0369a1;">
                    <strong>Foliage Wetness Risk:</strong> {wg.get('leaf_wetness_risk', 'Keep foliage dry.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            yield_forecast = estimate_yield_forecast(res["raw_class"], res["confidence"])
            precautions = build_field_precautions(res["raw_class"], res["confidence"])

            st.markdown(f"""
            <div class="agent-card" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 1.8rem;">📈</span>
                    <div>
                        <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #b45309; letter-spacing: 0.5px;">Yield Forecast</div>
                        <h4 style="margin: 0; color: #7c2d12; font-size: 1.4rem;">{yield_forecast['yield_percent']:.1f}% of expected harvest</h4>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px;">
                    <div class="metric-card">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #0f766e; text-transform: uppercase;">Expected Harvest</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #064e3b; margin-top: 4px;">{yield_forecast['estimated_harvest_tons_per_hectare']:.2f} t/ha</div>
                    </div>
                    <div class="metric-card" style="background: linear-gradient(135deg, #fff7ed 0%, #fef2f2 100%); border-color: #fed7aa;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #b45309; text-transform: uppercase;">Potential Loss</div>
                        <div style="font-size: 1.5rem; font-weight: 800; color: #9a4d00; margin-top: 4px;">{yield_forecast['yield_loss_percent']:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            from datetime import datetime
            current_time = datetime.now().strftime("%d %b %Y, %H:%M")

            st.markdown(f"""
            <div class="agent-card">
                <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #7c2d12; letter-spacing: 0.5px;">Field Safety Guidance</div>
                        <h4 style="margin: 0; color: #7c2d12; font-size: 1.3rem;">Precautions until the reviewer arrives</h4>
                    </div>
                    <div style="font-size: 0.72rem; color: #92400e; background: rgba(255,255,255,0.7); padding: 5px 10px; border-radius: 999px; border: 1px solid rgba(146, 64, 14, 0.18);">
                        {current_time}
                    </div>
                </div>
                <div style="color: #475569; font-size: 0.92rem; line-height: 1.8;">
                    <div style="background: rgba(255,255,255,0.5); border-radius: 14px; padding: 12px 14px; border: 1px solid rgba(251, 191, 36, 0.2);">
                        <div style="display: inline-block; background: linear-gradient(135deg, #fef3c7, #fdba74); color: #92400e; font-weight: 800; font-size: 0.7rem; padding: 5px 8px; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                            Alert
                        </div>
                        <p style="margin: 0;">{precautions[0]}</p>
                    </div>
                    <div style="margin-top: 12px;">
                        <div style="font-size: 0.7rem; font-weight: 800; color: #7c2d12; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Recommended actions</div>
                        <ul style="padding-left: 1.2rem; margin: 0;">
                            {''.join(f'<li>{step}</li>' for step in precautions[1:])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Details Tabs
            detail_tabs = st.tabs(["📝 Symptoms & Overview", "⚡ Immediate Action", "📊 Probability Breakdown"])

            with detail_tabs[0]:
                st.markdown(f"**Clinical Description:** {res['description']}")
                st.markdown("**Key Symptoms Checklist:**")
                for s in res["symptoms"]:
                    st.markdown(f"- 🔎 {s}")

            with detail_tabs[1]:
                st.markdown(f"""
                <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                    <strong style="color: #92400e;">⚡ Immediate Action Required:</strong>
                    <div style="color: #78350f; margin-top: 4px; font-size: 0.95rem;">{res['immediate_action']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Cultural Prevention Measures:**")
                for p in res["prevention"]:
                    st.markdown(f"- 🛡️ {p}")

            with detail_tabs[2]:
                st.caption("Top-5 model predictions:")
                for item in res["top_5"]:
                    col_p1, col_p2 = st.columns([3, 1])
                    with col_p1:
                        st.write(item["label"])
                        st.progress(item["prob"] / 100.0)
                    with col_p2:
                        st.markdown(f"**{item['prob']:.1f}%**")

            # Navigation Shortcuts to Deep Pages
            st.markdown("---")
            st.markdown("**Next Recommended Steps:**")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("💧 Open Smart Water Advisor", use_container_width=True):
                    st.info("Navigate to '💧 Smart Water & Irrigation Advisor' in the sidebar to calculate exact volumes and weather adjustments!")
            with col_b2:
                if st.button("🤖 Ask AI Plant Doctor", use_container_width=True):
                    st.info("Navigate to '🤖 AI Agronomist & Treatment Doctor' in the sidebar for full organic and chemical treatment remedies!")

        else:
            st.markdown("""
            <div class="stat-box" style="padding: 3rem 1.5rem; border: 2px dashed #cbd5e1;">
                <div style="font-size: 3.5rem;">🌱</div>
                <h4 style="color: #64748b; margin: 10px 0 5px 0;">No Leaf Scanned Yet</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; max-width: 320px; margin: 0 auto;">
                    Select an image from the left column and click <strong>Run Diagnostic AI Analysis</strong> to view the detailed health and moisture report.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# PAGE 2: 💧 SMART WATER & IRRIGATION ADVISOR
# =============================================================================
elif selected_page == "💧 Smart Water & Irrigation Advisor":
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #38bdf8 100%);">
        <h1 class="hero-title">Smart Water & Irrigation Advisor</h1>
        <p class="hero-subtitle">
            Dynamic precision irrigation intelligence. Determines whether your tomato plants require water right now, exact daily volume per plant, and disease-specific moisture rules to prevent pathogen outbreaks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Context Header: Auto-sync from scan or custom selection
    default_disease = "tomato_healthy"
    if st.session_state.scan_result:
        default_disease = st.session_state.scan_result["raw_class"]
        st.success(f"⚡ Synced with latest scan diagnosis: **{st.session_state.scan_result['disease_name']}** ({st.session_state.scan_result['confidence']:.1f}% confidence)")

    col_calc_inputs, col_calc_outputs = st.columns([1, 1.2], gap="large")

    with col_calc_inputs:
        st.markdown("### ⚙️ Field & Environmental Factors")

        # Disease Condition Selector
        disease_options = list(DISEASE_DETAILS.keys())
        disease_labels = [DISEASE_DETAILS[k]["name"] for k in disease_options]

        default_idx = 0
        normalized_default = normalize_class_key(default_disease)
        if normalized_default in disease_options:
            default_idx = disease_options.index(normalized_default)

        selected_disease_name = st.selectbox(
            "Current Plant Health Status:",
            options=disease_labels,
            index=default_idx
        )
        selected_disease_key = disease_options[disease_labels.index(selected_disease_name)]

        # Plant Growth Stage
        growth_stage = st.selectbox(
            "Plant Growth Stage:",
            [
                "Seedling / Young Plant (Weeks 1-3)",
                "Vegetative Growth (Weeks 4-6)",
                "Flowering Stage (Weeks 7-9)",
                "Fruit Development (Weeks 10-14)",
                "Ripening & Harvest (Weeks 15+)"
            ],
            index=1
        )

        # Soil Moisture Status
        soil_moisture = st.selectbox(
            "Current Topsoil Moisture Check (Top 2 inches):",
            [
                "Bone Dry",
                "Top 2 Inches Dry",
                "Adequately Moist (Damp to touch)",
                "Very Wet",
                "Waterlogged / Saturated"
            ],
            index=1
        )

        # Soil Type
        soil_type = st.selectbox(
            "Soil Composition:",
            [
                "Loamy Soil (Optimal moisture holding capacity)",
                "Sandy Soil (Drains fast, needs more frequent water)",
                "Clay Soil (Retains moisture long, risk of waterlogging)",
                "Peat / Potting Mix (High water holding)"
            ],
            index=0
        )

        # Ambient Weather
        weather = st.selectbox(
            "Today's Weather Condition:",
            [
                "Moderate & Sunny (22-29°C)",
                "Sunny & Hot (>30°C / 86°F)",
                "Humid & Sticky (>80% Humidity)",
                "Overcast / Cloudy (<22°C)",
                "Rainy / Wet Day"
            ],
            index=0
        )

        temperature = st.slider("Current Ambient Temperature (°C):", min_value=15.0, max_value=45.0, value=28.0, step=0.5)

    # Compute Smart Plan
    smart_plan = calculate_smart_water_plan(
        disease_key=selected_disease_key,
        growth_stage=growth_stage,
        soil_type=soil_type,
        soil_moisture=soil_moisture,
        weather=weather,
        temperature_c=temperature
    )

    with col_calc_outputs:
        st.markdown("### 💧 Irrigation Verdict & Action Plan")

        # Definitive Big Decision Banner
        decision = smart_plan["decision"]
        is_yes = "YES" in decision or "NOW" in decision
        is_no = "NO" in decision or "WITHHOLD" in decision or "DELAY" in decision
        banner_class = "water-banner-yes" if is_yes else ("water-banner-no" if is_no else "water-banner-caution")

        st.markdown(f"""
        <div class="{banner_class}">
            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; font-weight: 700;">
                Smart Irrigation Decision
            </div>
            <h2 style="margin: 4px 0 6px 0; font-size: 1.8rem; font-weight: 800; line-height: 1.2;">
                {decision}
            </h2>
            <div style="font-size: 0.95rem; opacity: 0.95;">
                {smart_plan['reasoning'][0] if smart_plan['reasoning'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Metric Tiles
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val">{smart_plan['recommended_volume_liters']} L</div>
                <div class="stat-lbl">Per Plant / Day</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="font-size: 1.2rem; padding-top: 5px;">{smart_plan['best_timing']}</div>
                <div class="stat-lbl">Optimal Time</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-val" style="font-size: 1.2rem; padding-top: 5px; color: #0284c7;">Sub-Mulch Drip</div>
                <div class="stat-lbl">Application Mode</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # Disease Specific Moisture Rules Card
        st.markdown(f"""
        <div class="agro-card">
            <h4 style="color: #0369a1; margin-top: 0;">💧 Moisture & Disease Dynamics for {smart_plan['disease_name']}</h4>
            <div style="margin-bottom: 8px;">
                <strong style="color: #475569;">Foliar Wetness Risk Level:</strong>
                <span class="badge-pill badge-danger" style="margin-left: 6px;">{smart_plan['leaf_wetness_risk']}</span>
            </div>
            <div style="margin-bottom: 12px;">
                <strong style="color: #475569;">Approved Irrigation Method:</strong> {smart_plan['irrigation_method']}
            </div>
            <strong>Mandatory Water Guidelines:</strong>
            <ul style="margin-top: 6px; padding-left: 1.2rem; color: #334155;">
        """, unsafe_allow_html=True)

        for rule in smart_plan["rules"]:
            st.markdown(f"- 🔹 {rule}")

        st.markdown("""
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 7-Day Smart Irrigation Forecast
    st.markdown("---")
    st.markdown("### 📅 Recommended 7-Day Irrigation Schedule")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sched_cols = st.columns(7)

    for i, day in enumerate(days):
        with sched_cols[i]:
            # Sample realistic rotational schedule based on disease
            if "Late Blight" in selected_disease_name:
                day_status = "0.5 L Drip" if i in [0, 4] else "REST"
                day_color = "#ef4444" if day_status != "REST" else "#94a3b8"
            elif "Spider Mites" in selected_disease_name:
                day_status = "2.0 L + Rinse" if i % 2 == 0 else "1.0 L Drip"
                day_color = "#10b981"
            elif "Bacterial" in selected_disease_name or "Early Blight" in selected_disease_name:
                day_status = "1.0 L Drip" if i in [0, 3, 5] else "REST (Dry)"
                day_color = "#f59e0b" if day_status != "REST (Dry)" else "#94a3b8"
            else:
                day_status = "1.5 L Drip" if i % 2 == 0 else "Rest / Check"
                day_color = "#10b981" if "1.5" in day_status else "#94a3b8"

            st.markdown(f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; text-align: center;">
                <strong style="font-size: 0.85rem; color: #0f172a;">{day}</strong>
                <div style="font-size: 0.8rem; font-weight: 700; color: {day_color}; margin-top: 6px;">
                    {day_status}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# PAGE 3: 🤖 AI AGRONOMIST & TREATMENT DOCTOR
# =============================================================================
elif selected_page == "🤖 AI Agronomist & Treatment Doctor":
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 100%);">
        <h1 class="hero-title">AI Agronomist & Disease Treatment Doctor</h1>
        <p class="hero-subtitle">
            Intelligent crop pathology consultant. Access verified organic and chemical treatment protocols, cultural pruning procedures, and chat interactively with our plant doctor AI for customized remedies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Active Diagnosis Banner
    current_key = "tomato_early_blight"
    if st.session_state.scan_result:
        current_key = st.session_state.scan_result["raw_class"]
        st.info(f"🌿 Current Patient Context: **{st.session_state.scan_result['disease_name']}** (Confidence: {st.session_state.scan_result['confidence']:.1f}%)")
    else:
        st.caption("No scan performed yet. Select a disease below to review treatment protocols or ask the AI Doctor:")

    info = get_disease_info(current_key)
    tg = info.get("treatment_guide", {})

    col_treat_left, col_treat_right = st.columns([1.1, 1], gap="large")

    with col_treat_left:
        st.markdown(f"### 🧪 Treatment Protocols for {info['name']}")

        st.markdown(f"""
        <div class="agro-card" style="border-left: 6px solid #10b981;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #065f46;">🌱 Organic & Biological Remedies</h4>
                <span class="badge-pill badge-healthy">Eco-Friendly</span>
            </div>
            <ul style="margin-top: 10px; padding-left: 1.2rem; color: #1e293b;">
        """, unsafe_allow_html=True)
        for org in tg.get("organic_options", ["Apply cold-pressed neem oil or copper soap spray."]):
            st.markdown(f"- 🌿 **{org}**")
        st.markdown("</ul></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="agro-card" style="border-left: 6px solid #ef4444;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #991b1b;">⚗️ Targeted Chemical Controls</h4>
                <span class="badge-pill badge-danger">Follow Safety Label</span>
            </div>
            <ul style="margin-top: 10px; padding-left: 1.2rem; color: #1e293b;">
        """, unsafe_allow_html=True)
        for chem in tg.get("chemical_options", ["Consult local extension for approved fungicides."]):
            st.markdown(f"- 🧪 **{chem}**")
        st.markdown("</ul></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="agro-card" style="border-left: 6px solid #f59e0b;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #92400e;">✂️ Cultural & Field Sanitation Steps</h4>
                <span class="badge-pill badge-warning">Prevention</span>
            </div>
            <ul style="margin-top: 10px; padding-left: 1.2rem; color: #1e293b;">
        """, unsafe_allow_html=True)
        for cult in tg.get("cultural_steps", ["Prune lower foliage and sanitize tools."]):
            st.markdown(f"- 🛡️ **{cult}**")
        st.markdown(f"""
            </ul>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #e2e8f0; font-size: 0.85rem; color: #64748b;">
                <strong>Expected Recovery Outlook:</strong> {tg.get('recovery_outlook', 'Consistent treatment halts spread to new shoots.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_treat_right:
        st.markdown("### 💬 Chat with AI Plant Doctor")

        # Quick Prompt Chips
        st.caption("Quick Suggested Questions:")
        quick_cols = st.columns(3)
        prompt_to_add = None
        if quick_cols[0].button("Can I spray neem oil?"):
            prompt_to_add = "Can I spray neem oil on this tomato plant?"
        if quick_cols[1].button("How to save other plants?"):
            prompt_to_add = "How do I prevent this from spreading to neighboring tomato and pepper plants?"
        if quick_cols[2].button("Are fruits safe to eat?"):
            prompt_to_add = "Can I still safely consume fruits harvested from this plant?"

        # Chat Input Box
        user_query = st.chat_input("Ask the AI Plant Doctor any question about disease, fungicides, or watering...")

        if prompt_to_add:
            user_query = prompt_to_add

        if user_query:
            # Append user message
            st.session_state.ai_chat_history.append({"role": "user", "text": user_query})

            # Generate smart agronomic response
            q_lower = user_query.lower()
            d_name = info["name"]

            if "neem" in q_lower or "oil" in q_lower:
                reply = (
                    f"🌿 **Neem Oil Guidance for {d_name}:**\n\n"
                    "Cold-pressed neem oil (0.5% - 1.0% dilution) is an effective natural bio-pesticide and mild anti-sporulant. "
                    "**Application Rules:**\n"
                    "1. Spray exclusively during early dawn or late twilight. Never spray under intense afternoon sunlight, as oil deposits cause leaf scalding (phototoxicity).\n"
                    "2. Coat the undersides of leaves where fungal spores and pests (like spider mites) harbor.\n"
                    "3. Repeat every 7 to 10 days until disease progression ceases."
                )
            elif "spread" in q_lower or "neighbor" in q_lower or "other plant" in q_lower:
                reply = (
                    f"🛡️ **Quarantine & Protective Shield for {d_name}:**\n\n"
                    "1. **Bottom Clearance:** Prune the lower 12-15 inches of foliage on neighboring plants so no leaves touch wet ground.\n"
                    "2. **Barrier Mulching:** Apply a 3-inch layer of clean wheat straw or black plastic mulch across all rows to stop rain-splash spore transmission.\n"
                    "3. **Tool Sterilization:** Dip pruning shears in 70% isopropyl alcohol or 10% household bleach between each plant.\n"
                    "4. **Protective Coating:** Apply a protective bio-fungicide (like *Bacillus subtilis* or copper soap) on healthy adjacent plants before rainfall."
                )
            elif "eat" in q_lower or "fruit" in q_lower or "consume" in q_lower or "safe" in q_lower:
                reply = (
                    f"🍅 **Fruit Safety Assessment:**\n\n"
                    "Unblemished, firm fruits from plants with foliar diseases (like Early Blight or Leaf Mold) are generally safe to eat after thorough washing. "
                    "**Crucial Cautions:**\n"
                    "- Discard any fruit displaying sunken black lesions, rot, or water-soaked patches (e.g. Late Blight fruit rot).\n"
                    "- If you have applied chemical fungicides (e.g., Chlorothalonil or Mancozeb), strictly observe the **Pre-Harvest Interval (PHI)** on the chemical label (typically 1 to 7 days before picking)!"
                )
            elif "water" in q_lower or "irrigate" in q_lower:
                reply = (
                    f"💧 **Water Management Protocol for {d_name}:**\n\n"
                    f"- Current Verdict: **{info.get('water_guidance', {}).get('verdict', 'Base drip only')}**\n"
                    f"- Method: **{info.get('water_guidance', {}).get('method', 'Precision drip at soil line')}**\n"
                    "- Never wet foliage! Spores require only 4-6 hours of free leaf surface water to penetrate plant stomata. Water strictly before 8:00 AM."
                )
            else:
                reply = (
                    f"👨‍⚕️ **Agronomist Recommendation for {d_name}:**\n\n"
                    f"Regarding *'{user_query}'*:\n"
                    f"- **Core Pathology:** {info['description']}\n"
                    f"- **Immediate Step:** {info['immediate_action']}\n"
                    f"- **Watering Rule:** {info.get('water_guidance', {}).get('status', 'Base drip only')}. Avoid wetting foliage.\n"
                    f"- **Suggested Treatment:** {', '.join(tg.get('organic_options', ['Prune lower leaves']))}."
                )

            st.session_state.ai_chat_history.append({"role": "doctor", "text": reply})

        # Render Chat History Container
        chat_container = st.container()
        with chat_container:
            for msg in reversed(st.session_state.ai_chat_history):
                if msg["role"] == "doctor":
                    st.markdown(f"""
                    <div class="chat-doctor">
                        <strong style="color: #047857;">🩺 AI Plant Doctor</strong>
                        <div style="margin-top: 6px; font-size: 0.92rem; line-height: 1.5;">
                            {msg['text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-user">
                        <strong style="color: #1e40af;">👤 Grower / Farmer</strong>
                        <div style="margin-top: 4px; font-size: 0.92rem;">
                            {msg['text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# =============================================================================
# PAGE 4: 📚 DISEASE ENCYCLOPEDIA
# =============================================================================
elif selected_page == "📚 Disease Encyclopedia":
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #065f46 0%, #047857 50%, #059669 100%);">
        <h1 class="hero-title">Tomato Disease Encyclopedia</h1>
        <p class="hero-subtitle">
            Comprehensive field pathology compendium covering all 10 diagnostic categories in the AgroSense AI knowledge base. Filter by pathogen category, inspect foliar symptoms, and study irrigation recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter Bar
    filter_col1, filter_col2 = st.columns([1, 2])
    with filter_col1:
        cat_filter = st.selectbox(
            "Filter by Category:",
            ["All Categories", "Fungal", "Bacterial", "Viral", "Pest", "Healthy"]
        )
    with filter_col2:
        search_query = st.text_input("🔍 Search disease name, symptom, or pathogen:", "")

    # Filtered List
    filtered_keys = []
    for k, v in DISEASE_DETAILS.items():
        if cat_filter != "All Categories":
            if cat_filter.lower() not in v.get("category", "").lower():
                continue
        if search_query:
            q = search_query.lower()
            text_corpus = f"{v['name']} {v['scientific_name']} {v['description']} {' '.join(v['symptoms'])}".lower()
            if q not in text_corpus:
                continue
        filtered_keys.append(k)

    st.markdown(f"**Showing {len(filtered_keys)} of {len(DISEASE_DETAILS)} Conditions**")

    # Grid of Cards
    for key in filtered_keys:
        item = DISEASE_DETAILS[key]
        wg = item.get("water_guidance", {})
        badge_color = item.get("accent_color", "#10b981")

        with st.expander(f"📌 {item['name']} ({item.get('category', 'Condition')}) — Severity: {item['severity']}", expanded=(len(filtered_keys) == 1)):
            c1, c2 = st.columns([1.2, 1])
            with c1:
                st.markdown(f"**Scientific Pathogen:** *{item['scientific_name']}*")
                st.markdown(f"**Summary:** {item.get('summary', item['description'])}")
                st.markdown(f"**Description:** {item['description']}")

                st.markdown("**Diagnostic Symptoms:**")
                for sym in item["symptoms"]:
                    st.markdown(f"- 🔍 {sym}")

            with c2:
                st.markdown(f"""
                <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 12px; margin-bottom: 10px;">
                    <strong style="color: #0369a1;">💧 Water & Irrigation Rule:</strong>
                    <div style="color: #0f172a; font-size: 0.9rem; margin-top: 4px;">
                        <strong>Verdict:</strong> {wg.get('verdict', 'Base drip only')}<br>
                        <strong>Method:</strong> {wg.get('method', 'Sub-mulch drip')}<br>
                        <strong>Volume:</strong> {wg.get('daily_volume', '1.2 - 1.5 L/plant')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 12px; padding: 12px;">
                    <strong style="color: #065f46;">🛡️ Immediate Response:</strong>
                    <div style="color: #064e3b; font-size: 0.9rem; margin-top: 4px;">
                        {item['immediate_action']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Analyze in Smart Water Advisor", key=f"water_btn_{key}"):
                    st.session_state.scan_result = {
                        "disease_name": item["name"],
                        "raw_class": key,
                        "confidence": 99.0,
                        "badge_color": badge_color,
                        "severity": item["severity"]
                    }
                    st.info("Disease loaded into advisor! Navigate to '💧 Smart Water & Irrigation Advisor' in sidebar.")


# =============================================================================
# PAGE 5: 📊 MODEL ANALYTICS & ARCHITECTURE
# =============================================================================
elif selected_page == "📊 Model Analytics & Architecture":
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);">
        <h1 class="hero-title">Model Performance & CNN Architecture</h1>
        <p class="hero-subtitle">
            Inspection suite for the deep learning computer vision model. View validation accuracy curves, the complete 10-class confusion matrix, and technical pipeline benchmarks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-val" style="color: #10b981;">10</div>
            <div class="stat-lbl">Class Categories</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-val" style="color: #0ea5e9;">224×224</div>
            <div class="stat-lbl">Input Dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-val" style="color: #8b5cf6;">Conv2D</div>
            <div class="stat-lbl">CNN Backbone</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat4:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-val" style="color: #f59e0b;">~1.4 MB</div>
            <div class="stat-lbl">Model File Size</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.markdown("### 📈 Training History (Loss & Accuracy)")
        if os.path.exists(TRAINING_HISTORY_PATH):
            st.image(TRAINING_HISTORY_PATH, use_container_width=True, caption="Training & Validation Accuracy/Loss Curves")
        else:
            st.info("Training history plot will appear here once generated during training.")

    with col_img2:
        st.markdown("### 🎯 10-Class Confusion Matrix")
        if os.path.exists(CONFUSION_MATRIX_PATH):
            st.image(CONFUSION_MATRIX_PATH, use_container_width=True, caption="Model Evaluation Confusion Matrix")
        else:
            st.info("Confusion matrix plot will appear here once generated during training.")

    st.markdown("---")
    st.markdown("### 🏗️ Deep Learning Architecture Breakdown")
    st.markdown("""
    | Layer | Type | Specifications | Output Shape | Function |
    |---|---|---|---|---|
    | **Input** | InputLayer | RGB 3-Channel Normalization | `(None, 224, 224, 3)` | Accepts raw photographic leaf input |
    | **Block 1** | Conv2D + BatchNorm + MaxPool | 32 Filters (3×3), ReLU | `(None, 112, 112, 32)` | Detects edges, veins, and fine foliar textures |
    | **Block 2** | Conv2D + BatchNorm + MaxPool | 64 Filters (3×3), ReLU | `(None, 56, 56, 64)` | Captures lesion boundaries and chlorotic halos |
    | **Block 3** | Conv2D + BatchNorm + MaxPool | 128 Filters (3×3), ReLU | `(None, 28, 28, 128)` | Discovers concentric target rings and mold patterns |
    | **Block 4** | Conv2D + BatchNorm + MaxPool | 256 Filters (3×3), ReLU | `(None, 14, 14, 256)` | High-level disease feature representations |
    | **Dense** | Flatten + Dropout (0.5) + Dense | 256 Units, ReLU | `(None, 256)` | Fully-connected reasoning layer with regularization |
    | **Output** | Dense (Softmax) | 10 Class Probabilities | `(None, 10)` | Normalized probability distribution across conditions |
    """)


# =============================================================================
# PAGE 6: ℹ️ ABOUT & USER GUIDE
# =============================================================================
elif selected_page == "ℹ️ About & User Guide":
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);">
        <h1 class="hero-title">About AgroSense AI & User Guide</h1>
        <p class="hero-subtitle">
            An advanced AI precision agriculture solution developed for IBM Project. Bridging the gap between edge deep learning foliar computer vision and real-time smart irrigation agronomy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c_g1, c_g2 = st.columns(2, gap="large")
    with c_g1:
        st.markdown("""
        ### 📖 How to Use This Platform
        
        1. **Leaf Diagnostic Scanner:**
           - Take a close-up photo of an affected tomato leaf.
           - Ensure the leaf fills 70%+ of the frame and is well-focused.
           - Click **Run Diagnostic AI Analysis** to receive immediate condition classification.
           
        2. **Check Smart Water Requirement:**
           - Immediately review the **Water & Irrigation Verdict** card.
           - Fungal and bacterial diseases require strict withholding of overhead water to halt spore germination.
           - Open the **Smart Water Advisor** to get tailored daily liters and schedules adjusted for weather and soil.
           
        3. **Consult AI Treatment Doctor:**
           - Receive organic bio-fungicide formulas (Neem, copper soap, *Bacillus subtilis*).
           - Ask the conversational Plant Doctor questions about pruning, PHI intervals, and neighboring crop protection.
           
        4. **Disease Encyclopedia:**
           - Review high-definition reference material for all 10 classes to confirm field findings.
        """)

    with c_g2:
        st.markdown("""
        ### 🌟 Technological Highlights
        
        - **Deep CNN Architecture:** Trained on verified tomato leaf specimens across 10 distinct health states.
        - **Dual Web Engines:** Full-featured **Streamlit UI** for rich multi-page interaction, plus standalone **Flask REST API** backend.
        - **Agronomical Water Engine:** Scientific calculation model factoring growth stage, topsoil moisture, weather evapotranspiration, and pathogen moisture dynamics.
        - **Offline-Ready:** Runs 100% locally on your computer with zero mandatory cloud dependencies or paid API keys.
        - **Built for Farmers & Researchers:** Clean, high-contrast, colorful responsive design for both desktop and field tablets.
        """)
