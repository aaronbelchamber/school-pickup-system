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
TESSERACT_CONFIG = ('-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789')

MIN_CONFIDENCE = 0.7
NUMBER_LENGTH = 3
TESSERACT_CONFIG = ('-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789') #Essential whitelist
MOTION_THRESHOLD = 20

#New CONFIG Settings for Digits
MIN_DIGIT_WIDTH = 10 #MIN width for digits
MIN_DIGIT_HEIGHT = 20 #Min height for digits
MAX_DIGIT_WIDTH = 100 #Maximum width for digits
MAX_DIGIT_HEIGHT = 200 #Maximum height for digits
MIN_DIGIT_ASPECT = 0.2 #Minimum aspect ratio (width / height)
MAX_DIGIT_ASPECT = 1.0 #Maximum aspect ratio

def detect_motion(frame1, frame2):
    """Detects motion between two frames."""
    try:
        # Calculate the difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)  # Adjust kernel size
        dilated = cv2.dilate(thresh, kernel, iterations=1)  # Adjust iterations

        #dilated = cv2.dilate(thresh, None, iterations=3)
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

        #Store the window names we want to destroy later
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

                    thresh1 = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, c=10) #Try this if gaussian fails
                    thresh = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, c=10) #Currently using this
                    window_name_mean = "Adaptive Mean"
                    window_name_gaussian = "Adaptive Gaussian"

                    cv2.imshow(window_name_mean, thresh1)
                    cv2.imshow(window_name_gaussian, thresh)
                    cv2.waitKey(1)

                    #window_names.append(window_name_mean)
                    #window_names.append(window_name_gaussian)

                    #thresh = thresh #Pick best above

                    #2 MORPH
                    kernel = np.ones((2, 2), np.uint8)  # Adjust kernel size
                    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  # Erosion followed by dilation
                    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # Dilation followed by erosion
                    window_name_opening = "Opening"
                    window_name_closing = "Closing"

                    #cv2.imshow(window_name_opening, opening)
                    #cv2.imshow(window_name_closing, closing)
                    #cv2.waitKey(1)

                    #window_names.append(window_name_opening)
                    #window_names.append(window_name_closing)

                    #pick thresh
                    thresh = opening #Pick best above

                    #Show it. MOST IMPORTANT DEBUGGING STEP
                    window_name_ocr = "OCR Input"
                    #cv2.imshow(window_name_ocr, thresh)  # Show the preprocessed ROI
                    #cv2.waitKey(1)  # Add a small delay to allow the window to update
                    #window_names.append(window_name_ocr)

                    # Recognize text using Tesseract OCR
                    try:
                        text = pytesseract.image_to_string(thresh, config=TESSERACT_CONFIG)
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
                #for window in window_names: #loop to remove windows created

                #    cv2.destroyWindow(window) #No need to delete the individual windows here

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
        cv2.destroyAllWindows() #Move here

if __name__ == "__main__":
    main()