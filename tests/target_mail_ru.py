# encoding: utf-8
import os
import unittest
from selenium import webdriver
from tests.lib.pages import AdCreatePage, LoginPage, AdsCampaignsPage, AdEditPage


class TargetMailRuTestCase(unittest.TestCase):
    def setUp(self):
        self.login = 'tech-testing-ha2-13'
        self.domain = '@bk.ru'
        self.password = os.environ['TTHA2PASSWORD']

        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

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

    def __fill_ad_create_page_banner_info(self, ad_create_page):
        ad_create_page.campaign_name.clear()
        ad_create_page.campaign_name = 'Campaign!'
        ad_create_page.banner_title = 'Title'
        ad_create_page.banner_text = 'Text text text'
        ad_create_page.banner_url = 'www.example.com'

        ad_create_page.banner_image = self.__get_ad_create_page_image_path()

    def test_ad_create_page_banner_image_uploading(self):
        ad_create_page = AdCreatePage(self.driver)

        self.__fill_ad_create_page_banner_info(ad_create_page)

        assert ad_create_page.banner_image_preview_display == 'block'

    def __fill_ad_create_page_target_restrict(self, ad_create_page, value):
        ad_create_page.target_restrict_switch.click()
        ad_create_page.get_target_restrict_by_value(value).click()

    def __clean_up_last_ad_campaign(self, ad_campaigns_page):
        ad_campaigns_page.delete_first_campaign_button.click()

    def test_ad_create_page_do_not_fill_restrict_and_region(self):
        ad_create_page = AdCreatePage(self.driver)

        self.__fill_ad_create_page_banner_info(ad_create_page)

        default_target_region = ad_create_page.get_target_region_chosen()

        ad_create_page.submit_button.click()

        ad_campaigns_page = AdsCampaignsPage(self.driver, force_load=False)
        ad_campaigns_page.edit_first_campaign_button.click()

        ad_edit_page = AdEditPage(self.driver, force_load=False)

        assert ad_edit_page.target_restrict_switch.text() == u'Не учитывать'
        assert ad_edit_page.get_target_region_chosen() == default_target_region

        self.driver.back()
        self.__clean_up_last_ad_campaign(ad_campaigns_page)

    def test_ad_create_page_fill_restrict_and_region(self):
        target_restrict_value = '12+'
        target_region_value = u'Европа'

        ad_create_page = AdCreatePage(self.driver)

        self.__fill_ad_create_page_banner_info(ad_create_page)
        self.__fill_ad_create_page_target_restrict(ad_create_page, target_restrict_value)

        ad_create_page.deselect_all_target_region_chosen()
        region = ad_create_page.get_target_region_by_name(target_region_value)
        region.click()

        assert ad_create_page.target_restrict_switch.text() == target_restrict_value
        assert ad_create_page.get_target_region_chosen() == [target_region_value]

        ad_create_page.submit_button.click()

        ad_campaigns_page = AdsCampaignsPage(self.driver, force_load=False)
        ad_campaigns_page.edit_first_campaign_button.click()

        ad_edit_page = AdEditPage(self.driver, force_load=False)

        assert ad_edit_page.target_restrict_switch.text() == target_restrict_value
        assert ad_edit_page.get_target_region_chosen() == [target_region_value]

        self.driver.back()
        self.__clean_up_last_ad_campaign(ad_campaigns_page)

    def test_ad_create_page_fill_restrict_and_region_with_suggester(self):
        target_restrict_value = '0+'
        target_region_value = u'Европа'

        ad_create_page = AdCreatePage(self.driver)

        self.__fill_ad_create_page_banner_info(ad_create_page)
        self.__fill_ad_create_page_target_restrict(ad_create_page, target_restrict_value)

        ad_create_page.deselect_all_target_region_chosen()
        ad_create_page.target_region_suggester = target_region_value + '\n'

        assert ad_create_page.target_restrict_switch.text() == target_restrict_value
        assert ad_create_page.get_target_region_chosen() == [target_region_value]

        ad_create_page.submit_button.click()

        ad_campaigns_page = AdsCampaignsPage(self.driver, force_load=False)
        ad_campaigns_page.edit_first_campaign_button.click()

        ad_edit_page = AdEditPage(self.driver, force_load=False)

        assert ad_edit_page.target_restrict_switch.text() == target_restrict_value
        assert ad_edit_page.get_target_region_chosen() == [target_region_value]

        self.driver.back()
        self.__clean_up_last_ad_campaign(ad_campaigns_page)