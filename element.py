from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class BasePageElement(object):
    def __set__(self, obj, value):
        driver = obj.driver
        wait = WebDriverWait(driver, 10)

        try:
            element = wait.until(EC.presence_of_element_located(self.locator))
            element.send_keys(value)
        except Exception:
            pass

    def __get__(self, obj, owner):
        self.driver = obj.driver
        return self

    def value(self):
        wait = WebDriverWait(self.driver, 10)

        try:
            element = wait.until(EC.presence_of_element_located(self.locator))
            return element.get_attribute("value")
        except Exception:
            pass

    def text(self):
        wait = WebDriverWait(self.driver, 10)

        try:
            element = wait.until(EC.presence_of_element_located(self.locator))
            return element.text
        except Exception:
            pass

    def click(self):
        wait = WebDriverWait(self.driver, 10)

        try:
            element = wait.until(EC.presence_of_element_located(self.locator))
            element.click()
        except Exception:
            pass


class SelectPageElement(BasePageElement):
    def select_option(self, text):
        wait = WebDriverWait(self.driver, 10)

        try:
            element = Select(wait.until(EC.presence_of_element_located(self.locator)))
            element.select_by_visible_text(text)
        except Exception:
            pass