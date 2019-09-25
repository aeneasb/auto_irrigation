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
        self.channel = int(self.configFile.get(self.name+'_chan',0))
        self.poll_freq = int(self.configFile.get('poll_freq',60))
        self.sensor = AnalogIn(ads,self.channel)
        self.record_queue = queue
    def run_threaded(self,job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()
    def start_thread(self):
        self.timer = schedule.every(self.poll_freq).seconds.do(self.run_threaded, self.poll)

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
        w_l = self.sensor.voltage
        self.record_queue.put(db_handler.water_level(self.timer.next_run,w_l))
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
        s_m = self.sensor.voltage
        self.record_queue.put(db_handler.soil_moisture(self.timer.next_run,s_m))
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
        l = self.sensor.voltage
        self.record_queue.put(db_handler.light(self.timer.next_run,l))
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
        t = self.sensor.voltage
        self.record_queue.put(db_handler.temperature(self.timer.next_run,t))
