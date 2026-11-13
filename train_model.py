"""
Tomato Crop Disease Detection - Model Training Script
Trains a Convolutional Neural Network (CNN) on tomato leaf disease images.
Automatically detects classes from the dataset folders, trains the model,
evaluates on test data (if available), and exports the trained model and class mappings.
"""

import os
import sys
import json
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt

# Keras / TensorFlow imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks

# Metrics
from sklearn.metrics import classification_report, confusion_matrix

# Constants
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
DEFAULT_EPOCHS = 20
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "tomato_disease_model.keras")
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, "class_names.json")

DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "validation")
TEST_DIR = os.path.join(DATASET_DIR, "test")


def check_dataset_directories(train_dir: str):
    """
    Validates that the training directory exists and contains class subfolders with images.
    If missing or empty, prints a friendly guide and exits cleanly.
    """
    if not os.path.exists(train_dir):
        print("\n" + "=" * 70)
        print("[ERROR] Training dataset directory not found!")
        print(f"Expected path: {os.path.abspath(train_dir)}")
        print("=" * 70)
        print("Please organize your dataset as follows:")
        print("  dataset/")
        print("  ├── train/")
        print("  │   ├── Tomato_Bacterial_Spot/")
        print("  │   ├── Tomato_Early_Blight/")
        print("  │   ├── Tomato_Late_Blight/")
        print("  │   ├── Tomato_Leaf_Mold/")
        print("  │   ├── Tomato_Septoria_Leaf_Spot/")
        print("  │   ├── Tomato_Spider_Mites/")
        print("  │   ├── Tomato_Target_Spot/")
        print("  │   ├── Tomato_Mosaic_Virus/")
        print("  │   ├── Tomato_Yellow_Leaf_Curl_Virus/")
        print("  │   └── Tomato_Healthy/")
        print("  ├── validation/  (optional, will split train if omitted)")
        print("  └── test/        (optional, for final evaluation)")
        print("\nTip: You can run 'python setup_sample_data.py' to generate quick sample")
        print("data for testing, or download the PlantVillage Tomato dataset.")
        print("=" * 70 + "\n")
        return None

    # Detect class folders
    subdirs = [
        d for d in os.listdir(train_dir)
        if os.path.isdir(os.path.join(train_dir, d)) and not d.startswith(".")
    ]

    if not subdirs:
        print("\n" + "=" * 70)
        print(f"[ERROR] No class folders found inside '{os.path.abspath(train_dir)}'.")
        print("Each subfolder inside 'dataset/train/' must represent one disease class")
        print("and contain corresponding leaf images (.jpg, .jpeg, .png).")
        print("=" * 70 + "\n")
        return None

    # Verify at least one image exists
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    total_images = 0
    empty_classes = []
    for cls in subdirs:
        cls_path = os.path.join(train_dir, cls)
        count = sum(1 for f in os.listdir(cls_path) if f.lower().endswith(valid_extensions))
        if count == 0:
            empty_classes.append(cls)
        total_images += count

    if empty_classes:
        print(f"[WARNING] The following class folders contain no images: {empty_classes}")

    if total_images == 0:
        print("\n" + "=" * 70)
        print(f"[ERROR] Found {len(subdirs)} class folders, but NO valid images (.jpg, .jpeg, .png) were found.")
        print(f"Please place leaf images inside: {os.path.abspath(train_dir)}")
        print("=" * 70 + "\n")
        return None

    subdirs.sort()
    return subdirs


def build_cnn_model(input_shape=(224, 224, 3), num_classes=10):
    """
    Builds and compiles the Convolutional Neural Network architecture:
    - Input: 224x224x3
    - Data Augmentation layers (rotation, zoom, flip, shift)
    - Rescaling (1./255)
    - 3 Conv2D + ReLU + MaxPooling2D blocks
    - Flatten / GlobalAveragePooling2D
    - Dense layer + Dropout
    - Output Dense with Softmax
    """
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
            layers.RandomTranslation(0.1, 0.1),
        ],
        name="data_augmentation"
    )

    inputs = layers.Input(shape=input_shape, name="input_image")
    x = data_augmentation(inputs)
    x = layers.Rescaling(1.0 / 255.0, name="rescaling")(x)

    # Block 1
    x = layers.Conv2D(32, (3, 3), padding="same", activation="relu", name="conv1")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name="pool1")(x)

    # Block 2
    x = layers.Conv2D(64, (3, 3), padding="same", activation="relu", name="conv2")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name="pool2")(x)

    # Block 3
    x = layers.Conv2D(128, (3, 3), padding="same", activation="relu", name="conv3")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name="pool3")(x)

    # Classification Head
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.Dense(128, activation="relu", name="dense1")(x)
    x = layers.Dropout(0.5, name="dropout1")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="output_probabilities")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="tomato_disease_cnn")

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def plot_training_history(history, save_path: str):
    """Plots and saves training and validation accuracy and loss curves."""
    acc = history.history.get("accuracy", [])
    val_acc = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs_range = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))

    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy", color="#2e7d32", linewidth=2)
    if val_acc:
        plt.plot(epochs_range, val_acc, label="Validation Accuracy", color="#1565c0", linewidth=2)
    plt.title("Model Accuracy", fontsize=14, fontweight="bold")
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Accuracy", fontsize=12)
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.6)

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss", color="#c62828", linewidth=2)
    if val_loss:
        plt.plot(epochs_range, val_loss, label="Validation Loss", color="#ef6c00", linewidth=2)
    plt.title("Model Loss", fontsize=14, fontweight="bold")
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Loss", fontsize=12)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"[INFO] Training curves saved to: {save_path}")


