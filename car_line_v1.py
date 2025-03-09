import cv2
import pytesseract
from PIL import Image
import requests
import imutils
import time
import numpy as np
import logging  #Import logging

# This didn't work

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration (Adjust these!)
pytesseract.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
API_ENDPOINT = "https://localhost:8080"

PAPER_ASPECT_RATIO = 11 / 8.5
MIN_CONFIDENCE = 0.7
NUMBER_LENGTH = 3
TESSERACT_CONFIG = ('-l eng --oem 1 --psm 7')
MIN_AREA = 500 #Minimum contour area
MAX_AREA = 10000 #Max contour area
MIN_SOLIDITY = 0.8 #Minimum solidity

def preprocess_roi(roi):
    """Preprocesses the ROI to improve OCR accuracy."""
    try:
        # 1. Adaptive Thresholding
        thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # 2. Denoising (Median Blur)
        thresh = cv2.medianBlur(thresh, 3)

        # 3. Morphological Operations (Dilation followed by Erosion - Opening)
        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        #4. Increase contrast - sometimes helpful.
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        thresh = clahe.apply(thresh)

        return thresh
    except Exception as e:
        logging.error(f"Error during ROI preprocessing: {e}")
        return None  # Return None if preprocessing fails

def process_frame(frame):


    """Processes a single frame to detect and read the number."""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            #Area and Solidity filters
            area = cv2.contourArea(c)
            if area < MIN_AREA or area > MAX_AREA:
                continue

            hull = cv2.convexHull(c)
            hull_area = cv2.contourArea(hull)
            if hull_area == 0:
                continue  #Avoid division by zero
            solidity = float(area) / hull_area
            if solidity < MIN_SOLIDITY:
                continue

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            # print(f"DEBUG {peri},{approx}")

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h

                if 0.8 * PAPER_ASPECT_RATIO <= aspect_ratio <= 1.2 * PAPER_ASPECT_RATIO:
                    roi = gray[y:y + h, x:x + w]

                    processed_roi = preprocess_roi(roi)  #Preprocess
                    if processed_roi is None:
                        continue  #Skip if preprocessing failed

                    #DEBUG: Show preprocessed ROI
                    cv2.imshow("Preprocessed ROI", processed_roi)

                    try:
                        text = pytesseract.image_to_string(processed_roi, config=TESSERACT_CONFIG)
                        text = ''.join(filter(str.isdigit, text)).strip()
                        logging.info(f"Raw OCR Text: '{text}'")


                        if len(text) == NUMBER_LENGTH and text.isdigit():
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                            try:
                                api_data = {'student_number': text}
                                response = requests.post(API_ENDPOINT, json=api_data)

                                if response.status_code == 200:
                                    student_name = response.json().get('student_name', 'Unknown')
                                    cv2.putText(frame, student_name, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                    logging.info(f"Student Number: {text}, Student Name: {student_name}")
                                else:
                                    logging.error(f"API Error: {response.status_code}, {response.text}")
                            except requests.exceptions.RequestException as e:
                                logging.error(f"API Request Exception: {e}")

                    except Exception as e:
                        logging.error(f"OCR Error: {e}")

    except Exception as e:
        logging.error(f"Error processing frame: {e}") #Catch any error during frame process and log it

    return frame

def main():
    """Main function to capture video and process frames."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        processed_frame = process_frame(frame)

        cv2.imshow('Live Feed', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(.5)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()