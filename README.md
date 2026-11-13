# Tomato Crop Disease Detection Using CNN Algorithm

An end-to-end Deep Learning web application designed to automatically detect and classify foliar diseases in tomato crops from uploaded leaf photographs using a Convolutional Neural Network (CNN) built with TensorFlow/Keras and deployed on a Flask backend.

---

## 1. Project Overview

Tomato (*Solanum lycopersicum*) is one of the most widely cultivated vegetable crops globally. However, tomato plants are highly susceptible to foliar pathogens including bacteria, fungi, viruses, and spider mites. Manual scouting is labor-intensive, error-prone, and often too late to prevent extensive crop loss.

This system provides a practical AI tool for farmers, agricultural students, and researchers:
- **Instant Diagnosis:** Upload an image of a suspected tomato leaf.
- **Deep Feature Extraction:** A custom 3-block CNN inspects textures, spots, and chlorosis patterns.
- **Dynamic Class Mapping:** Automatically adapts to the class folders in the dataset.
- **Confidence Safeguards:** Warns users when predictions fall below 60% confidence.
- **Eco-friendly Care Advice:** Provides agricultural symptoms, prevention methods, and immediate actions without hazardous chemical dosages.

---

## 2. Key Features

- **10 Target Leaf Classes:** Covers healthy leaves and 9 widespread fungal, bacterial, and viral infections.
- **Dynamic Dataset Discovery:** Automatically extracts classes alphabetically from the `dataset/train/` folder rather than hardcoding class indices.
- **Robust Preprocessing & Augmentation:** Standardized $224 \times 224 \times 3$ image pipeline with horizontal flipping, rotation, zoom, and normalization.
- **Confidence Scoring & Low-Confidence Warning:** Computes softmax probability percentages and warns the user if confidence is below 60%.
- **Responsive Modern UI:** Emerald botanical design system with drag-and-drop dropzone, live client-side image preview, progress spinners, and animated probability breakdown bars.
- **Resilient Error Handling:** Validates file formats (`.jpg`, `.jpeg`, `.png`), limits upload size to 10 MB, verifies PIL image integrity, and avoids leaking raw stack traces.
- **Complete Metrics & Visualizations:** Training script exports training/validation accuracy-loss curves and generates a confusion matrix on test sets.

---

## 3. Targeted Disease Classes

The model is configured to recognize the following 10 tomato leaf conditions:

| # | Class Name | Pathogen Type | Scientific Name |
|---|---|---|---|
| 1 | **Tomato Healthy** | None | *Solanum lycopersicum* |
| 2 | **Tomato Bacterial Spot** | Bacteria | *Xanthomonas perforans / vesicatoria* |
| 3 | **Tomato Early Blight** | Fungus | *Alternaria solani* |
| 4 | **Tomato Late Blight** | Oomycete | *Phytophthora infestans* |
| 5 | **Tomato Leaf Mold** | Fungus | *Passalora fulva* |
| 6 | **Tomato Septoria Leaf Spot** | Fungus | *Septoria lycopersici* |
| 7 | **Tomato Spider Mites** | Arachnid Pest | *Tetranychus urticae* |
| 8 | **Tomato Target Spot** | Fungus | *Corynespora cassiicola* |
| 9 | **Tomato Mosaic Virus** | Virus | *Tomato mosaic tobamovirus (ToMV)* |
| 10 | **Tomato Yellow Leaf Curl Virus** | Virus | *Tomato yellow leaf curl begomovirus (TYLCV)* |

---

## 4. Technologies Used

### Frontend
- **HTML5:** Semantic architecture, accessible forms, and drag-and-drop container.
- **CSS3:** Custom responsive layout, botanical color scheme, glassmorphic badges, and micro-animations. No external CSS frameworks required.
- **JavaScript (ES6+):** Asynchronous `fetch` API, live image preview via `FileReader`, client-side file size and MIME-type validation.

