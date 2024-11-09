import streamlit as st
import pandas as pd
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils import contours

# Function to create answer key from CSV
def create_answer_key(csv_file):
    answer_key = {}
    letter_to_int = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}

    csv_data = pd.read_csv(csv_file)

    for index, row in csv_data.iterrows():
        question = int(row['Question']) - 1  # Index from 0
        answer_letter = row['Answer'].strip().upper()
        answer = letter_to_int.get(answer_letter, -1)

        if answer != -1:
            answer_key[question] = answer

    return answer_key

# Streamlit App Interface
st.title("OMR Answer Sheet Grader")

# Upload answer key CSV file
uploaded_csv = st.file_uploader("Upload Answer Key CSV", type=["csv"])

if uploaded_csv is not None:
    st.write("Answer key CSV uploaded!")
    ANSWER_KEY = create_answer_key(uploaded_csv)
    st.write("Answer Key: ", ANSWER_KEY)

    # Upload OMR sheet image
    uploaded_image = st.file_uploader("Upload OMR Sheet Image", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        # Convert uploaded image to a numpy array for OpenCV
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        # OMR Processing starts here
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        # Find contours of the document
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        docCnt = None

        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                if len(approx) == 4:
                    docCnt = approx
                    break

        # Get top-down view of the OMR sheet
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))

        # Apply thresholding to get a binary image
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        # Filter contours to find bubbles
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)

            if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                questionCnts.append(c)

        # Sort question contours top-to-bottom
        questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

        correct = 0
        questionsContourImage = paper.copy()

        # Threshold for considering a bubble as filled
        FILL_THRESHOLD = 500

        for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):  # 4 options for each question
            cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
            bubbled = []

            # Loop through each bubble in the question
            for (j, c) in enumerate(cnts):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)

                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                if total > FILL_THRESHOLD:  # Consider the bubble as filled
                    bubbled.append(j)

            color = (0, 0, 255)  # Default: Mark the answer as wrong

            # Handle multiple bubbles filled
            if len(bubbled) == 1:
                if ANSWER_KEY[q] == bubbled[0]:
                    color = (0, 255, 0)  # Correct answer, mark green
                    correct += 1
                else:
                    cv2.drawContours(paper, [cnts[ANSWER_KEY[q]]], -1, (0, 255, 0), 3)

            # Multiple bubbles or unfilled
            elif len(bubbled) > 1 or len(bubbled) == 0:
                for idx in bubbled:
                    cv2.drawContours(paper, [cnts[idx]], -1, (0, 0, 255), 3)

            for idx in bubbled:
                cv2.drawContours(paper, [cnts[idx]], -1, color, 3)

        # Calculate and display percentage score
        score = (correct / len(ANSWER_KEY)) * 100
        cv2.putText(paper, f"Score: {score:.2f}%", (10, paper.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        # Display the final graded paper
        st.image(paper, caption=f"Graded OMR Sheet - Score: {score:.2f}%", use_column_width=True)
