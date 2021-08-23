from classes.camera import Camera
from classes.mask import Mask
import cv2

cam = Camera(ipCam=True, width=480, height=320)

def getPicture(frame):
        cv2.imwrite('img/out.jpg',frame)
        print("Success")

def getWaveLength(r, g, b):
    red = int(r)
    green = int(g)
    blue = int(b)
    return red * green * blue

  
# While loop to continuously fetching data from the Url
while True:
    # frame = cam.getVideo()
    frame = cv2.imread("img/out2.jpg")

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    redMask = Mask(name="RED", frame=hsv_frame, low=[0, 85, 65], high=[10, 255, 255])
    redMask2 = Mask(name="RED", frame=hsv_frame, low=[160, 85, 65], high=[179, 255, 255])
    blueMask = Mask(name="BLUE", frame=hsv_frame, low=[95, 100, 70], high=[130, 255, 255])
    greenMask = Mask(name="GREEN", frame=hsv_frame, low=[35, 95, 70], high=[80, 255, 255])
    orangeMask = Mask(name="ORANGE", frame=hsv_frame, low=[10, 100, 20], high=[10, 100, 20])
    exceptWhiteMask = Mask(name="WHITE", frame=hsv_frame, low=[0, 42, 0], high=[179, 255, 255])

    # redMask.drawContours(frame=frame)
    # redMask2.drawContours(frame)
    blueMask.drawContours(frame)
    # greenMask.drawContours(frame)

    m = cv2.mean(frame, blueMask.getMask())
    wl = getWaveLength(m[2], m[1], m[0])

    print(m)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    # Press Esc key to exit
    if (key == 27):
        break
    if(key == 32):
        getPicture(frame)
  
cv2.destroyAllWindows()
