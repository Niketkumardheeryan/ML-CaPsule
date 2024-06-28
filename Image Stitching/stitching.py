import numpy as np
import cv2
import glob
import imutils
import os

# Configurable parameters
dataset_name = 'Glacier'
threshold = 0.97

# Load images
file_path = os.path.join('Dataset', dataset_name, '*.jpg')
image_paths = glob.glob(file_path)
images = []
for image_path in image_paths:
    img = cv2.imread(image_path)
    if img is not None:
        images.append(img)
    else:
        print(f"Error loading image: {image_path}")

# Check OpenCV version and create the stitcher accordingly
if cv2.__version__.startswith('3'):
    stitcher = cv2.createStitcher()
else:
    stitcher = cv2.Stitcher_create()

# Stitch the images
error, stitched_img = stitcher.stitch(images)

if error == cv2.Stitcher_OK:
    # Save the stitched image
    result_folder = os.path.join('Result', dataset_name)
    os.makedirs(result_folder, exist_ok=True)
    output_path1 = os.path.join(result_folder, 'output1.jpg')
    
    cv2.imwrite(output_path1, stitched_img)
    cv2.imshow("Stitched Image", stitched_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Add a border to the stitched image
    stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    # Convert to grayscale and apply threshold to find the black border
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv2.contourArea)

    # Define a threshold to determine if the border is small
    if cv2.contourArea(areaOI) < threshold * gray.size:
        # Create a mask with the largest contour
        mask = np.zeros(thresh_img.shape, dtype="uint8")
        x, y, w, h = cv2.boundingRect(areaOI)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # Erode the mask until the black border is removed
        minRectangle = mask.copy()
        sub = mask.copy()

        while cv2.countNonZero(sub) > 0:
            minRectangle = cv2.erode(minRectangle, None)
            sub = cv2.subtract(minRectangle, thresh_img)

        # Find the new bounding box
        contours = cv2.findContours(minRectangle, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        areaOI = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(areaOI)

        # Crop the image to the bounding box
        stitched_img = stitched_img[y:y + h, x:x + w]

    # Save the processed image
    output_path2 = os.path.join(result_folder, 'output2.jpg')
    cv2.imwrite(output_path2, stitched_img)
    cv2.imshow("Stitched Image Processed", stitched_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error during stitching:", error)
    print("Images could not be stitched! Likely not enough keypoints being detected!")
