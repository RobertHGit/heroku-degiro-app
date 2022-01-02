import attr
from degiro_app.lib_degiro_scraping.degiro_actions.login_to_degiro import LoginToDeGiro
from selenium.webdriver.chrome.webdriver import WebDriver


@attr.s
class ScrapeEtfPage:
    driver: WebDriver = attr.ib()

    def run(self) -> WebDriver:
        login_to_degiro = LoginToDeGiro(driver=self.driver)
        driver = login_to_degiro.run()

        etf_page = EtfPage(driver=driver)
        etf_page.get_page()
        etf_page.next_page_etf_table()
        etf_page.next_page_etf_table()
        return etf_page.driver
