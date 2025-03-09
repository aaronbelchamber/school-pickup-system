import cv2
import pytesseract
from PIL import Image
import requests
import imutils
import time
import logging
import numpy as np

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration (Adjust these!)
pytesseract.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
API_ENDPOINT = "https://localhost:8080"

MIN_CONFIDENCE = 0.8
NUMBER_LENGTH = 3
TESSERACT_CONFIG = ('-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789') #Try the Psm 8 config
MOTION_THRESHOLD = 20


#New CONFIG Settings for Digits
MIN_DIGIT_WIDTH = 10 #MIN width for digits
MIN_DIGIT_HEIGHT = 20 #Min height for digits
MAX_DIGIT_WIDTH = 100 #Maximum width for digits
MAX_DIGIT_HEIGHT = 200 #Maximum height for digits
MIN_DIGIT_ASPECT = 0.2 #Minimum aspect ratio (width / height)
MAX_DIGIT_ASPECT = .5#Maximum aspect ratio

def detect_motion(frame1, frame2):
    """Detects motion between two frames."""
    try:
        # Calculate the difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # If enough motion is detected, return True
        if len(contours) > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error during motion detection: {e}")
        return False


def recognize_digits(frame):
    """Recognizes digits in a frame."""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Perform edge detection
        edged = cv2.Canny(blurred, 75, 200)

        # Find contours
        contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        #Apply dilation Before contour Detection
        kernel = np.ones((5, 5), np.uint8)  # Adjust kernel size
        dilated = cv2.dilate(edged, kernel, iterations=1)  # Adjust iterations

        # Find contours on the dilated image
        contours = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        window_names = []

        for c in contours:
            # Extract bounding box and ROI
            (x, y, w, h) = cv2.boundingRect(c)

            # Check for minimum and maximum size of digit and new ASpect Ratio config
            if w > MIN_DIGIT_WIDTH and h > MIN_DIGIT_HEIGHT and w < MAX_DIGIT_WIDTH and h < MAX_DIGIT_HEIGHT:
                aspect_ratio = float(w) / h
                if MIN_DIGIT_ASPECT <= aspect_ratio <= MAX_DIGIT_ASPECT:

                    roi = gray[y:y + h, x:x + w]

                    # ** AGGRESSIVE PREPROCESSING **
                    # 1. Adaptive Thresholding
                    #Less Agressive Try
                    thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 10) #Less agressive  the C Value is now 5 instead of 2
                    #thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                    #Before Finding Contours Apply Dilation
                    #Applying scaling instead of morph
                    scale_percent = 150 # percent of original size
                    width = int(roi.shape[1] * scale_percent / 100)
                    height = int(roi.shape[0] * scale_percent / 100)
                    dim = (width, height)

                    # resize image
                    resized = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
                    cv2.imshow("ROI RESIZE", resized)
                    cv2.waitKey(1)

                    #Show it. MOST IMPORTANT DEBUGGING STEP
                    window_name_ocr = "OCR Input"
                    cv2.imshow(window_name_ocr, thresh)  # Show the preprocessed ROI
                    cv2.waitKey(3)  # Add a small delay to allow the window to update
                    window_names.append(window_name_ocr)


                    # Recognize text using Tesseract OCR
                    try:

                        #Invert Threshold test.
                        inverted_thresh = cv2.bitwise_not(thresh) #Try this

                        #Added inverted or not
                        text = pytesseract.image_to_string(inverted_thresh, config=TESSERACT_CONFIG) #To OCR process using correct whitelist
                        #Now it has the OCR process on the correct grayscale image for OCR
                        text = ''.join(filter(str.isdigit, text)).strip() #We will be extracting only digits
                        logging.info(f"Raw OCR Text: '{text}'") #Extracted final numbers and showing

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
        return frame

    except Exception as e:
        logging.error(f"Error during digit recognition: {e}")
        return frame
def main():
    """Main function to capture video and detect motion."""
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Error: Could not open webcam")
            return

        # Read the first frame
        ret, frame1 = cap.read()
        if not ret:
            logging.error("Error: Could not read initial frame")
            return

        while True:
            # Read the next frame
            ret, frame2 = cap.read()
            if not ret:
                logging.error("Error: Could not read frame")
                break

            # Detect motion
            if detect_motion(frame1, frame2):
                logging.info("Motion detected!")

                #Recognize digits in captured frame
                frame2 = recognize_digits(frame2)

            # Show the current frame
            cv2.imshow("Motion Detection", frame2)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        logging.error(f"Error in main function: {e}")

    finally:
        # Release the camera and destroy all windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()