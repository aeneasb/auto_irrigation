import RPi.GPIO as GPIO
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pumpdur", help="Duration of pumping in seconds",type=int)
parser.add_argument("pin",type=int)
args = parser.parse_args()
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pin,GPIO.OUT,initial=GPIO.LOW)
print('pump {0:d}s'.format(args.pumpdur))
GPIO.output(args.pin,GPIO.HIGH)
sleep(args.pumpdur)
GPIO.output(args.pin,GPIO.LOW)
print('done')
GPIO.cleanup()
