import RPi.GPIO as GPIO

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

while True:
    if GPIO.input(btnFlash)==0:
        print("btnFlash Was Pressed:")
        
    if GPIO.input(btnReset)==0:
        print("btnReset Was Pressed:")


