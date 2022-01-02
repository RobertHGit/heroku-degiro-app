from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job("interval", seconds=3)
def timed_job():
    print("[LOG] SCHEDULED_RUN - print every 3 seconds.")


sched.start()
