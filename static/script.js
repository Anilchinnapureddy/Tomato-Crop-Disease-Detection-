/**
 * Tomato Crop Disease Detection - Interactive Frontend Controller
 * Handles drag-and-drop, image preview, client-side validation,
 * and AJAX prediction submission.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("fileInput");
    const dropzonePrompt = document.getElementById("dropzonePrompt");
    const previewContainer = document.getElementById("previewContainer");
    const imagePreview = document.getElementById("imagePreview");
    const removeImageBtn = document.getElementById("removeImageBtn");
    const previewFileInfo = document.getElementById("previewFileInfo");
    const clientError = document.getElementById("clientError");

    const predictionForm = document.getElementById("predictionForm");
    const predictBtn = document.getElementById("predictBtn");
    const btnSpinner = document.getElementById("btnSpinner");
    const resetBtn = document.getElementById("resetBtn");

    // Result Elements
    const emptyState = document.getElementById("emptyState");
    const loadingState = document.getElementById("loadingState");
    const predictionResults = document.getElementById("predictionResults");

    const lowConfidenceAlert = document.getElementById("lowConfidenceAlert");
    const lowConfidenceText = document.getElementById("lowConfidenceText");
    const resStatusBadge = document.getElementById("resStatusBadge");
    const resDiseaseName = document.getElementById("resDiseaseName");
    const resScientificName = document.getElementById("resScientificName");
    const resConfidenceVal = document.getElementById("resConfidenceVal");
    const resConfidenceText = document.getElementById("resConfidenceText");
    const resMeterFill = document.getElementById("resMeterFill");
    const resImage = document.getElementById("resImage");
    const resDescription = document.getElementById("resDescription");
    const resSeverity = document.getElementById("resSeverity");
    const resSymptomsList = document.getElementById("resSymptomsList");
    const resPreventionList = document.getElementById("resPreventionList");
    const resImmediateAction = document.getElementById("resImmediateAction");
    const breakdownList = document.getElementById("breakdownList");

    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB
    const VALID_EXTENSIONS = ["jpg", "jpeg", "png"];

    // -------------------------------------------------------------------------
    // Helper: Show & Hide Client Errors
    // -------------------------------------------------------------------------
    function showError(message) {
        clientError.textContent = message;
        clientError.classList.remove("hidden");
    }

    function clearError() {
        clientError.textContent = "";
        clientError.classList.add("hidden");
    }

    // -------------------------------------------------------------------------
    // File Validation & Preview Handling
    // -------------------------------------------------------------------------
    function handleSelectedFile(file) {
        clearError();

        if (!file) {
            resetImagePreview();
            return;
        }

        // Extension check
        const ext = file.name.split(".").pop().toLowerCase();
        if (!VALID_EXTENSIONS.includes(ext)) {
            showError("Unsupported file type. Please upload a JPG, JPEG, or PNG photograph.");
            resetImagePreview();
            return;
        }

        // Size check
        if (file.size > MAX_FILE_SIZE) {
            showError("File size exceeds 10 MB limit. Please select a smaller photo.");
            resetImagePreview();
            return;
        }

        // Preview with FileReader
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewFileInfo.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
            dropzonePrompt.classList.add("hidden");
            previewContainer.classList.remove("hidden");
        };
        reader.onerror = () => {
            showError("Unable to read the selected file. It may be corrupted.");
            resetImagePreview();
        };
        reader.readAsDataURL(file);
    }

    function resetImagePreview() {
        fileInput.value = "";
        imagePreview.src = "";
        previewFileInfo.textContent = "";
        previewContainer.classList.add("hidden");
        dropzonePrompt.classList.remove("hidden");
        clearError();
    }

    // -------------------------------------------------------------------------
    // Event Listeners for File Selection & Drag-and-Drop
    // -------------------------------------------------------------------------
    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    removeImageBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        resetImagePreview();
    });

    // Drag-and-Drop
    ["dragenter", "dragover"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove("dragover");
        });
    });

    dropzone.addEventListener("drop", (e) => {
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleSelectedFile(e.dataTransfer.files[0]);
        }
    });

    // Reset button
    resetBtn.addEventListener("click", () => {
        resetImagePreview();
        if (predictionResults) predictionResults.classList.add("hidden");
        if (emptyState) emptyState.classList.remove("hidden");
        if (loadingState) loadingState.classList.add("hidden");
    });

    // -------------------------------------------------------------------------
    // AJAX Prediction Submission
    // -------------------------------------------------------------------------
    predictionForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        clearError();

        if (!fileInput.files || fileInput.files.length === 0) {
            showError("Please select or drag-and-drop a tomato leaf image first.");
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("file", file);

        // UI Loading State
        predictBtn.disabled = true;
        btnSpinner.classList.remove("hidden");
        if (emptyState) emptyState.classList.add("hidden");
        if (predictionResults) predictionResults.classList.add("hidden");
        if (loadingState) loadingState.classList.remove("hidden");

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                const errMsg = result.error || "Prediction request failed. Please check the server logs.";
                showError(errMsg);
                if (loadingState) loadingState.classList.add("hidden");
                if (emptyState) emptyState.classList.remove("hidden");
                return;
            }

            // Populate Results UI
            displayPredictionResults(result.data);

        } catch (err) {
            console.error("AJAX error:", err);
            showError("Network or server connection error. Please make sure Flask is running.");
            if (loadingState) loadingState.classList.add("hidden");
            if (emptyState) emptyState.classList.remove("hidden");
        } finally {
            predictBtn.disabled = false;
            btnSpinner.classList.add("hidden");
        }
    });

    // -------------------------------------------------------------------------
    // Render Results in DOM
    // -------------------------------------------------------------------------
    function displayPredictionResults(data) {
        if (loadingState) loadingState.classList.add("hidden");
        if (emptyState) emptyState.classList.add("hidden");

        // Status Badge & Colors
        resStatusBadge.textContent = data.status;
        resStatusBadge.className = `badge-status badge-${data.badge_color || 'danger'}`;

        // Disease Name & Details
        resDiseaseName.textContent = data.disease_name;
        resScientificName.innerHTML = `Pathogen: <em>${data.scientific_name}</em>`;
        resConfidenceVal.textContent = `${data.confidence}%`;
        resConfidenceText.textContent = `${data.confidence}%`;
        resMeterFill.style.width = `${Math.min(data.confidence, 100)}%`;

        // Low Confidence Warning
        if (data.is_low_confidence) {
            lowConfidenceAlert.classList.remove("hidden");
            lowConfidenceText.textContent = data.low_confidence_message;
        } else {
            lowConfidenceAlert.classList.add("hidden");
        }

        // Image & Clinical Overview
        resImage.src = data.image_url;
        resDescription.textContent = data.description;
        resSeverity.textContent = data.severity;

        // Symptoms List
        resSymptomsList.innerHTML = "";
        if (data.symptoms && Array.isArray(data.symptoms)) {
            data.symptoms.forEach((s) => {
                const li = document.createElement("li");
                li.textContent = s;
                resSymptomsList.appendChild(li);
            });
        }

        // Prevention List
        resPreventionList.innerHTML = "";
        if (data.prevention && Array.isArray(data.prevention)) {
            data.prevention.forEach((p) => {
                const li = document.createElement("li");
                li.textContent = p;
                resPreventionList.appendChild(li);
            });
        }

        // Immediate Action
        resImmediateAction.textContent = data.immediate_action;

        // Class Probability Breakdown
        breakdownList.innerHTML = "";
        if (data.top_probabilities && Array.isArray(data.top_probabilities)) {
            data.top_probabilities.forEach((item) => {
                const row = document.createElement("div");
                row.className = "breakdown-row";
                row.innerHTML = `
                    <span class="breakdown-name" title="${item.class_name}">${item.class_name}</span>
                    <div class="breakdown-bar-track">
                        <div class="breakdown-bar-fill" style="width: ${Math.min(item.probability, 100)}%;"></div>
                    </div>
                    <span class="breakdown-num">${item.probability}%</span>
                `;
                breakdownList.appendChild(row);
            });
        }

        // Reveal results container
        predictionResults.classList.remove("hidden");

        // Smooth scroll to result on mobile
        if (window.innerWidth < 960) {
            predictionResults.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }
});
