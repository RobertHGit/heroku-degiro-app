import time
from typing import List

import attr
import pandas as pd
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import (
    PortfolioPageLocators,
)
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class PortfolioPage:
    driver: WebDriver = attr.ib()
    portfolio_data: pd.DataFrame = attr.ib(default=None)

    def get_page(self) -> None:
        time.sleep(3)
        self.driver.get(url=PortfolioPageLocators.PAGE_URL.value)

    def scrape_table(self) -> None:
        time.sleep(3)
        dfs = pd.read_html(
            self.driver.page_source, parse_dates=True, thousands=".", decimal=","
        )
        self.portfolio_data = dfs
