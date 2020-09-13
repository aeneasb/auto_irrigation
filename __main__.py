import schedule
import time
from datetime import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from sys import exit
import argparse
import json
import queue

from Services.Sensor import Sensor_Water, Sensor_Moisture, Sensor_Light, Sensor_Temperature
from Services.PumpService import PumpService
from Services.ScheduleService import ScheduleService
import db_handler
from db_handler import Db_handler

#Main program
def main():
    '''
    The main function for the irrigation system and sensor data.
    '''
    def load(configFiles):
        configs = []
        if isinstance(configFiles, str):
            return []
        for configFile in configFiles:
            with open(configFile,'r') as cf:
                configs.append(json.loads(cf.read()))
        return configs
    parser = argparse.ArgumentParser()
    parser.add_argument("--configFilesIrrigation", help="Specify the path of the configFile(s) for the irrigation", nargs='*')
    parser.add_argument("--configFilesSensor", help="Specify the path of the configFile(s) for the sensors", nargs='?', const='e',default='e')
    args = parser.parse_args()
    configIrrigation = load(args.configFilesIrrigation)
    configSensor = load(args.configFilesSensor)
    #record_queue = queue.Queue() #Queue to place sensor reading
    #db = Db_handler(record_queue)
    #db.open_or_create_db(configSensor.get("db_path"))
    try:
        '''
        #Set up the ADC
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        #Create sensor objects
        wat = Sensor_Water(ads,configSensor,record_queue)
        moi = Sensor_Moisture(ads,configFile,record_queue)
        temp= Sensor_Temperature(ads,configFile)
        light = Sensor_Light(ads,configFile,record_queue)
        '''
        for config in configIrrigation:
            ScheduleService(PumpService(config),config).start_schedule()
        #Start threads
        '''
        wat.start_thread()
        moi.start_thread()
        light.start_thread()
        '''
    except Exception as anError:
        print('Unexpected error at start up')
        raise anError
        exit(0)
    try:
        print('Started main loop')
        while True:
            try:
                if 7 <= datetime.now().hour <= 22:
                    schedule.run_pending()
                #if not db.get_records():
                time.sleep(1)
            except KeyboardInterrupt:
                exit(0)
    except Exception as anError:
        print ('Error in main loop:' + str (anError))
        raise anError
    finally:
        PumpService.cleanup()
        schedule.clear()
        #db.conn.commit()
        #db.conn.close()
        print('irrigation stopped')
if __name__ == '__main__':
    main()
