import time
from typing import List

import attr
import pandas as pd
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import (
    EtfPageLocators,
    etf_asset_allocation_search_urls,
)
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@attr.s
class DfTransforms:
    @staticmethod
    def product_col(series):
        return series.transformed_product[2:-1]

    @staticmethod
    def symbool_col(series):
        transformed_col = series.symbool_isin
        transformed_col = transformed_col.replace("\xa0", "")
        if "|" in transformed_col:
            symbool_col, _ = transformed_col.split("| ", 2)
        else:
            symbool_col = None
        return symbool_col

    @staticmethod
    def isin_col(series):
        transformed_col = series.symbool_isin
        transformed_col = transformed_col.replace("\xa0", "")
        if "|" in transformed_col:
            _, isin_col = transformed_col.split("| ", 2)
        else:
            isin_col = transformed_col
        return isin_col

    @staticmethod
    def laatst_sign_col(series):
        return series.laatst[0]

    @staticmethod
    def laatst_col(series):
        transformed_col = series.laatst
        transformed_col = transformed_col.replace("\xa0", "")
        transformed_col = transformed_col[1:]
        transformed_col = transformed_col.replace(",", ".")
        try:
            transformed_col = float(transformed_col)
        except ValueError:
            transformed_col = 0
        return transformed_col

    @staticmethod
    def perc_change_col(series):
        transformed_col = series.perc_change
        transformed_col = transformed_col[1:-1]
        transformed_col = transformed_col.replace(",", ".")
        transformed_col = float(transformed_col)
        if series.perc_change[0] == "+":
            transformed_col = transformed_col / 100
        elif series.perc_change[0] == "-":
            transformed_col = -1 * transformed_col / 100
        return transformed_col


@attr.s
class EtfPage:
    driver: WebDriver = attr.ib()
    tables: List[pd.DataFrame] = attr.ib(default=[])
    etf_asset_allocation = attr.ib(default=None)
    etf_data: pd.DataFrame = attr.ib(default=None)

    def get_page(self) -> None:
        time.sleep(3)
        full_url = f"{EtfPageLocators.PAGE_URL.value}{etf_asset_allocation_search_urls[self.etf_asset_allocation]}"
        self.driver.get(url=full_url)

    def scrape_table(self) -> None:
        time.sleep(3)
        dfs = pd.read_html(
            self.driver.page_source, parse_dates=True, thousands=".", decimal=","
        )
        self.tables.append(dfs[0])

    def next_page_etf_table(self) -> bool:
        time.sleep(2)
        try:
            self.driver.find_element(
                by=By.XPATH, value=EtfPageLocators.NEXT_PAGE_BUTTON_XPATH.value
            ).click()
            return True
        except ElementClickInterceptedException:
            return False

    def scrape_tables(self) -> None:
        scrape_switch = True
        while scrape_switch:
            time.sleep(2)
            self.scrape_table()
            scrape_switch = self.next_page_etf_table()

    def transform_scraped_tables(self) -> None:
        time.sleep(2)
        df = pd.concat(self.tables)

        df.drop(df.columns[-1], inplace=True, axis=1)
        column_mapping = {
            "Product": "product",
            "Symbool | ISIN": "symbool_isin",
            "Beurs": "beurs",
            "Laatst": "laatst",
            "+/-": "abs_change",
            "+/- %": "perc_change",
            "Volume": "volume",
            "Slot": "slot",
            "laatste": "laatste",
            "LKF": "lkf",
            "Gebied": "gebied",
        }
        df = df.rename(columns=column_mapping)

        prefix = "transformed"
        copy_columns = ["product", "beurs", "gebied", "abs_change", "volume", "slot"]
        df[[f"{prefix}_{col_name}" for col_name in copy_columns]] = df[copy_columns]

        df_transforms = DfTransforms()
        df[f"{prefix}_symbool"] = df.apply(
            lambda row: df_transforms.symbool_col(row), axis=1
        )
        df[f"{prefix}_isin"] = df.apply(lambda row: df_transforms.isin_col(row), axis=1)
        df[f"{prefix}_laatst_sign"] = df.apply(
            lambda row: df_transforms.laatst_sign_col(row), axis=1
        )
        df[f"{prefix}_laatst"] = df.apply(
            lambda row: df_transforms.laatst_col(row), axis=1
        )
        df[f"{prefix}_perc_change"] = df.apply(
            lambda row: df_transforms.perc_change_col(row), axis=1
        )
        df[f"{prefix}_product"] = df.apply(
            lambda row: df_transforms.product_col(row), axis=1
        )

        df = df[[col for col in df.columns.to_list() if prefix in col]]
        df = df.rename(
            columns={col: col.replace(f"{prefix}_", "") for col in df.columns.to_list()}
        )
        df["asset_class"] = self.etf_asset_allocation

        self.etf_data = df
