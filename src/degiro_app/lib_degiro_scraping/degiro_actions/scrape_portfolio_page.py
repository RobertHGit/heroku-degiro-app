from typing import Tuple

import attr
from degiro_app.lib_degiro_scraping.degiro_pages.etf_page import EtfPage
from degiro_app.lib_degiro_scraping.degiro_pages.portfolio_page import PortfolioPage
from pandas import DataFrame
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class ScrapePortfolioPage:
    driver: WebDriver = attr.ib()

    def run(self) -> Tuple[WebDriver, DataFrame]:
        portfolio_page = PortfolioPage(driver=self.driver)
        portfolio_page.get_page()
        portfolio_page.scrape_table()
        return portfolio_page.driver, portfolio_page.portfolio_data
