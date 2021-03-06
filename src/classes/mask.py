from time import time
import cv2
import numpy as np
import imutils

from classes.scan_state import ScanState

class Mask:
    def __init__(self, name, low, high):
        self.SIZE_OF_MIN_CONTOUR_AREA = 750
        self.THICKNESS_OF_CONTOUR_EDGE = 2

        self.name = name
        self.lower = np.array(low)
        self.upper = np.array(high)
    
    def getMask(self):
        return self.mask

    def updateFrame(self, frame):
        self.mask = cv2.inRange(src=frame, lowerb=self.lower, upperb=self.upper)

    def getContours(self):
        contours = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        return contours

    def drawContours(self, frame, condition):
        con = self.getContours()

        areas = [cv2.contourArea(c) for c in con]
        idxMax = 0
        for i in range(1, len(areas)):
            if (areas[idxMax] < areas[i]):
                idxMax = i

        textColor = (0, 0, 255)

        for idx, c in enumerate(con):
            area = cv2.contourArea(c)
            if (area > self.SIZE_OF_MIN_CONTOUR_AREA):
                cv2.drawContours(frame, [c], -1, (0, 255, 0), thickness=self.THICKNESS_OF_CONTOUR_EDGE)

                M = cv2.moments(c)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                # cv2.circle(frame, (cx, cy), 4, (255, 255, 255), -1)
                # cv2.putText(frame, self.name, (cx-0, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), thickness=2)

                if (condition != ""):
                    cv2.putText(frame, condition, (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, thickness=2)
            else:
                if (ScanState.isState("scanning")):
                    if (condition != ""):
                        cv2.putText(frame, condition, (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, thickness=2)
                
                if (ScanState.isState("idle")):
                    if (condition != ""):
                        cv2.putText(frame, condition, (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, thickness=2)

        
        if (len(con) == 0):
            if (ScanState.isState("scanning")):
                if (condition != ""):
                    cv2.putText(frame, condition, (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, thickness=2)

            
            if (ScanState.isState("idle")):
                if (condition != ""):
                    cv2.putText(frame, condition, (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, textColor, thickness=2)