from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.lib.elements import BasePageElement, SelectPageElement


class BasePage(object):
    url = ''

    def __init__(self, driver, force_load=True):
        self.driver = driver

        if force_load:
            self.driver.get(self.url)


class TargetMailRuPage(BasePage):
    textAuth = BasePageElement((By.CSS_SELECTOR, '.x-ph__menu__button__text_auth'))

    def is_authorized(self, login, domain):
        user_name = self.textAuth.text()

        return user_name == login + domain


class AdsCampaignsPage(TargetMailRuPage):
    url = 'https://target.mail.ru/ads/campaigns/'

    edit_first_campaign_button = BasePageElement((By.CSS_SELECTOR, '.campaign-row .control__link_edit'))
    delete_first_campaign_button = BasePageElement((By.CSS_SELECTOR, '.campaign-row .control__preset_delete'))


class AdControlPage(TargetMailRuPage):
    campaign_name = BasePageElement((By.CSS_SELECTOR, '.base-setting__campaign-name__input'))
    banner_title = BasePageElement((By.CSS_SELECTOR, '.banner-form__input[data-name="title"]'))
    banner_text = BasePageElement((By.CSS_SELECTOR, '.banner-form__input[data-name="text"]'))
    banner_url = BasePageElement((By.CSS_SELECTOR, '.banner-form__row[data-top="false"] .banner-form__input[data-name="url"]'))

    banner_image = BasePageElement((By.CSS_SELECTOR, '.banner-form__input[data-name="image"]'))
    banner_image_preview = BasePageElement((By.CSS_SELECTOR, '.banner-preview__img'))

    target_restrict_switch = BasePageElement((By.CSS_SELECTOR, '.campaign-setting__wrapper_restrict span'))

    target_region_suggester = BasePageElement((By.CSS_SELECTOR, '.campaign-setting__wrapper[data-name="regions"] .suggester__input'))

    submit_button = BasePageElement((By.CSS_SELECTOR, '.main-button-new'))

    @property
    def banner_image_preview_display(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.banner_image_preview.locator))

        return self.banner_image_preview.css('display')

    def get_target_restrict_by_value(self, value):
        element = BasePageElement((
            By.CSS_SELECTOR,
            '.campaign-setting__wrapper_restrict input[data-value="{0}"] + label'.format(value)
        ))
        element.driver = self.driver

        return element

    def get_target_region_by_name(self, name):
        element = BasePageElement((
            By.CSS_SELECTOR,
            u'.campaign-setting__wrapper[data-name="regions"] span[data-node-id="{0}"] + input'.format(name)
        ))
        element.driver = self.driver

        return element

    def get_target_region_chosen(self):
        result = []
        css_selector = '.campaign-setting__chosen-box__item__name'
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            elements = self.driver.find_elements_by_css_selector(css_selector)

            for element in elements:
                result.append(element.text)
        except Exception:
            pass

        return result

    def deselect_all_target_region_chosen(self):
        css_selector = '.campaign-setting__chosen-box__item__close'
        wait = WebDriverWait(self.driver, 10)

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            elements = self.driver.find_elements_by_css_selector(css_selector)

            for element in elements:
                element.click()
                wait.until_not(EC.visibility_of(element))
        except Exception:
            pass


class AdEditPage(AdControlPage):
    pass


class AdCreatePage(AdControlPage):
    url = 'https://target.mail.ru/ads/create/'


class LoginPage(TargetMailRuPage):
    url = 'https://target.mail.ru/login'

    loginInput = BasePageElement((By.ID, 'id_Login'))
    domainSelect = SelectPageElement((By.ID, 'id_Domain'))
    passwordInput = BasePageElement((By.ID, 'id_Password'))
    loginSubmit = BasePageElement((By.CSS_SELECTOR, '#gogogo .submit'))

    def authorize(self, login, domain, password):
        self.loginInput = login
        self.domainSelect.select_option(domain)
        self.passwordInput = password
        self.loginSubmit.click()
