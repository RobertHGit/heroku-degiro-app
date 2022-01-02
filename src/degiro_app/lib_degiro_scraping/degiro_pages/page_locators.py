from enum import Enum


class LoginPageLocators(Enum):
    PAGE_URL = "https://trader.degiro.nl/login/nl#/login"
    USER_NAME_NAME = "username"
    PASSWORD_NAME = "password"
    LOGIN_BUTTON_NAME = "loginButtonUniversal"


class EtfPageLocators(Enum):
    PAGE_URL = "https://trader.degiro.nl/trader/#/products?productType=131&feeType=2&popularOnly=false&exchange=-1&issuer=-1&region=-1&benchmark=-1&assetAllocation=-1&totalExpenseRatioInterval=-%2F-"
    NEXT_PAGE_BUTTON_NAME = "nextPageButton"
    NEXT_PAGE_BUTTON_XPATH = '//*[@id="mainContent"]/div[1]/section/div/section/div[2]/div/section/div[2]/div/div[1]/button[3]/i'

