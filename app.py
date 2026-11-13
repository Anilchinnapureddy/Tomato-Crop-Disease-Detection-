"""
Tomato Crop Disease Detection - Flask Web Application
Provides a web interface for uploading tomato leaf images,
running CNN inference, and displaying disease diagnostics and prevention tips.
"""

import os
import webbrowser
import json
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# TensorFlow / Keras
import tensorflow as tf
from tensorflow import keras

# Local disease knowledge base
from disease_info import get_disease_info

# Initialize Flask app
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "tomato_disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB upload limit
TARGET_IMAGE_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.60  # 60% confidence threshold

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Global variables for model and class names
cnn_model = None
class_names = []
model_status = {
    "loaded": False,
    "error_message": None,
    "class_count": 0
}


def load_model_and_classes():
    """
    Loads the trained CNN model and class names JSON on startup.
    Fails gracefully if the model has not yet been trained.
    """
    global cnn_model, class_names, model_status

    if not os.path.exists(MODEL_PATH):
        model_status["loaded"] = False
        model_status["error_message"] = (
            f"Trained model not found at 'model/tomato_disease_model.keras'. "
            f"Please run 'python train_model.py' to train and save the model first."
        )
        print(f"[WARNING] {model_status['error_message']}")
        return

    if not os.path.exists(CLASS_NAMES_PATH):
        model_status["loaded"] = False
        model_status["error_message"] = (
            f"Class names mapping not found at 'model/class_names.json'. "
            f"Please run 'python train_model.py' to generate the class mapping."
        )
        print(f"[WARNING] {model_status['error_message']}")
        return

    try:
        # Load class names
        with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
            class_names = json.load(f)

        # Load Keras model
        print(f"[INFO] Loading CNN model from: {MODEL_PATH}")
        cnn_model = keras.models.load_model(MODEL_PATH)
        model_status["loaded"] = True
        model_status["error_message"] = None
        model_status["class_count"] = len(class_names)
        print(f"[SUCCESS] Model successfully loaded with {len(class_names)} classes!")
    except Exception as e:
        model_status["loaded"] = False
        model_status["error_message"] = f"Error loading model: {str(e)}"
        print(f"[ERROR] Failed to load model: {e}")


# Initialize model on module load
load_model_and_classes()


def allowed_file(filename: str) -> bool:
    """Checks if filename has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocesses uploaded image for CNN inference:
    1. Validates and opens image with PIL.
    2. Converts to RGB (handles RGBA / Grayscale).
    3. Resizes to 224x224.
    4. Converts to float32 numpy array.
    5. Normalizes to [0, 1] if model doesn't have an internal Rescaling layer.
    6. Expands batch dimension to (1, 224, 224, 3).
    """
    with Image.open(image_path) as img:
        img.verify()  # Ensure image file integrity

    # Re-open after verify()
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        img_resized = img_rgb.resize(TARGET_IMAGE_SIZE, Image.Resampling.BILINEAR)
        img_array = np.array(img_resized, dtype=np.float32)

    # Check if loaded model contains internal Rescaling layer
    has_rescaling = False
    if cnn_model is not None:
        has_rescaling = any(
            "rescaling" in layer.name.lower() or isinstance(layer, keras.layers.Rescaling)
            for layer in cnn_model.layers
        )

    # If the model does not have internal rescaling, scale [0, 255] to [0, 1]
    if not has_rescaling:
        img_array = img_array / 255.0

    # Expand batch dimension -> (1, 224, 224, 3)
    return np.expand_dims(img_array, axis=0)


