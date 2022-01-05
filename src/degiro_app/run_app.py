import os

import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from degiro_app.lib_degiro_scraping.utils.chrome_utils import get_headless_chrome_options
from degiro_app.lib_degiro_scraping.utils.db_utils import get_db_engine
from degiro_app.lib_degiro_scraping.utils.dummy_pom import GoToDummyPage
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy.types import Integer, VARCHAR

scheduler = BlockingScheduler(timezone=timezone(zone="Europe/Amsterdam"))


@scheduler.scheduled_job("cron", day_of_week="mon-fri", hour=19)
def run_scrape():
    """Daily job to scrape data and store."""

    print("*** running daily task ***")

    # scrape a website
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=get_headless_chrome_options())
    go_to_dummy_page = GoToDummyPage(driver=driver)
    driver = go_to_dummy_page.run()
    print(f"scraped: {driver.current_url}")

    # write to db
    df = pd.DataFrame([{"id": 0, "my_col": "hello world"}])
    df.to_sql(
        name="tmp_test_table",
        con=get_db_engine(),
        if_exists="replace",
        index=False,
        dtype={"id": Integer(), "my_col": VARCHAR()},
    )
    print(f"write to sql: \n {df}")


scheduler.start()