### Backend & Machine Learning
- **Python (3.11 recommended):** Core backend runtime.
- **Flask (3.x):** Lightweight WSGI web framework.
- **TensorFlow / Keras (2.15+):** Deep Learning CNN model architecture, data augmentation, and inference.
- **NumPy:** Multidimensional tensor manipulation.
- **Pillow (PIL):** Safe image reading and integrity verification.
- **scikit-learn:** Classification report and confusion matrix evaluation.
- **Matplotlib:** Visualization of training curves and confusion matrix.
- **Werkzeug:** Filename sanitization and secure file handling.

---

## 5. System Architecture

```
[ User Uploads Leaf Image ]
            │
            ▼
[ Flask Upload Validation ] ──► (Invalid format/size) ──► [ Friendly Error UI ]
            │ (Valid JPG/PNG, <= 10MB)
            ▼
[ Image Preprocessing (224x224x3, RGB, Rescaled) ]
            │
            ▼
[ CNN Model (Conv2D -> BatchNorm -> MaxPool -> GlobalAvgPool -> Dense -> Softmax) ]
            │
            ▼
[ Softmax Probability Distribution ]
            │
      ┌─────┴─────────────────────────┐
      ▼                               ▼
[ Top Confidence >= 60% ]      [ Top Confidence < 60% ]
      │                               │
      ▼                               ▼
[ High-Confidence Diagnosis ]   [ Low-Confidence Alert Banner ]
      │                               │
      └──────────────┬────────────────┘
                     ▼
[ JSON / HTML Response: Disease Info, Symptoms, Cultural Care & Meter ]
```

---

## 6. Directory Structure

```
tomato-disease-detection/
│
├── app.py                      # Flask web server & inference controller
├── train_model.py              # CNN model training and evaluation script
├── disease_info.py             # Knowledge base with symptoms & care tips
├── setup_sample_data.py        # Helper to generate test leaf samples immediately
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
│
├── dataset/                    # Image dataset directory
│   ├── train/                  # Training images organized by class folder
│   ├── validation/             # Validation images organized by class folder
│   └── test/                   # Test evaluation images organized by class folder
│
├── model/                      # Saved models and exported metrics
│   ├── tomato_disease_model.keras   # Trained Keras model
│   ├── class_names.json             # Dynamic index-to-class mapping
│   ├── training_history.png         # Accuracy and loss graphs
│   └── confusion_matrix.png         # Confusion matrix plot
│
├── templates/
│   └── index.html              # Modern responsive HTML template
│
├── static/
│   ├── style.css               # Botanical CSS design system
│   └── script.js               # Client validation, preview & AJAX handler
│
└── uploads/                    # Temporary storage for uploaded leaves
```

---

## 7. Installation & Setup (Windows)

### Step 1: Open PowerShell / Terminal
Navigate to the project directory:
```powershell
cd "c:\Users\anilc\OneDrive\Desktop\ibm project\tomato-disease-detection"
```

### Step 2: Create a Python 3.11 Virtual Environment
*Note: Python 3.11 is recommended for TensorFlow compatibility on Windows.*
```powershell
py -3.11 -m venv venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 4: Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 8. Dataset Placement Instructions

The system works with any standard tomato leaf image dataset organized in folder-per-class format.

### Recommended Full Dataset:
Download the **PlantVillage Tomato Leaf Disease Dataset** from Kaggle:
- Kaggle Dataset: [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)

### Dataset Folder Layout:
Organize your downloaded images into `dataset/train/`, `dataset/validation/`, and `dataset/test/` like this:
```
dataset/
├── train/
│   ├── Tomato_Bacterial_Spot/
│   ├── Tomato_Early_Blight/
│   ├── Tomato_Late_Blight/
│   ├── Tomato_Leaf_Mold/
│   ├── Tomato_Septoria_Leaf_Spot/
│   ├── Tomato_Spider_Mites/
│   ├── Tomato_Target_Spot/
│   ├── Tomato_Mosaic_Virus/
│   ├── Tomato_Yellow_Leaf_Curl_Virus/
│   └── Tomato_Healthy/
├── validation/
│   └── ... (same subfolders as train)
└── test/
    └── ... (same subfolders as train)
