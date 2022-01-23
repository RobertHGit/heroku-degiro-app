import os

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from degiro_app.lib_degiro_scraping.degiro_actions.login_to_degiro import LoginToDeGiro
from degiro_app.lib_degiro_scraping.degiro_actions.scrape_etf_page import ScrapeEtfPage
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import etf_asset_allocation_search_urls
from degiro_app.lib_degiro_scraping.utils.chrome_utils import (
    get_headless_chrome_options,
)
from degiro_app.lib_degiro_scraping.utils.db_utils import get_db_engine
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy.types import INTEGER, VARCHAR, FLOAT

logging.basicConfig(
    filename="newfile.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

scheduler = BlockingScheduler(timezone=timezone(zone="Europe/Amsterdam"))


@scheduler.scheduled_job("cron", day_of_week="mon-fri", hour=19)
def run_scrape():
    """Daily job to scrape data and store."""

    print("*** running daily task ***")
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    driver = webdriver.Chrome(service=service, options=get_headless_chrome_options())

    login_to_degiro = LoginToDeGiro(driver=driver)
    driver = login_to_degiro.run()

    for asset_class in etf_asset_allocation_search_urls.keys():
        print(f"*** scraping etf_page | {asset_class} ***")

        scrape_etf_page = ScrapeEtfPage(driver=driver, etf_asset_allocation=asset_class)
        driver, asset_df = scrape_etf_page.run()

        print(f"*** writing results | df_shape: {asset_df.shape} ***")
        asset_df.to_sql(
            name=f"etf_{asset_class}_data",
            con=get_db_engine(),
            if_exists="append",
            index=False,
            dtype={
                "product": VARCHAR(),
                "beurs": VARCHAR(),
                "gebied": VARCHAR(),
                "abs_change": FLOAT(),
                "volume": INTEGER(),
                "slot": FLOAT(),
                "symbool": VARCHAR(),
                "isin": VARCHAR(),
                "laatst_sign": VARCHAR(),
                "laatst": FLOAT(),
                "perc_change": FLOAT(),
                "asset_class": VARCHAR(),
            },
        )


scheduler.start()
