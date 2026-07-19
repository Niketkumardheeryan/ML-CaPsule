// Get DOM elements
const img = document.getElementById("img");
const inputFile = document.getElementById("input");
const upload = document.getElementById("upload");
const prediction = document.getElementById("prediction");

// Validate that all required elements exist
if (!img || !inputFile || !upload || !prediction) {
  console.error("Required DOM elements not found");
}

/**
 * Handles image file upload and classification
 */
inputFile.addEventListener("change", handleFileUpload);

/**
 * Processes the uploaded file and runs image classification
 * @param {Event} event - The change event from the file input
 */
async function handleFileUpload(event) {
  try {
    const file = event.target.files[0];

    // Validate file exists
    if (!file) {
      console.warn("No file selected");
      return;
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      showError("Please upload a valid image file (JPG, PNG, etc.)");
      return;
    }

    // Validate file size (e.g., max 5MB)
    const maxFileSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxFileSize) {
      showError("File size exceeds 5MB limit");
      return;
    }

    // Display the uploaded image
    displayImage(file);

    // Run image classification
    await classifyImage();
  } catch (error) {
    showError("An error occurred while processing the image");
    console.error("Error in handleFileUpload:", error);
  }
}

/**
 * Displays the uploaded image
 * @param {File} file - The image file to display
 */
function displayImage(file) {
  try {
    const objectUrl = window.URL.createObjectURL(file);

    img.onload = () => {
      // Clean up the object URL after image loads
      window.URL.revokeObjectURL(objectUrl);
    };

    img.src = objectUrl;
    img.alt = "Uploaded image for classification";
    img.style.border = "1px solid #ccc";

    updateStatus(upload, "Image Uploaded Successfully!", "success");
  } catch (error) {
    showError("Failed to display image");
    console.error("Error in displayImage:", error);
  }
}

/**
 * Classifies the image using MobileNet model
 */
async function classifyImage() {
  try {
    updateStatus(prediction, "Prediction Loading...", "loading");

    // Load the MobileNet model
    console.log("Loading MobileNet model...");
    const model = await mobilenet.load();

    // Classify the image
    console.log("Classifying image...");
    const predictions = await model.classify(img);

    // Display prediction results
    if (predictions && predictions.length > 0) {
      const topPrediction = predictions[0];
      const confidence = (topPrediction.probability * 100).toFixed(2);
      const resultText = `This image is predicted to be a <strong>${sanitizeHTML(topPrediction.className)}</strong> with <strong>${confidence}%</strong> confidence`;

      updateStatus(prediction, resultText, "success");
      console.log("Predictions:", predictions);
    } else {
      showError("No predictions returned");
    }
  } catch (error) {
    showError("Failed to classify image. Please try again.");
    console.error("Error in classifyImage:", error);
  }
}

/**
 * Updates status message with appropriate styling
 * @param {HTMLElement} element - The element to update
 * @param {string} message - The message to display
 * @param {string} status - Status type: 'success', 'error', or 'loading'
 */
function updateStatus(element, message, status = "info") {
  element.innerHTML = message;
  element.className = `status-${status}`;
}

/**
 * Displays an error message to the user
 * @param {string} message - The error message
 */
function showError(message) {
  updateStatus(prediction, message, "error");
  console.error("User-facing error:", message);
}

/**
 * Sanitizes HTML to prevent XSS attacks
 * @param {string} text - The text to sanitize
 * @returns {string} The sanitized text
 */
function sanitizeHTML(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}