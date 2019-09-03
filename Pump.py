import RPi.GPIO as GPIO
from time import sleep
import json
class Pump ():
    def __init__ (self,configFile):
        self.configFile = configFile
        self.pump_pin = self.load_param(param='pump_pin')
        self.pump_dur = self.load_param(param='pump_dur')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin,GPIO.OUT,initial=GPIO.HIGH)
    def trigger(self,dur=3):
        GPIO.output(self.pump_pin,GPIO.LOW)
        sleep(dur)
        GPIO.output(self.pump_pin,GPIO.HIGH)
    def cleanup(self):
        GPIO.cleanup()
    def load_param(self,param):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            val = int(configDict.get(param,0))
            return val
