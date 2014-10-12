import unittest
from selenium import webdriver
import page


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://target.mail.ru/login?redirect_url=%2Fads%2Fcreate%2F")

    def test_login_page(self):
        login_page = page.LoginPage(self.driver)

        login_page.authorize()
        assert login_page.is_authorized()

    def tearDown(self):
        self.driver.close()