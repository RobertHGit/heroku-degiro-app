from typing import Tuple

import attr
from degiro_app.lib_degiro_scraping.degiro_pages.etf_page import EtfPage
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class ScrapeEtfPage:
    driver: WebDriver = attr.ib()
    etf_asset_allocation = attr.ib(default=None)

    def run(self) -> Tuple[WebDriver, DataFrame]:
        etf_page = EtfPage(
            driver=self.driver, etf_asset_allocation=self.etf_asset_allocation
        )
        etf_page.get_page()
        etf_page.scrape_tables()
        etf_page.transform_scraped_tables()
        return etf_page.driver, etf_page.etf_data
