import cv2
import numpy as np
import time

# Initialize the USB Camera
cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Opened")
    exit()

# Variables for FPS calculation
prev_frame_time = 0
new_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Not Returned")
        break
        
    # Calculate FPS
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time) if prev_frame_time > 0 else 0
    prev_frame_time = new_frame_time
    fps_text = f"FPS: {int(fps)}"
    
    hsv_cap = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Even tighter tolerance for red hues
    # First red range (0-3 degrees)
    lower_red1 = np.array([0, 140, 140])
    upper_red1 = np.array([4, 255, 255])
    
    # Second red range (177-180 degrees)
    lower_red2 = np.array([176, 140, 140])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for both red ranges
    mask1 = cv2.inRange(hsv_cap, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_cap, lower_red2, upper_red2)
    
    # Combine the masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Optional: Add some noise reduction with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Only detect contours with significant area
    min_area = 100
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display FPS on the frame
    cv2.putText(frame, fps_text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
