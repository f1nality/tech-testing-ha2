# encoding: utf-8
import os
import unittest
from selenium import webdriver
from tests.lib.pages import AdCreatePage, LoginPage


class TargetMailRuTestCase(unittest.TestCase):
    def setUp(self):
        self.login = 'tech-testing-ha2-13'
        self.domain = '@bk.ru'
        self.password = os.environ['TTHA2PASSWORD']

        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(webdriver.DesiredCapabilities, browser).copy()
        )

        self.__authorize()

    def __authorize(self):
        login_page = LoginPage(self.driver)
        login_page.authorize(self.login, self.domain, self.password)

    def __get_ad_create_page_image_path(self):
        project_dir = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(project_dir, 'resources', 'image.png')

        return image_path

    def test_authorization(self):
        ad_create_page = AdCreatePage(self.driver)

        assert ad_create_page.is_authorized(self.login, self.domain)

    def fill_ad_create_page_banner_info(self, ad_create_page):
        ad_create_page.campaign_name.clear()
        ad_create_page.campaign_name = 'Campaign!'
        ad_create_page.banner_title = 'Title'
        ad_create_page.banner_text = 'Text text text'
        ad_create_page.banner_url = 'www.example.com'

        ad_create_page.banner_image = self.__get_ad_create_page_image_path()

    def test_ad_create_page_banner_image_uploading(self):
        ad_create_page = AdCreatePage(self.driver)

        self.fill_ad_create_page_banner_info(ad_create_page)

        assert ad_create_page.banner_image_preview_display == 'block'

    def test_ad_create_page(self):
        ad_create_page = AdCreatePage(self.driver)

        self.fill_ad_create_page_banner_info(ad_create_page)

        ad_create_page.target_restrict_switch.click()
        ad_create_page.target_restrict_item_12.click()

        assert ad_create_page.target_restrict_switch.text() == '12+'

        ad_create_page.target_restrict_switch.click()

        assert ad_create_page.target_restrict_switch.text() == '12+'

        ad_create_page.deselect_all_target_region_chosen()

        chosen_regions = ad_create_page.get_target_region_chosen()

        assert len(chosen_regions) == 0

        region = ad_create_page.get_target_region_by_name(u'Европа')
        region.click()

        chosen_regions = ad_create_page.get_target_region_chosen()

        assert len(chosen_regions) == 1
        assert chosen_regions[0] == u'Европа'