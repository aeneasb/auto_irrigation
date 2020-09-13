import RPi.GPIO as GPIO
from time import sleep
class PumpService ():
    '''
    PumpService-class which control basic functions of a water pump
    Args:
        configFile: .json file with hardware parameters
    Returns:
        PumpService object
    '''
    def __init__ (self,configFile):
        self.configFile = configFile
        self.pump_pin = int(configFile.get('pump_pin',0))
        self.pump_dur = int(configFile.get('pump_dur',0))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin,GPIO.OUT,initial=GPIO.LOW)
    def trigger(self,dur=3):
        GPIO.output(self.pump_pin,GPIO.HIGH)
        sleep(dur)
        GPIO.output(self.pump_pin,GPIO.LOW)
    @staticmethod
    def cleanup():
        GPIO.cleanup()
