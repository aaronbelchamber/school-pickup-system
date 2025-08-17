import cv2

'''
This is just to test that your devices camera works.
'''
try:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"An error occurred: {e}")

exit()

img = cv2.imread("./tests/test-number-card.jpg")  # Replace with the path to an actual image
cv2.imshow("Test Image", img)
cv2.waitKey(0)  # Wait until a key is pressed
cv2.destroyAllWindows()