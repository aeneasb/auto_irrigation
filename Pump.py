import RPi.GPIO as GPIO
from time import sleep
import json
class Pump ():
    def __init__ (self,configFile):
        self.configFile = configFile
        self.load()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin,GPIO.OUT,initial=GPIO.HIGH)
    def trigger(self,dur=3):
        GPIO.output(self.pump_pin,GPIO.LOW)
        sleep(dur)
        GPIO.output(self.pump_pin,GPIO.HIGH)
    def cleanup(self):
        GPIO.cleanup()
    def load(self):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            self.pump_pin = int(configDict.get('pump_pin',4))
