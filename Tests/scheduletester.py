import schedule
import time

def job():
    print("I'm working...")
schedule.every().day.at("21:22").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
    print(schedule.next_run())
