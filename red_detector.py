import cv2
import numpy as np

# Initialize the USB Camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Opened")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Not Returned")
        break

    hsv_cap = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red has hue values at both ends of the HSV spectrum
    # We need two masks and combine them
    lower_red1 = np.array([0, 150, 150])
    upper_red1 = np.array([3, 255, 255])
    lower_red2 = np.array([177, 150, 150])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for both red ranges
    mask1 = cv2.inRange(hsv_cap, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_cap, lower_red2, upper_red2)
    
    # Combine the masks
    mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
