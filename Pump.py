import RPi.GPIO as GPIO
from time import sleep
class Pump ():
    '''
    Pump-class which control basic functions of the water pump
    Args:
        configFile: .json file with hardware parameters
    Returns:
        Pump object
    '''
    def __init__ (self,configFile):
        self.configFile = configFile
        self.pump_pin = int(configFile.get('pump_pin',0))
        self.pump_dur = int(configFile.get('pump_dur',0))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin,GPIO.OUT,initial=GPIO.HIGH)
    def trigger(self,dur=3):
        GPIO.output(self.pump_pin,GPIO.LOW)
        sleep(dur)
        GPIO.output(self.pump_pin,GPIO.HIGH)
    def cleanup(self):
        GPIO.cleanup()
