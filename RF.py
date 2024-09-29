import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)

reader = SimpleMFRC522()
while True:
        try:

            id, text = reader.read()
            print(id)
            print(type(id))
            print(text)
            sleep(2)
              
                
        except:
            GPIO.cleanup()