from enum import Enum

etf_asset_allocation_search_urls = {
    "bonds": "products?productType=131&feeType=2&popularOnly=false&exchange=-1&issuer=-1&region=-1&benchmark=-1&assetAllocation=Bonds&totalExpenseRatioInterval=-%2F-",  # noqa: E501
    "shares": "products?productType=131&feeType=2&popularOnly=false&exchange=-1&issuer=-1&region=-1&benchmark=-1&assetAllocation=Shares&totalExpenseRatioInterval=-%2F-",  # noqa: E501
    "real_estate": "products?productType=131&feeType=2&popularOnly=false&exchange=-1&issuer=-1&region=-1&benchmark=-1&assetAllocation=Real%20Estate&totalExpenseRatioInterval=-%2F-",  # noqa: E501
    "commodities": "products?productType=131&feeType=2&popularOnly=false&exchange=-1&issuer=-1&region=-1&benchmark=-1&assetAllocation=Commodities&totalExpenseRatioInterval=-%2F-",  # noqa: E501
}


class LoginPageLocators(Enum):
    PAGE_URL = "https://trader.degiro.nl/login/nl#/login"
    USER_NAME_NAME = "username"
    PASSWORD_NAME = "password"
    LOGIN_BUTTON_NAME = "loginButtonUniversal"


class EtfPageLocators(Enum):
    PAGE_URL = "https://trader.degiro.nl/trader/#/"
    NEXT_PAGE_BUTTON_NAME = "nextPageButton"
    NEXT_PAGE_BUTTON_XPATH = '//*[@id="mainContent"]/div[1]/section/div/section/div[2]/div/section/div[2]/div/div[1]/button[3]/i'  # noqa: E501
