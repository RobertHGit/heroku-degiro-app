import time
from typing import List

import attr
import pandas as pd
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import EtfPageLocators
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@attr.s
class EtfPage:
    driver: WebDriver = attr.ib()
    tables: List[pd.DataFrame] = attr.ib(default=[])

    def get_page(self) -> None:
        time.sleep(2)
        self.driver.get(url=EtfPageLocators.PAGE_URL.value)

    def scrape_table(self) -> None:
        time.sleep(2)
        dfs = pd.read_html(self.driver.page_source)
        df = dfs[0]
        df.replace(u'\xa0', u'', regex=True, inplace=True)
        self.tables.append(df)

    def next_page_etf_table(self) -> bool:
        time.sleep(2)
        try:
            self.driver.find_element(by=By.XPATH, value=EtfPageLocators.NEXT_PAGE_BUTTON_XPATH.value).click()
            return True
        except ElementClickInterceptedException:
            return False

    def scrape_tables(self) -> None:
        scrape_switch = True
        while scrape_switch:
            self.scrape_table()
            scrape_switch = self.next_page_etf_table()
