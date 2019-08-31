import time
class Coffee():
    def __init__(self,wat,moi,temp,light,pump):
        self.wat = wat
        self.moi = moi
        self.temp = temp
        self.light = light
        self.pump = pump
    def run(self):
        print('run!')
        #Check water level
        print('water_level:'+str(self.wat.sensor.voltage))
        if self.wat.sensor.voltage <= self.wat.thresh:
            #Check light
            if self.light.sensor.voltage >= self.light.thresh:
                print('light_level:'+str(self.light.sensor.voltage))
                #Measure moisture and trigger pump
                print('moisture_thresh:'+str(self.moi.thresh))
                print('moisture_level:'+str(self.moi.sensor.voltage))
                if self.moi.sensor.voltage <= self.moi.thresh:
                    self.pump.trigger(dur=3)
