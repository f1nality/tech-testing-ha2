from selenium.webdriver.common.by import By
from element import BasePageElement, SelectPageElement
from locators import MainPageLocators


class LoginInput(BasePageElement):
    locator = (By.ID, 'id_Login')


class DomainSelect(SelectPageElement):
    locator = (By.ID, 'id_Domain')


class PasswordInput(BasePageElement):
    locator = (By.ID, 'id_Password')


class LoginSubmitInput(BasePageElement):
    locator = (By.CSS_SELECTOR, '#gogogo .submit')


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    login = LoginInput()
    domain = DomainSelect()
    password = PasswordInput()
    loginSubmit = LoginSubmitInput()

    def authorize(self):
        self.login = 'tech-testing-ha2-13'
        self.domain.select_option('@bk.ru')
        self.password = 'Pa$$w0rD-13'
        self.loginSubmit.click()

    def is_authorized(self):
        return True


class SearchResultsPage(BasePage):
    def is_results_found(self):
        pass