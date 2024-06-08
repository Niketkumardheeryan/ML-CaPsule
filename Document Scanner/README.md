# Document Scanner using OpenCV

## Introduction
Document scanning is a common task in offices and personal use. By automating document scanning with computer vision techniques, we can efficiently digitize documents.

## Goal
The goal of this project is to develop a document scanner that can detect documents in images and extract them for further processing or storage.

## Libraries used
- OpenCV
- NumPy
- Matplotlib

## Steps

### 1. Loading and importing all the libraries
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

### 2. Loading the image
```python
image = cv2.imread("document.jpg")
```

### 3. Preprocessing
```python
# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edged = cv2.Canny(blurred, 30, 150)
```

### 4. Finding contours
```python
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

### 5. Finding the document contour
```python
doc_contour = None
if len(contours) > 0:
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        # Approximating the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # If the contour has four points, we assume it is the document contour
        if len(approx) == 4:
            doc_contour = approx
            break
```

### 6. Perspective transformation
```python
# Perspective transformation function
# (code for the function is included in the template provided above)

# Apply the perspective transform to get the scanned document
if doc_contour is not None:
    scanned_document = four_point_transform(image, doc_contour)
```

### 7. Displaying the result
```python
# Displaying original and scanned document images using Matplotlib
```

## Conclusion
With the completion of this project, we have successfully implemented a document scanner using OpenCV. This can be further integrated into various applications for digitizing documents efficiently.

## Author
Code Contributed by Arunita Sahu

