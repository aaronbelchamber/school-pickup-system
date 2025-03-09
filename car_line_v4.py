import cv2
import easyocr
import requests
import time
import logging
import numpy as np

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration (Adjust these!)
API_ENDPOINT = "http://localhost:8080"
MOTION_THRESHOLD = 20
FRAME_INTERVAL = 5

# Initialize EasyOCR reader
try:
    reader = easyocr.Reader(['en'])  # Specify language (English in this case)
    logging.info("EasyOCR reader initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing EasyOCR reader: {e}")
    exit()  # Exit if EasyOCR initialization fails

# Camera size is 640x480

# New CONFIG Settings for Digits - Tune based on your image
ROI_X_START = 20  # Approximate x-coordinate of the top-left corner of digits
ROI_Y_START = 20  # Approximate y-coordinate of the top-left corner of digits
ROI_WIDTH = 600  # Approximate width of the digit region
ROI_HEIGHT = 440  # Approximate height of the digit region


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


def recognize_digits_with_easyocr(frame):
    """Recognizes digits in a frame using EasyOCR."""
    try:
        # Predefined ROI Based on Original Image
        roi = frame[ROI_Y_START:ROI_Y_START + ROI_HEIGHT, ROI_X_START:ROI_X_START + ROI_WIDTH]

        # Convert ROI to grayscale (EasyOCR works best with grayscale)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        #Now test to see if this portion is working by removing Adaptive
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        #Adaptive Threshold
        #clahe_output = clahe.apply(median)
        # cv2.imshow("Gray Test 1:10", gray)
        # cv2.waitKey(1)

        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(gray, kernel)
        #cv2.imshow("DilationBeforeMedian", dilated)
        #cv2.waitKey(1)
        #.Add what it needs but remove the non value add.

        median = dilated
        clahe_output = clahe.apply(median)
        #-

        clahe_output = gray
        clahe = dilated #To pass this

        #cv2.imshow("clahe_output", clahe_output)
        #cv2.waitKey(1)

        #Show it.
        thresh = clahe_output
        cv2.imshow("EasyOCR Input", thresh)  # Show the preprocessed ROI
        #cv2.waitKey(1)
        #Perform before image, because there is no roi image anymore
        results = reader.readtext(thresh)

        #Extract the text
        recognized_digits = []  # Store digits
        for (bbox, text, prob) in results:
            text = ''.join(filter(str.isdigit, text)).strip()  # Extrat Numbers

            # Now Verify only numbers and correct digit amount
            if len(text) == 3 and text.isdigit():
                recognized_digits.append(text)  # Append Digits

        return recognized_digits

    except Exception as e:
        logging.error(f"Error during digit recognition with EasyOCR: {e}")
        return []
    

def main():
    """Main function to capture video and use EasyOCR for digit recognition."""
    try:
        
        # cv2.namedWindow("AdaptiveThresh", cv2.WINDOW_NORMAL)
        # cv2.moveWindow("Easy OCR Input", 500, 500)

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Error: Could not open webcam")
            return

        # Read the first frame
        ret, frame1 = cap.read()
        if not ret:
            logging.error("Error: Could not read initial frame")
            return

        # Get camera image size and print it

        height, width, channels = frame1.shape #Added line. Note BGR
        print(f"Initial Camera Image Size: Width = {width}, Height = {height}") #added line

        frame_count = 0
        while True:
            # Read the next frame
            ret, frame2 = cap.read()
            if not ret:
                logging.error("Error: Could not read frame")
                break

            cv2.imshow("Original Frame", frame2) #Show orig frame
            # Small delay here to reduce the frame rate the camera looks for motion
            time.sleep(0.1)  # Short break before the next frame

            # Detect motion
            if frame_count % FRAME_INTERVAL == 0:
                if detect_motion(frame1, frame2):
                    print("Motion Detected!")
                    logging.info("Motion detected!")


                    # Recognize digits in captured frame
                    numbers = recognize_digits_with_easyocr(frame2)
                    if numbers:
                        print(f"Numbers: {numbers}")
                        for number in numbers: #loop to post
                           try:
                               api_data = {'student_number': number}
                               response = requests.post(API_ENDPOINT, json=api_data)

                               if response.status_code == 200:
                                   student_name = response.json().get('student_name', 'Unknown')
                                   logging.info(f"Student Number: {number}, Student Name: {student_name}")
                               else:
                                   logging.error(f"API Error: {response.status_code}, {response.text}")
                           except requests.exceptions.RequestException as e:
                                 logging.error(f"API Request Exception: {e}")


                    # Wait 2 seconds before scanning again
                    time.sleep(2)

                # Update frame1 for the next iteration
                frame1 = frame2.copy()
            frame_count += 1


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