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
    etf_data: pd.DataFrame = attr.ib(default=None)

    def get_page(self) -> None:
        time.sleep(2)
        full_url = EtfPageLocators.PAGE_URL.value + EtfPageLocators.SEARCH_URL.value
        self.driver.get(url=full_url)

    def scrape_table(self) -> None:
        time.sleep(2)
        dfs = pd.read_html(self.driver.page_source)
        self.tables.append(dfs[0])

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

    def transform_scraped_tables(self) -> None:
        df = pd.concat(self.tables)
        df.drop(df.columns[-1], inplace=True, axis=1)
        df.replace(u"\xa0", u"", regex=True, inplace=True)
        df = df.rename(
            columns={
                "Product": "product",
                "Symbool | ISIN": "symbool_isin",
                "Beurs": "beurs",
                "Laatst": "laatst",
                "+/-": "abs_change",
                "+/- %": "perc_change",
                "Volume": "volume",
                "Slot": "slot",
                "Laatste": "laatste",
                "LKF": "lkf",
                "Gebied": "gebied",
            }
        )
        for col_name in ["laatst", "perc_change"]:
            df[f'{col_name}_sign'] = df[col_name].astype(str).str[0]
            df[col_name] = df[col_name].str[1:]
            df[col_name] = df[col_name].str.replace(",", ".")
        df["perc_change"] = df["perc_change"].str[:-1]
        df["laatst"] = df["laatst"].astype(float)
        df["perc_change"] = df["perc_change"].astype(float)

        # df[["Symbool", "ISIN"]] = df.symbool_isin.str.split("| ", expand=True)
        self.etf_data = df
