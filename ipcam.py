import requests
import cv2
import numpy as np
import imutils
  
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
url = "http://192.168.43.233:8080/shot.jpg"

WIDTH = 768
HEIGHT = 768
  
# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    frame = imutils.resize(img, width=WIDTH, height=HEIGHT)

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color
    low_red = np.array([0, 85, 65])
    high_red = np.array([15, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # red = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Red color 2
    low_red2 = np.array([160, 85, 65])
    high_red2 = np.array([179, 255, 255])
    red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
    # red2 = cv2.bitwise_and(frame, frame, mask=red_mask2)

    # Blue color
    low_blue = np.array([95, 100, 70])
    high_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    # blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Green color
    low_green = np.array([35, 95, 70])
    high_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    # green = cv2.bitwise_and(frame, frame, mask=green_mask)

    # orange color
    # low_orange = np.array([10, 100, 20])
    # high_orange = np.array([25, 255, 255])
    # orange_mask = cv2.inRange(hsv_frame, low_orange, high_orange)
    # orange = cv2.bitwise_and(frame, frame, mask=orange_mask)

    # Every color except white
    # low = np.array([0, 42, 0])
    # high = np.array([179, 255, 255])
    # mask = cv2.inRange(hsv_frame, low, high)
    # result = cv2.bitwise_and(frame, frame, mask=mask)
  

    redContours = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    redContours = imutils.grab_contours(redContours)

    redContours2 = cv2.findContours(red_mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    redContours2 = imutils.grab_contours(redContours2)

    blueContours = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blueContours = imutils.grab_contours(blueContours)

    greenContours = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    greenContours = imutils.grab_contours(greenContours)


    for c in blueContours:
        area = cv2.contourArea(c)
        if (area > 2500):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=2)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Blue", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    for c in redContours:
        area = cv2.contourArea(c)
        if (area > 2500):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=2)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Red", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    for c in redContours2:
        area = cv2.contourArea(c)
        if (area > 2500):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=2)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Red", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
    
    for c in greenContours:
        area = cv2.contourArea(c)
        if (area > 2500):
            cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=2)

            M = cv2.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(frame, "Green", (cx-0, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 3)


    cv2.imshow("Android_cam", frame)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()