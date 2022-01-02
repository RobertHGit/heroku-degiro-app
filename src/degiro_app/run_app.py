from apscheduler.schedulers.blocking import BlockingScheduler
from degiro_app.lib_degiro_scraping.func import imported_print_log_line
from pytz import timezone

scheduler = BlockingScheduler(timezone=timezone(zone="Europe/Amsterdam"))


@scheduler.scheduled_job("interval", seconds=3)
def timed_job():
    imported_print_log_line()


scheduler.start()
