import json
from adafruit_ads1x15.analog_in import AnalogIn

class Sensor(object):
    """
    Sensor does all general initialization of sensors
    """
    def __init__(self,ads,configFile,name):
        self.name = name
        self.configFile = configFile
        self.channel = self.load()
        self.sensor = AnalogIn(ads,self.channel)
        self.setup()
    def setup (self):
        pass
    def load(self):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            channel = int(configDict.get(self.name+'_chan',0))
            return channel
        
class Sensor_Water(Sensor):
    """
    Water_Sensor specific initialization
    Sample measurement [voltage]:
    baseline:    0
    1/4:         ?
    """
    def __init__(self,ADS,configFile):
        super().__init__(ADS,configFile,name='water')
        self.setup()
    def setup(self):
        self.thresh = self.load_thresh()
    def load_thresh(self):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            thresh = float(configDict.get(self.name+'_thresh',0))
            return thresh

class Sensor_Moisture(Sensor):
    """
    Moisture_Sensor specific initialization
    Sample measurement [voltage]:
    baseline:   0
    dry:        1.55
    wet:        1.9
    """
    def __init__(self,ADS,configFile,name='moisture'):
        super().__init__(ADS,configFile,name)
        self.setup()
    def setup(self):
        self.thresh = self.load_param(param='thresh')
        self.offset = self.load_param(param='offset')
    def load_param(self,param):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            val = float(configDict.get(self.name+'_'+param,0))
            return val

class Sensor_Light(Sensor):
    """
    Light_specific initialization
    Sample measurement [voltage]:
    daylight, cloudy:   2
    dim light:          0.3
    dark:               <0.1
    """
    def __init__(self,ADS,configFile):
        super().__init__(ADS,configFile,name='light')
        self.setup()
    def setup(self):
        self.thresh = self.load_thresh()
    def load_thresh(self):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            thresh = float(configDict.get(self.name+'_thresh',0))
            return thresh

class Sensor_Temperature(Sensor):
    """
    Temperature_specific initialization
    Sample measurement [voltage]:
    room temperature [21.3 deg celcius]:    1.54
    """
    def __init__(self,ADS,configFile):
        super().__init__(ADS,configFile,name='temperature')
        self.setup()
    def setup(self):
        pass
