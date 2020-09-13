import schedule
from datetime import datetime
class ScheduleService():
    '''
    ScheduleService class, which defines generic functions to irrigate a plant. Requires a pumpService object.
    Args:
        pumpService: pumpService object
        configFile: .json file with parameters
    Returns:
        Schedule object
    '''
    def __init__(self,pumpService,configFile):
        self.configFile = configFile
        self.pumpService = pumpService
        self.cleaning_dur = int(configFile.get('cleaning_dur',0))
        self.cleaning_int = int(configFile.get('cleaning_int',10))
        self.irrigation_dur = int(configFile.get('rainstorm_dur',0))
        self.irrigation_time = configFile.get('irrigation_time','08:00')
        self.tag = configFile.get('tag','default')
    def clean(self):
        print('cleaning-dur: ',self.cleaning_dur)
        print(datetime.now())
        self.pumpService.trigger(dur=self.cleaning_dur)
    def irrigate(self):
        print('watering: ',self.irrigation_dur)
        print(datetime.now())
        self.pumpService.trigger(dur=self.irrigation_dur)
    def start_schedule(self):
        schedule.every().day.at(self.irrigation_time).do(self.irrigate).tag(self.tag,'hourly-tasks')
        schedule.every(self.cleaning_int).minutes.do(self.clean).tag(self.tag,'daily-tasks')
