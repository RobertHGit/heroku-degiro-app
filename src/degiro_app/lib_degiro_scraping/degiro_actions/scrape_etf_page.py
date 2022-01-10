from typing import Tuple

import attr
from degiro_app.lib_degiro_scraping.degiro_actions.login_to_degiro import LoginToDeGiro
from degiro_app.lib_degiro_scraping.degiro_pages.etf_page import EtfPage
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class ScrapeEtfPage:
    driver: WebDriver = attr.ib()

    def run(self) -> Tuple[WebDriver, DataFrame]:
        login_to_degiro = LoginToDeGiro(driver=self.driver)
        driver = login_to_degiro.run()

        etf_page = EtfPage(driver=driver)
        etf_page.get_page()
        etf_page.scrape_tables()
        etf_page.transform_scraped_tables()
        return etf_page.driver, etf_page.etf_data
