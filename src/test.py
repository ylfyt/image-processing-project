from time import sleep, time
import datetime
from threading import *
# import RPi.GPIO as GPIO
from gpiozero import Button
from gpiozero import LED
import cv2
from classes.scan_state import ScanState

# from gpiozero import Button
# from time import sleep

# button = Button(6)

# while True:
#     if button.is_pressed:
#         print("Button is pressed")
#     else:
#         print("Button is not pressed")

#     sleep(1)

# from gpiozero import LED
# from time import sleep

# led = LED(24)

# while True:
#     led.on()
#     sleep(1)
#     led.off()
#     sleep(1)


# GPIO.setmode(GPIO.BOARD)
btnFlash=Button(12)     # flash
btnFlashPressed = False
btnPhoto=20      # take photo
btnReset= Button(16)
ledToggle = LED(20)           # LED
buzzerToggle = LED(21)
# GPIO.setup(btnFlash,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnPhoto,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnReset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED,GPIO.OUT)
# GPIO.setup(BUZZER,GPIO.OUT)
flagLED=False
flagBuzzer=False


# class state

def buzzerSignal():
    flagSignal = False
    for i in range(ScanState.buzzerRepeat):
        if flagSignal==False:
            ScanState.buzzerToggle.on()
            flagSignal=True
            sleep(ScanState.buzzerDelay)
        else:
            ScanState.buzzerToggle.off()
            flagSignal=False
            sleep(ScanState.buzzerDelay)

def ledSwitch():
    if (ScanState.ledFlag == False):
        ScanState.ledToggle.on()
    else:
        ScanState.ledToggle.off()
    ScanState.ledFlag = not ScanState.ledFlag

# def getPicture(frame, cond):
#     path = '../img/' + '{%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '_' + cond + '.jpg'
#     cv2.imwrite(path, frame)
#     print("Scanned")
#     return path

prevReset = False
prevFlash = False

while True:
    # print('State: ', end="")
    flashState = btnFlash.is_pressed
    if flashState and prevFlash != flashState:
        print("btnFlash Was Pressed:")
        ScanState.ledToggle = ledToggle
        Thread( target=ledSwitch ).start()
        # Thread( target=signal(buzzerToggle, flagBuzzer, 10, 0.5) ).start()
        # ledToggle.on()
    prevFlash = flashState
    print(prevFlash)
    
    resetState = btnReset.is_pressed
    if resetState and resetState != prevReset:
        print("btnReset Was Pressed:")
        # clear class state
        ScanState.buzzerToggle = buzzerToggle
        ScanState.buzzerDelay = 0.3
        ScanState.buzzerRepeat = 6
        Thread( target=buzzerSignal ).start()
        # if (ScanState.isState("picture")):
        #     ScanState.setIdleState()
        # elif (ScanState.isState("idle")):
        #     ScanState.resetScan()
    prevReset = resetState
    # print()


