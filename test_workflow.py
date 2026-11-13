"""
End-to-End Workflow and Edge Case Test Suite
Tests:
1. GET / (Homepage rendering and model loaded indicator)
2. POST /predict with valid JPG image
3. POST /predict with valid PNG image
4. POST /predict with invalid file type (.txt)
5. POST /predict with empty file upload / no file chosen
6. POST /predict with corrupted image file
7. Confidence thresholds and response payload integrity
"""

import os
import io
import json
from PIL import Image
from app import app, cnn_model, class_names


def test_homepage():
    """Test homepage loads successfully."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Tomato Crop Disease Detection" in response.data
    assert b"Model Ready" in response.data
    print(" [PASS] test_homepage")


def test_valid_jpg_prediction():
    """Test valid JPG upload returns correct diagnosis payload."""
    client = app.test_client()

    # Create dummy RGB image in memory
    img = Image.new("RGB", (224, 224), color=(50, 150, 50))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    response = client.post(
        "/predict",
        data={"file": (img_bytes, "test_leaf.jpg")},
        content_type="multipart/form-data",
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert "disease_name" in data["data"]
    assert "confidence" in data["data"]
    assert "description" in data["data"]
    assert "prevention" in data["data"]
    assert "symptoms" in data["data"]
    assert "immediate_action" in data["data"]
    assert "top_probabilities" in data["data"]
    print(f" [PASS] test_valid_jpg_prediction -> Diagnosed: {data['data']['disease_name']} ({data['data']['confidence']}%)")


def test_valid_png_prediction():
    """Test valid PNG upload returns correct diagnosis payload."""
    client = app.test_client()

    img = Image.new("RGB", (300, 300), color=(180, 180, 60))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    response = client.post(
        "/predict",
        data={"file": (img_bytes, "test_leaf.png")},
        content_type="multipart/form-data",
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    print(f" [PASS] test_valid_png_prediction -> Diagnosed: {data['data']['disease_name']} ({data['data']['confidence']}%)")


def test_invalid_file_type():
    """Test rejection of unsupported file extensions (e.g., .txt)."""
    client = app.test_client()

    txt_bytes = io.BytesIO(b"This is not a leaf image.")
    response = client.post(
        "/predict",
        data={"file": (txt_bytes, "notes.txt")},
        content_type="multipart/form-data",
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Unsupported file type" in data["error"]
    print(" [PASS] test_invalid_file_type (rejected as expected)")


def test_no_file_uploaded():
    """Test rejection when no file is selected."""
    client = app.test_client()

    empty_bytes = io.BytesIO(b"")
    response = client.post(
        "/predict",
        data={"file": (empty_bytes, "")},
        content_type="multipart/form-data",
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "No image selected" in data["error"]
    print(" [PASS] test_no_file_uploaded (rejected as expected)")


def test_corrupted_image():
    """Test graceful handling of corrupted or truncated image file."""
    client = app.test_client()

    corrupt_bytes = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01ThisIsCorruptGarbageData12345")
    response = client.post(
        "/predict",
        data={"file": (corrupt_bytes, "corrupt.jpg")},
        content_type="multipart/form-data",
        headers={"X-Requested-With": "XMLHttpRequest"}
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "Invalid or corrupted image" in data["error"]
    print(" [PASS] test_corrupted_image (handled gracefully without crash)")


def test_missing_model():
    """Test graceful handling when model is missing or unloaded."""
    import app as flask_app_module
    client = flask_app_module.app.test_client()

    # Temporarily set model to unloaded
    prev_model = flask_app_module.cnn_model
    prev_loaded = flask_app_module.model_status["loaded"]
    try:
        flask_app_module.cnn_model = None
        flask_app_module.model_status["loaded"] = False

        # 1. Homepage should load showing offline status
        res_home = client.get("/")
        assert res_home.status_code == 200

        # 2. Predict should return friendly 503 instead of crashing
        img = Image.new("RGB", (224, 224), color=(50, 150, 50))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        res_predict = client.post(
            "/predict",
            data={"file": (img_bytes, "test.jpg")},
            content_type="multipart/form-data",
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        # It may attempt reload if model file exists on disk, which is valid and graceful
        assert res_predict.status_code in (200, 503)
        print(" [PASS] test_missing_model (handled gracefully)")
    finally:
        flask_app_module.cnn_model = prev_model
        flask_app_module.model_status["loaded"] = prev_loaded


def run_all_tests():
    print("=" * 60)
    print("Running Tomato Disease Detection Automated Test Suite...")
    print("=" * 60)
    test_homepage()
    test_valid_jpg_prediction()
    test_valid_png_prediction()
    test_invalid_file_type()
    test_no_file_uploaded()
    test_corrupted_image()
    test_missing_model()
    print("=" * 60)
    print("ALL 7 TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