def evaluate_on_test_data(model, test_dir: str, class_names: list):
    """
    Evaluates model on test dataset if available, prints classification report,
    and plots confusion matrix.
    """
    if not os.path.exists(test_dir):
        print("[INFO] No test directory found at 'dataset/test'. Skipping test evaluation.")
        return

    test_subdirs = [
        d for d in os.listdir(test_dir)
        if os.path.isdir(os.path.join(test_dir, d))
    ]
    if not test_subdirs:
        print("[INFO] Test directory contains no class subfolders. Skipping test evaluation.")
        return

    print("\n" + "=" * 60)
    print("Evaluating Model on Test Dataset...")
    print("=" * 60)

    test_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        labels="inferred",
        label_mode="categorical",
        class_names=class_names,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    y_true_list = []
    y_pred_list = []

    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true_list.extend(np.argmax(labels.numpy(), axis=1))
        y_pred_list.extend(np.argmax(preds, axis=1))

    y_true = np.array(y_true_list)
    y_pred = np.array(y_pred_list)

    print("\n--- Classification Report ---")
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    cm_path = os.path.join(MODEL_DIR, "confusion_matrix.png")

    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Greens)
    plt.title("Confusion Matrix - Tomato Leaf Disease Detection", fontsize=14, fontweight="bold")
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45, ha="right", fontsize=9)
    plt.yticks(tick_marks, class_names, fontsize=9)

    thresh = cm.max() / 2.0 if cm.max() > 0 else 1
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j, i, format(cm[i, j], "d"),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black"
            )

    plt.ylabel("True Disease Class", fontsize=11)
    plt.xlabel("Predicted Disease Class", fontsize=11)
    plt.tight_layout()
    plt.savefig(cm_path, dpi=200)
    plt.close()
    print(f"[INFO] Confusion matrix plot saved to: {cm_path}")


def train(epochs: int = DEFAULT_EPOCHS, batch_size: int = BATCH_SIZE):
    os.makedirs(MODEL_DIR, exist_ok=True)

    class_names = check_dataset_directories(TRAIN_DIR)
    if class_names is None:
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Tomato Crop Disease Detection - CNN Training Pipeline")
    print("=" * 60)
    print(f"Detected {len(class_names)} Disease Classes:")
    for idx, name in enumerate(class_names):
        print(f"  [{idx}] {name}")
    print("=" * 60)

    # Save class names JSON
    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=4)
    print(f"[INFO] Saved class names mapping to: {CLASS_NAMES_PATH}")

    # Check if validation directory exists with subfolders
    has_val_dir = os.path.exists(VAL_DIR) and any(
        os.path.isdir(os.path.join(VAL_DIR, d)) for d in os.listdir(VAL_DIR)
    )

    if has_val_dir:
        print("[INFO] Loading dedicated training and validation splits from folders...")
        train_ds = tf.keras.utils.image_dataset_from_directory(
            TRAIN_DIR,
            labels="inferred",
            label_mode="categorical",
            class_names=class_names,
            image_size=IMAGE_SIZE,
            batch_size=batch_size,
            shuffle=True,
            seed=42
        )
        val_ds = tf.keras.utils.image_dataset_from_directory(
            VAL_DIR,
            labels="inferred",
            label_mode="categorical",
            class_names=class_names,
            image_size=IMAGE_SIZE,
            batch_size=batch_size,
            shuffle=False
        )
    else:
        print("[INFO] No separate validation directory found. Splitting training data (80% train, 20% val)...")
        train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
            TRAIN_DIR,
            labels="inferred",
            label_mode="categorical",
            class_names=class_names,
            image_size=IMAGE_SIZE,
            batch_size=batch_size,
            validation_split=0.2,
            subset="both",
            shuffle=True,
            seed=42
        )

    # Prefetch datasets for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # Build CNN
    print("\n[INFO] Constructing CNN model architecture...")
    model = build_cnn_model(input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), num_classes=len(class_names))
    model.summary()

    # Callbacks
    training_callbacks = [
        callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]

    print(f"\n[INFO] Starting training for {epochs} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=training_callbacks
    )

    # Save final model if not already saved by checkpoint
    if not os.path.exists(MODEL_PATH):
        model.save(MODEL_PATH)
    print(f"\n[SUCCESS] Model successfully saved to: {MODEL_PATH}")

    # Plot history
    history_plot_path = os.path.join(MODEL_DIR, "training_history.png")
    plot_training_history(history, history_plot_path)

    # Evaluate on test data
    evaluate_on_test_data(model, TEST_DIR, class_names)

    print("\n" + "=" * 60)
    print("Training Pipeline Completed Successfully!")
    print(f"Model:       {MODEL_PATH}")
    print(f"Class Names: {CLASS_NAMES_PATH}")
    print("You can now start the web application with: python app.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CNN for Tomato Leaf Disease Detection")
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS, help="Number of training epochs (default: 20)")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size (default: 32)")
    args = parser.parse_args()

    train(epochs=args.epochs, batch_size=args.batch_size)
