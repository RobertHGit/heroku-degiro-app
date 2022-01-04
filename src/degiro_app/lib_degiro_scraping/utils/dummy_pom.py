import time
from enum import Enum
from typing import Any

import attr
from selenium.webdriver.chrome.webdriver import WebDriver


class DummyPageLocators(Enum):
    PAGE_URL = "https://hckrnews.com/"


@attr.s
class DummyPage:
    driver: Any = attr.ib()

    def get_page(self) -> None:
        time.sleep(3)
        self.driver.get(url=DummyPageLocators.PAGE_URL.value)


@attr.s
class GoToDummyPage:
    driver: WebDriver = attr.ib()

    def run(self) -> WebDriver:
        dummy_page = DummyPage(driver=self.driver)
        dummy_page.get_page()
        return dummy_page.driver
