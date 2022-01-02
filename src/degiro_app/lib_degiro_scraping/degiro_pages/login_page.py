import time

import attr
from degiro_app.lib_degiro_scraping.degiro_pages.page_locators import LoginPageLocators
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


@attr.s
class LoginPage:
    driver: WebDriver = attr.ib()

    def get_page(self) -> None:
        time.sleep(2)
        self.driver.get(url=LoginPageLocators.PAGE_URL.value)

    def scrape_url_page(self) -> str:
        time.sleep(3)
        return self.driver.current_url

    def enter_user_name(self, username: str) -> None:
        time.sleep(2)
        user_name_element = self.driver.find_element(by=By.NAME, value=LoginPageLocators.USER_NAME_NAME.value)
        user_name_element.clear()
        user_name_element.send_keys(username)

    def enter_password(self, password: str) -> None:
        time.sleep(1)
        password_element = self.driver.find_element(by=By.NAME, value=LoginPageLocators.PASSWORD_NAME.value)
        password_element.clear()
        password_element.send_keys(password)

    def login(self) -> None:
        time.sleep(2)
        self.driver.find_element(by=By.NAME, value=LoginPageLocators.LOGIN_BUTTON_NAME.value).click()
