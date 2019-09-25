import schedule
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from sys import exit
import argparse
import json
import queue

from Sensor import Sensor_Water, Sensor_Moisture, Sensor_Light, Sensor_Temperature
from Pump import Pump
from Coffee import Coffee
import db_handler
from db_handler import Db_handler

#Main program
def main():
    '''
    The main function for the automatic irrigation system
    Takes care of the timing
    '''
    def load(configFile):
        with open(configFile,'r') as fp:
            return json.loads(fp.read()) 
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile", help="Specify the path of the configFile")
    args = parser.parse_args()
    configFile = load(args.configFile)
    record_queue = queue.Queue() #Queue to place sensor reading
    db = Db_handler(record_queue)
    db.open_or_create_db(configFile.get("db_path"))
    try:
        #Set up the ADC
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        #Create sensor objects
        wat = Sensor_Water(ads,configFile,record_queue)
        moi = Sensor_Moisture(ads,configFile,record_queue)
        moi2 = Sensor_Moisture(ads,configFile,record_queue,name='moisture2')
        #temp= Sensor_Temperature(ads,configFile)
        light = Sensor_Light(ads,configFile,record_queue)
        pump = Pump(configFile) #Pump object
        ruler = Coffee(pump,configFile)
        #Start threads
        wat.start_thread()
        moi.start_thread()
        light.start_thread()
        ruler.start_schedule()
    except Exception as anError:
        print('Unexpected error at start up')
        raise anError
        exit(0)
    try:
        print('Started main loop')
        while True:
            try:
                schedule.run_pending()
                if not db.get_records():
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
