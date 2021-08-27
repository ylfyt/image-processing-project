from time import sleep
import datetime
from threading import *
import RPi.GPIO as GPIO
import cv2

GPIO.setmode(GPIO.BOARD)
btnFlash=16      # flash
btnPhoto=20      # take photo
btnReset=21      # reset
LED=12           # LED
BUZZER=18        # Buzzer
GPIO.setup(btnFlash,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnPhoto,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnReset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(BUZZER,GPIO.OUT)
flagLED=False
flagBuzzer=False

# class state

def signal(indicator, flagSignal, repeat):
    for i in range(repeat):
        if flagSignal==False:
            GPIO.output(indicator,True)
            flagSignal=True
            sleep(0.5)
        else:
            GPIO.output(indicator, False)
            flagSignal=False
            sleep(0.5)

def getPicture(frame, cond):
    name = '{%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '_' + cond + '.jpg'
    cv2.imwrite('img/' + name, frame)
    print("Scanned")

def controlBtn(frame):
    if GPIO.input(btnFlash)==0:
        print("btnFlash Was Pressed:")
        Thread( target=signal(LED, flagLED, 1) ).start()
        Thread( target=signal(BUZZER, flagBuzzer, 1) ).start()
        
    if GPIO.input(btnPhoto)==0:
        print("btnPhoto Was Pressed:")
        Thread( target=getPicture(frame))
        Thread( target=signal(BUZZER, flagBuzzer, 2) ).start()
        
    if GPIO.input(btnReset)==0:
        print("btnReset Was Pressed:")
        # clear class state
        Thread( target=signal(BUZZER, flagBuzzer, 1) ).start()



