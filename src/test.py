from time import sleep
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
btnFlash=Button(16)     # flash
btnFlashPressed = False
btnPhoto=20      # take photo
btnReset= Button(21)
ledToggle = LED(12)           # LED
buzzerToggle = LED(26)
# GPIO.setup(btnFlash,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnPhoto,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(btnReset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED,GPIO.OUT)
# GPIO.setup(BUZZER,GPIO.OUT)
flagLED=False
flagBuzzer=False


# class state

def buzzerSignal(repeat, speed):
    flagSignal = False
    for i in range(repeat):
        if flagSignal==False:
            buzzerToggle.on()
            flagSignal=True
            sleep(speed)
        else:
            buzzerToggle.off()
            flagSignal=False
            sleep(speed)

def ledSwitch(toggle):
    if (ScanState.ledFlag == False):
        toggle.on()
    else:
        toggle.off()
    ScanState.ledFlag = not ScanState.ledFlag

# def getPicture(frame, cond):
#     path = '../img/' + '{%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '_' + cond + '.jpg'
#     cv2.imwrite(path, frame)
#     print("Scanned")
#     return path

btnFlashPressed = False
btnResetPressed = False

while True:
    print('State: ', end="")
    if btnFlash.is_pressed and not btnFlashPressed:
        print("btnFlash Was Pressed:")
        Thread( target=ledSwitch(ledToggle) ).start()
        # Thread( target=signal(buzzerToggle, flagBuzzer, 10, 0.5) ).start()
        # ledToggle.on()
    btnFlashPressed = btnFlash.is_pressed
        
    if btnReset.is_pressed and not btnResetPressed:
        print("btnReset Was Pressed:")
        # clear class state
        Thread( target=buzzerSignal(2, 3) ).start()
        # if (ScanState.isState("picture")):
        #     ScanState.setIdleState()
        # elif (ScanState.isState("idle")):
        #     ScanState.resetScan()
    btnResetPressed = btnReset.is_pressed
    print()


