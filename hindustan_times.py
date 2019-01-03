from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains

import lxml.html
import pandas as pd


class HindustanTimes:
    '''
        This is the wrapper class for Hindustan times.
        In it's current implementation it scrapes the
        homepage for the news headlines.
    '''

    def __init__(self):

        self.base_url = "https://www.hindustantimes.com/"

        # top news element locators
        # this will be the box on the left inside top news container
        self.latest_news_headlines_path = "//div[contains(@class, 'latestnews-left')]/descendant::div[contains" \
                                          "(@class, 'subhead4')]//a/text()"
        # all other headlines inside top news container
        self.top_news_headlines_path = "//div[contains(@class, 'big-middlenews')]//div/*[self::h1 or self::h2]/a/text()"

        # don't miss section locators
        self.dont_miss_headlines_locator = "//div[starts-with(@class, 'col-sm-')]/div" \
                                           "[contains(@class,'dont-miss-row')]//div[@class='media-body']/div/a/text()"

        # must watch section locator
        self.must_watch_headlines_path = "//a[contains(text(), 'must watch')]/ancestor::div" \
                                         "[contains(@class,'relative') ]/following-sibling::ul//div[contains" \
                                         "(@class, 'media-body')]//div/a/text()"

        # current topic (for ex: - India vs Australia) show case locator
        self.show_case_path = "//div[contains(@class,'ipl-hm-body')]//ul/ li//*[self::div" \
                              "[contains(@class,'headingfour')] or self::div[contains(@class,'media-body')]]//a/text()"

        # editors pick section locator
        self.editors_pick = "//div[contains(@class,'editor-pick-section')]/div[contains(@class, 'row')]" \
                            "//div[contains(@ class,'headingfour')]/a/text()"

        # miscellineous news headlines
        self.miscelleniuos_headlines_path = "//div [contains(@class, 'random-content')]" \
                                            "//*[self::h3 or self::div [contains(@class,'para-txt')]]/a/text()"

        self.home_page_locators = [self.latest_news_headlines_path, self.top_news_headlines_path,
                                   self.dont_miss_headlines_locator, self.must_watch_headlines_path,
                                   self.show_case_path, self.editors_pick, self.miscelleniuos_headlines_path]

    @staticmethod
    def setup_driver():
        '''
        Setups web driver for the selenium code,
        to navigate to the URL.
        :return: web driver
        '''
        # TODO : get different project
        # path for the driver
        gecko_path = r'E:\drivers\geckodriver.exe'
        driver = webdriver.Firefox(executable_path=gecko_path)

        driver.implicitly_wait(20)
        driver.maximize_window()
        return driver

    @staticmethod
    def handle_popup(driver):
        '''
        Handles push notification pop-up.
        Declines th pop-up
        :param driver: Web driver
        '''

        # click on the popup Later
        pop_up_path = "//div[@class ='btns']/a[contains(text(),'Later')]"
        wait = WebDriverWait(driver, 15, poll_frequency=1,
                             ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,
                                                 ElementNotSelectableException])
        pop_up = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, pop_up_path)))

        actions = ActionChains(driver)
        actions.move_to_element(pop_up).click().perform()

    def scrape_home_page(self):
        '''
        Scrapes the home page of Hindustan times
        :return: extracted headlines
        '''

        driver = self.setup_driver()
        driver.get(self.base_url)

        self.handle_popup(driver=driver)

        html_source = driver.page_source
        driver.close()

        tree = lxml.html.fromstring(html_source)

        headlines = []

        for locator in self.home_page_locators:
            texts = tree.xpath(locator)
            for text in texts:
                if text.strip():
                    headlines.append(text.strip())

        return headlines


ht = HindustanTimes()
headlines = ht.scrape_home_page()

if __name__ == '__main__':
    # write to disk
    pd.DataFrame(data=headlines, columns=['headlines'])\
      .to_csv(path_or_buf='headlines.csv', index=False, encoding='utf-8')

