from adafruit_ads1x15.analog_in import AnalogIn
import threading
import schedule
import db_handler
class Sensor(object):
    """
    Sensor does all general initialization of sensors
    Args:
        ads: analog-to-difital converter object
        configFile: Pointer to json file containing the parameter
        name: name of sensor
    Returns:
        sensor object
    """
    def __init__(self,ads,configFile,queue,name):
        self.name = name
        self.configFile = configFile
        self.channel = int(self.configFile.get(self.name+'_chan',None))
        self.poll_freq = int(self.configFile.get('poll_freq',60))
        self.sensor = AnalogIn(ads,self.channel)
        self.record_queue = queue
    def start_thread(self):
        self.timer = schedule.every(self.poll_freq).seconds.do(self.poll)

class Sensor_Water(Sensor):
    """
    Water_Sensor specific initialization
    Sample measurement [voltage]:
    baseline:    0
    1/4:         ?
    """
    def __init__(self,ADS,configFile,queue):
        super().__init__(ADS,configFile,queue,name='water')
        self.setup()
    def setup(self):
        self.thresh = float(self.configFile.get(self.name+'_thresh',0))
    def poll(self):
        self.record_queue.put(db_handler.water_level(self.timer.next_run,self.sensor.voltage))
class Sensor_Moisture(Sensor):
    """
    Moisture_Sensor specific initialization
    Sample measurement [voltage]:
    baseline:   0
    dry:        1.55
    wet:        1.9
    """
    def __init__(self,ADS,configFile,queue,name='moisture'):
        super().__init__(ADS,configFile,queue,name)
        self.setup()
    def setup(self):
        self.thresh = float(self.configFile.get(self.name+'_thresh',0))
        self.offset = float(self.configFile.get(self.name+'_offset',0))
    def poll(self):
        self.record_queue.put(db_handler.soil_moisture(self.timer.next_run,self.sensor.voltage))
class Sensor_Light(Sensor):
    """
    Light_specific initialization
    Sample measurement [voltage]:
    daylight, cloudy:   2
    dim light:          0.3
    dark:               <0.1
    """
    def __init__(self,ADS,configFile,queue):
        super().__init__(ADS,configFile,queue,name='light')
        self.setup()
    def setup(self):
        self.thresh = float(self.configFile.get(self.name+'_thresh',0))
    def poll(self):
        self.record_queue.put(db_handler.light(self.timer.next_run,self.sensor.voltage))
class Sensor_Temperature(Sensor):
    """
    Temperature_specific initialization
    Sample measurement [voltage]:
    room temperature [21.3 deg celcius]:    1.54
    """
    def __init__(self,ADS,configFile,queue):
        super().__init__(ADS,configFile,queue,name='temperature')
        self.setup()
    def setup(self):
        pass
    def poll(self):
        self.record_queue.put(db_handler.temperature(self.timer.next_run,self.sensor.voltage))
