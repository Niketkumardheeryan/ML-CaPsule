# OMR-TEST-GRADER
OMR (Optical Mark Recognition) is a technique used to capture human-marked data from documents like multiple-choice exams, surveys, and ballots.

## Introduction
OMR (Optical Mark Recognition) is a technique used to capture human-marked data from documents like multiple-choice exams, surveys, and ballots. An OMR scanner identifies marks made by users (typically filled bubbles or boxes) on a printed form, and then processes that data. This project aims to build an OMR scanner and grader that can read and grade multiple-choice test forms including handling of multiple marked bubbles , Non-filled bubbles, Visualization of correct and incorrect answers and displaying the percentage of correct answers at the bottom of the OMR sheet. It also includes reading the answer key from a CSV file, easier to input large answer keys.

## Methodology

# Image Preprocessing:
Image Acquisition: Capture or scan the OMR sheet (scanned or photographed).

Grayscale Conversion: Convert the image to grayscale to simplify further processing.

Thresholding/Binarization: Apply thresholding to convert the grayscale image into a binary image (black and white). This helps in clearly distinguishing the filled marks from the background.

Noise Reduction: Use filters (e.g., Gaussian or median filters) to remove noise from the image.

OMR Sheet Alignment:
Perspective Transformation: Correct any skew or rotation in the scanned form using perspective transformation.
Contour Detection: Find the contours of the OMR form, ensuring to process the area that contains the marks (typically a grid of answer choices).
Bubble/Mark Detection:
Grid Division: Divide the detected region of interest (ROI) into sections corresponding to the answer options (i.e., the grid where bubbles are located).
Mark Identification: For each section, check whether a bubble is filled. This can be done by counting the number of black pixels in each bubble region and setting a threshold to decide if a bubble is marked (e.g., more than 60% of the area is filled). -Handling Multiple Marks: If the user marks more than one option for a question, it can be marked as incorrect based on predefined rules.
Answer Key Comparison: Once the marked bubbles are detected, compare the selected answers with the correct answer key stored in the system. The given code reads the answer key from a CSV file using the pandas library. Each correct answer receives a point, and wrong or multiple answers get no points.

## Grading and Output:

Score Calculation: Calculate the total score by summing up the correct answers.
Result: Output the results to the user, which include the number of correct answers, incorrect answers, and the total score.
Visualization: Highlight correct and incorrect answers on the image by drawing circles around the marks.
Requirements
OpenCV
imutils
numpy
pandas
Streamlit
Setup
Install all required libraries

pip install numpy pandas opencv-python-headless imutils
Make sure you have a CSV file that follows this structure(answers can vary based on the options available for each question) : 
Question,Answer
1,A
2,B
3,C
4,D
5,E

Run cells of notebook
