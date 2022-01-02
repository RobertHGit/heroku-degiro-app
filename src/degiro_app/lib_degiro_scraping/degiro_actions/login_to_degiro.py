import os

import attr
from degiro_app.lib_degiro_scraping.degiro_pages.login_page import LoginPage
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class LoginToDeGiro:
    driver: WebDriver = attr.ib()

    def run(self) -> WebDriver:
        login_page = LoginPage(driver=self.driver)
        login_page.get_page()
        login_page.enter_user_name(username=os.environ.get("DEGIRO_USER_NAME"))
        login_page.enter_password(password=os.environ.get("DEGIRO_MAGIC"))
        login_page.login()
        return login_page.driver

