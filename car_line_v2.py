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
TESSERACT_CONFIG = ('-l eng --oem 1 --psm 8 -c tessedit_char_whitelist=0123456789')  # Try the Psm 8 config
MOTION_THRESHOLD = 20
FRAME_INTERVAL = 5  # Process every 5th frame


# New CONFIG Settings for Digits - Tune based on your image
ROI_X_START = 200  # Approximate x-coordinate of the top-left corner of digits
ROI_Y_START = 450  # Approximate y-coordinate of the top-left corner of digits
ROI_WIDTH = 500   # Approximate width of the digit region
ROI_HEIGHT = 150  # Approximate height of the digit region


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
        # Predefined ROI Based on Original Image
        roi = frame[ROI_Y_START:ROI_Y_START + ROI_HEIGHT, ROI_X_START:ROI_X_START + ROI_WIDTH]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # Convert ROI to grayscale

        # ** AGGRESSIVE PREPROCESSING **
        # Apply Adaptive Thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        #Apply Morphological Transformations for smoothing the images
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)  # Remove small noises
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)  # Close potential gaps

        #Show the preprocessed to help see whats being detected
        cv2.imshow("Preprocessed ROI", closing)
        cv2.waitKey(1)

        # Recognize text using Tesseract OCR
        try:
            text = pytesseract.image_to_string(closing, config=TESSERACT_CONFIG)  # To OCR process using correct whitelist
            text = ''.join(filter(str.isdigit, text)).strip()  # We will be extracting only digits
            logging.info(f"Raw OCR Text: '{text}'")  # Extracted final numbers and showing

            if len(text) == NUMBER_LENGTH and text.isdigit():
                x,y = ROI_X_START,ROI_Y_START  #We manually added the config variables so its important to keep in mind here
                cv2.rectangle(frame, (x, y), (x + ROI_WIDTH, y + ROI_HEIGHT), (0, 255, 0), 2)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


                try:
                    api_data = {'student_number': text}
                    response = requests.post(API_ENDPOINT, json=api_data)

                    if response.status_code == 200:
                        student_name = response.json().get('student_name', 'Unknown')
                        cv2.putText(frame, student_name, (x, y + ROI_HEIGHT + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                    (0, 255, 0), 2)
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

        frame_count = 0
        while True:
            # Read the next frame
            ret, frame2 = cap.read()
            if not ret:
                logging.error("Error: Could not read frame")
                break

            # Small delay here to reduce the frame rate the camera looks for motion
            time.sleep(0.1)  # Short break before the next frame

            # Detect motion

            if frame_count % FRAME_INTERVAL == 0:
                if detect_motion(frame1, frame2):
                    logging.info("Motion detected!")

                    # Recognize digits in captured frame
                    frame2 = recognize_digits(frame2)


                    # Wait 2 seconds before scanning again
                    time.sleep(2)

                # Update frame1 for the next iteration
                frame1 = frame2.copy()
            frame_count += 1
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