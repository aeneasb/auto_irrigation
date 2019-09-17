import time
class Coffee():
    def __init__(self,wat,moi,moi2,light,pump,configFile):
        self.configFile = configFile
        self.wat = wat
        self.moi = moi
        self.moi2 = moi2
        self.light = light
        self.pump = pump
        self.shower_dur = self.load_param(param='shower_dur')
        self.rainstorm_dur= self.load_param(param='rainstorm_dur')
    def shower(self):
        print('shower')
        self.pump.trigger(dur=self.shower_dur)
    def rainstorm(self):
        print('water that plant!')
        self.pump.trigger(dur=self.rainstorm_dur)
    def measure(self):
        # Todo: Load data into database
        #Check water level
        print('water_level:'+str(self.wat.sensor.voltage))
        #Check light
        print('light_level:'+str(self.light.sensor.voltage))
        #Measure moisture and trigger pump
        m=(self.moi.sensor.voltage+self.moi.offset
           +self.moi2.sensor.voltage+self.moi2.offset)/2
        print('moisture_level: {0:.2f}'.format(m))
    def load_param(self,param):
        with open(self.configFile,'r') as fp:
            configDict = json.loads(fp.read())
            val = int(configDict.get(param,0))
            return val
