from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", seconds=3)
def timed_job():
    print("[LOG] SCHEDULED_RUN - print every 3 seconds.")


scheduler.start()
