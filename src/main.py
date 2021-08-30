from threading import Thread
from classes.camera import Camera
from classes.scan_state import ScanState
from classes.mask import Mask
from classes.config import Config
import cv2
import control as cl
import time
import colorsys

conditionRange = Config.getCondition()

def getCondition(hsv):
    for cond in conditionRange:
        hsvLower = cond['lower']
        hLower = hsvLower[0]
        sLower = hsvLower[1]
        vLower = hsvLower[2]

        hsvUpper = cond['upper']
        hUpper = hsvUpper[0]
        sUpper = hsvUpper[1]
        vUpper = hsvUpper[2]

        if (hLower <= hsv[0] <= hUpper and sLower <= hsv[1] <= sUpper and vLower <= hsv[2] <= vUpper):
            return cond['desc']
    
    return "Unknown"

def getMaxMask(masks):
    idxMax = 0
    for i in range(len(masks)):
        nMax = cv2.countNonZero(masks[idxMax].getMask())
        n = cv2.countNonZero(masks[i].getMask())
        if (n > nMax):
            idxMax = i
    
    return [masks[idxMax], cv2.countNonZero(masks[idxMax].getMask())]

def showOutput(path):
    frame = cv2.imread(path)
    cv2.putText(frame, "(Result)", (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)
    return frame


ScanState.SCAN_DURATION = Config.getScanDuration()
camConfig = Config.getCamConfig()
ip = False
if (camConfig['ipcam'] == 'true'):
    ip = True
cam = Camera(ipCam=ip, url="http://" + camConfig['ip'] + "/shot.jpg",width=camConfig['width'], height=camConfig['height'])
colorMasks = Config.getColorMasks()
output_path = ""

Thread(target=cl.btnControl).start()

while True:
    frame = 1
    if (ScanState.isState("picture")):
        frame = showOutput(output_path)
    else:
        frame = cam.getVideo()
        # frame = cv2.imread("../img/1.jpg")

    if (not ScanState.isState("picture")):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for mask in colorMasks:
            mask.updateFrame(frame=hsv_frame)

        info = getMaxMask(colorMasks)
        maxMask = info[0]
        nMax = info[1]
        condition = ""
        if (nMax > 750):
            meanRGB = cv2.mean(frame, maxMask.getMask())
            hsvCode = colorsys.rgb_to_hsv(meanRGB[2], meanRGB[1], meanRGB[0])
            hsvCode = (hsvCode[0]*255, hsvCode[1]*255, hsvCode[2])
            condition = getCondition(hsvCode)

            condition += " | " + str(round(hsvCode[0])) +  " " + str(round(hsvCode[1])) +  " " + str(round(hsvCode[2])) 

            maxMask.drawContours(frame, "")
        
        if (ScanState.isState("scanning")):
            if (ScanState.getScanTime() >= ScanState.SCAN_DURATION):
                if (condition == ""):
                    condition = "Aman"
                maxMask.drawContours(frame, condition)
                # TODO: Take a picture
                output_path = cl.getPicture(frame, condition)
                # TODO: Set to picture state
                cl.onBuzzer(3, 0.15)
                ScanState.setPictureState()
            else:
                maxMask.drawContours(frame, "Scanning...")

        if (ScanState.isState("idle")):
            maxMask.drawContours(frame, condition + "(idle)")

    # cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("Camera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    print("1")
    cv2.imshow("Camera", frame)
    
    if (ScanState.exitProgram):
        print("Exit program")
        break

    key = cv2.waitKey(1)
    # Press Esc key to exit
    if (key == 27):
        break
    if (key == 115):
        if (ScanState.isState("picture")):
            ScanState.setIdleState()
        elif (ScanState.isState("idle")):
            ScanState.resetScan()
  
cv2.destroyAllWindows()
exit()
