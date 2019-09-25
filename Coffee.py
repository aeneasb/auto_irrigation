import schedule
class Coffee():
    '''
    Coffee class, which defines functions specific to the irrigation of a
    coffee plant
    Args:
        wat,moi,moi2,light: All sensor objects used by the coffee class
        pump: pump object
        configFile: .json file with parameters
    Returns:
        Coffee object
    '''
    def __init__(self,pump,configFile):
        self.configFile = configFile
        self.pump = pump
        self.shower_dur = int(configFile.get('shower_dur',0))
        self.rainstorm_dur= int(configFile.get('rainstorm_dur',0))
    def shower(self):
        print('shower')
        self.pump.trigger(dur=self.shower_dur)
    def rainstorm(self):
        print('water that plant!')
        self.pump.trigger(dur=self.rainstorm_dur)
    def start_schedule(self):
        schedule.every().day.at("06:30").do(self.shower) 
        schedule.every().day.at("20:30").do(self.shower)
        schedule.every().friday.at("12:00").do(self.rainstorm)
        schedule.every().tuesday.at("12:00").do(self.rainstorm)
