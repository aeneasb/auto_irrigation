import schedule
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from sys import exit,argv

from Sensor import Sensor, Sensor_Water, Sensor_Moisture, Sensor_Light, Sensor_Temperature
from Pump import Pump
from Coffee import Coffee

#Main program
def main():
    '''
    The main function for the automatic irrigation system
    Takes care of the timing
    '''
    try:
        configFile = None
        if argv.__len__() > 1:
            configFile = argv [1]
        #Set up the ADC
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        #Create sensor objects
        wat = Sensor_Water(ads,configFile)
        moi = Sensor_Moisture(ads,configFile)
        moi2 = Sensor_Moisture(ads,configFile,name='moisture2')
        #temp= Sensor_Temperature(ads,configFile)
        light = Sensor_Light(ads,configFile)
        pump = Pump(configFile) #Pump object
        ruler = Coffee(wat,moi,moi2,light,pump,configFile)
        schedule.every().day.at("06:30").do(ruler.shower) 
        schedule.every().day.at("20:30").do(ruler.shower)
        schedule.every(30).minutes.do(ruler.measure)
        schedule.every().friday.at("12:00").do(ruler.rainstorm)
    except Exception as anError:
        print('Unexpected error at start up')
        raise anError
        exit(0)
    try:
        print('Started main loop')
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                exit(0)
    except Exception as anError:
        print ('Error in main loop:' + str (anError))
        raise anError
    finally:
        pump.cleanup()
        schedule.clear()
        print('irrigation stopped')
if __name__ == '__main__':
    main()
