import time
class Coffee():
    def __init__(self,wat,moi,moi2,light,pump):
        self.wat = wat
        self.moi = moi
        self.moi2 = moi2
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
                m =(self.moi.sensor.voltage+self.moi.offset+
                 self.moi2.sensor.voltage+self.moi2.offset)/2
                print('moisture_level: {0:.2f}'.format(m))
                if m <= self.moi.thresh:
                    self.pump.trigger(dur=3)
