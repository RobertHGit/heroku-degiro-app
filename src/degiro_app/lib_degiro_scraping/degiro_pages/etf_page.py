import time

import attr
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import EtfPageLocators
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@attr.s
class EtfPage:
    driver: WebDriver = attr.ib()

    def get_page(self) -> None:
        time.sleep(2)
        self.driver.get(url=EtfPageLocators.PAGE_URL.value)

    def next_page_etf_table(self) -> None:
        time.sleep(2)
        try:
            self.driver.find_element(by=By.XPATH, value=EtfPageLocators.NEXT_PAGE_BUTTON_XPATH.value).click()
        except ElementClickInterceptedException:
            pass
