import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0) #P0=water sensor, P1 = moisture sensor
chan2 = AnalogIn(ads, ADS.P1)
while True:
    time.sleep(1)
    print('chan: {0:.3f} chan2: {1:.3f}'.format(chan.voltage,chan2.voltage))
    print('info: chan2 isch vrgrabe')