@app.route("/")
def index():
    """Renders the main dashboard homepage."""
    # Attempt reload if model was not previously loaded
    if not model_status["loaded"]:
        load_model_and_classes()

    return render_template(
        "index.html",
        model_status=model_status,
        class_names=class_names,
        result=None
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Safely serves uploaded images for frontend display."""
    safe_name = secure_filename(filename)
    return send_from_directory(app.config["UPLOAD_FOLDER"], safe_name)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles image upload, runs CNN prediction, and returns diagnostic results.
    Supports both JSON (AJAX) and traditional HTML form responses.
    """
    is_ajax = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.is_json
        or (request.accept_mimetypes["application/json"] > request.accept_mimetypes["text/html"])
    )

    # 1. Model Availability Check
    if not model_status["loaded"] or cnn_model is None:
        load_model_and_classes()
        if not model_status["loaded"] or cnn_model is None:
            err = (
                "Model is currently unavailable. Please run 'python train_model.py' "
                "to train and save the CNN model first."
            )
            if is_ajax:
                return jsonify({"success": False, "error": err}), 503
            return render_template("index.html", model_status=model_status, error_message=err, result=None)

    # 2. File Upload Check
    if "file" not in request.files:
        err = "No file part was found in the upload request."
        if is_ajax:
            return jsonify({"success": False, "error": err}), 400
        return render_template("index.html", model_status=model_status, error_message=err, result=None)

    file = request.files["file"]

    if file.filename == "":
        err = "No image selected. Please select a tomato leaf image file."
        if is_ajax:
            return jsonify({"success": False, "error": err}), 400
        return render_template("index.html", model_status=model_status, error_message=err, result=None)

    if not allowed_file(file.filename):
        err = "Unsupported file type. Only JPG, JPEG, and PNG images are supported."
        if is_ajax:
            return jsonify({"success": False, "error": err}), 400
        return render_template("index.html", model_status=model_status, error_message=err, result=None)

    try:
        # 3. Securely Save File
        clean_ext = file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        if not unique_filename.endswith(f".{clean_ext}"):
            unique_filename = f"{unique_filename}.{clean_ext}"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(filepath)

        # 4. Preprocess and Validate Image
        try:
            input_tensor = preprocess_image(filepath)
        except Exception as img_err:
            if os.path.exists(filepath):
                os.remove(filepath)
            err = "Invalid or corrupted image file. Please upload a valid photograph."
            if is_ajax:
                return jsonify({"success": False, "error": err}), 400
            return render_template("index.html", model_status=model_status, error_message=err, result=None)

        # 5. Run CNN Inference
        predictions = cnn_model.predict(input_tensor, verbose=0)[0]
        max_idx = int(np.argmax(predictions))
        max_prob = float(predictions[max_idx])
        confidence_percent = round(max_prob * 100.0, 2)

        predicted_raw_class = class_names[max_idx] if max_idx < len(class_names) else f"Class_{max_idx}"

        # 6. Retrieve Disease Information
        info = get_disease_info(predicted_raw_class)

        # 7. Low Confidence Safeguard Check
        is_low_confidence = max_prob < CONFIDENCE_THRESHOLD
        low_confidence_message = None
        if is_low_confidence:
            low_confidence_message = (
                "The model is not sufficiently confident in this prediction. "
                "Please upload a clear, well-lit tomato leaf image."
            )

        # All class probabilities for breakdown
        breakdown = []
        for idx, prob in enumerate(predictions):
            c_name = class_names[idx] if idx < len(class_names) else f"Class_{idx}"
            c_display = c_name.replace("___", " - ").replace("_", " ").title()
            breakdown.append({
                "class_name": c_display,
                "probability": round(float(prob) * 100.0, 2)
            })
        breakdown.sort(key=lambda x: x["probability"], reverse=True)

        result_payload = {
            "disease_name": info["name"],
            "raw_class": predicted_raw_class,
            "scientific_name": info.get("scientific_name", "Solanum lycopersicum"),
            "status": info["status"],
            "severity": info["severity"],
            "badge_color": info["badge_color"],
            "confidence": confidence_percent,
            "confidence_ratio": max_prob,
            "is_low_confidence": is_low_confidence,
            "low_confidence_message": low_confidence_message,
            "image_url": f"/uploads/{unique_filename}",
            "description": info["description"],
            "symptoms": info["symptoms"],
            "prevention": info["prevention"],
            "immediate_action": info["immediate_action"],
            "top_probabilities": breakdown[:5]
        }

        if is_ajax:
            return jsonify({"success": True, "data": result_payload})

        return render_template(
            "index.html",
            model_status=model_status,
            class_names=class_names,
            result=result_payload,
            error_message=None
        )

    except Exception as e:
        # Graceful error handling without exposing stack traces
        print(f"[ERROR] Prediction failed: {e}")
        err = "An unexpected error occurred while processing the image. Please try again."
        if is_ajax:
            return jsonify({"success": False, "error": err}), 500
        return render_template("index.html", model_status=model_status, error_message=err, result=None)


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handles oversized uploads."""
    err = "File size exceeds the 10 MB limit. Please upload a smaller image."
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({"success": False, "error": err}), 413
    return render_template("index.html", model_status=model_status, error_message=err, result=None), 413


@app.errorhandler(404)
def not_found(error):
    return render_template("index.html", model_status=model_status, error_message="The requested resource was not found.", result=None), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("index.html", model_status=model_status, error_message="Internal server error occurred. Please try again.", result=None), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Starting Tomato Crop Disease Detection Web Server...")
    print("Application URL: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")
    webbrowser.open("http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
