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


class MenuAuthButtonTextAuth(BasePageElement):
    locator = (By.CSS_SELECTOR, '.x-ph__menu__button__text_auth')


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    loginInput = LoginInput()
    domainSelect = DomainSelect()
    passwordInput = PasswordInput()
    loginSubmit = LoginSubmitInput()
    textAuth = MenuAuthButtonTextAuth()

    def authorize(self, login, domain, password):
        self.login = login
        self.domain = domain
        self.password = password

        self.loginInput = login
        self.domainSelect.select_option(domain)
        self.passwordInput = password
        self.loginSubmit.click()

    def is_authorized(self):
        user_name = self.textAuth.text()

        return user_name == self.login + self.domain


class SearchResultsPage(BasePage):
    def is_results_found(self):
        pass