```

### Quick Starter Sample (Instant Verification):
If you want to verify the entire system before downloading gigabytes of images, simply run:
```powershell
python setup_sample_data.py
```
This generates synthetic starter leaf patterns across all 10 classes in `dataset/train/`, `dataset/validation/`, and `dataset/test/`.

---

## 9. Training the CNN Model

Run the training pipeline with:
```powershell
python train_model.py
```

### Optional Arguments:
```powershell
# Custom epochs and batch size
python train_model.py --epochs 25 --batch-size 32
```

### What Happens During Training:
1. Automatically scans `dataset/train/` and indexes all class folders alphabetically.
2. Saves class mappings to `model/class_names.json`.
3. Compiles the CNN architecture with Adam optimizer and categorical crossentropy.
4. Uses `EarlyStopping`, `ModelCheckpoint`, and `ReduceLROnPlateau` callbacks.
5. Saves the best model weights to `model/tomato_disease_model.keras`.
6. Generates `model/training_history.png` (accuracy/loss plots).
7. Evaluates against `dataset/test/` (if present) and generates `model/confusion_matrix.png`.

---

## 10. Running the Web Application

Ensure your virtual environment is active, then launch the Flask server:
```powershell
python app.py
```

### Expected Output:
```
============================================================
Starting Tomato Crop Disease Detection Web Server...
Application URL: http://127.0.0.1:5000
Press CTRL+C to stop the server.
============================================================
 * Running on http://127.0.0.1:5000
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 11. Prediction Workflow

1. **Select an Image:** Click the upload dropzone or drag and drop a leaf photo (`.jpg`, `.jpeg`, `.png`).
2. **Instant Preview:** The selected leaf appears immediately in the preview box with file size information.
3. **Run Prediction:** Click **"Predict Disease"**.
4. **CNN Inference:**
   - The image is safely uploaded to `uploads/`.
   - The backend checks image integrity using Pillow (`PIL`).
   - The image is converted to RGB, resized to $224 \times 224$, and normalized to $[0, 1]$.
   - The CNN model generates probabilities across all classes.
5. **View Results:**
   - **Disease Name & Pathogen:** Full scientific diagnosis.
   - **Confidence Percentage:** E.g., `94.52%` with visual meter.
   - **Clinical Symptoms:** Detailed bullet points of symptoms.
   - **Agricultural Prevention:** Organic prevention, pruning, and watering suggestions.
   - **Probability Breakdown:** Top 5 class probabilities.
   - **Low Confidence Alert:** Displayed if confidence is $< 60\%$.

---

## 12. Troubleshooting & Common Errors

| Issue | Cause | Solution |
|---|---|---|
| `No module named 'tensorflow'` | Virtual environment not active or packages not installed | Run `.\venv\Scripts\activate` and `pip install -r requirements.txt`. |
| `Training dataset directory not found!` | `dataset/train/` is missing or empty | Run `python setup_sample_data.py` or place your dataset folders in `dataset/train/`. |
| `Model is currently unavailable` | `tomato_disease_model.keras` has not been generated yet | Run `python train_model.py` to train and save the model. |
| `Unsupported file type` | Uploaded file is not JPG, JPEG, or PNG | Ensure you only upload standard image files. |
| `File size exceeds 10 MB limit` | The uploaded photograph is too large | Compress or resize the image to under 10 MB. |
| `Low confidence warning` | Image is blurry, not a tomato leaf, or poorly lit | Upload a clear, close-up photograph of a single tomato leaf under good lighting. |

---

## 13. Future Enhancements

- Integration with mobile camera via HTML5 WebRTC.
- Multilingual support for regional agricultural dialects.
- Automated weather API integration to assess localized blight risk.
- Integration of lightweight Edge TPU / TensorFlow Lite models for offline field deployment.
