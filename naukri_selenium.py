# -*- coding: utf-8 -*-
"""
@author: Vivek
"""
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class NaukriSelenium:
    
#    def __init__(self, link, email_path, phone_path):
#        self.link = link
#        self.email_path = email_path
#        self.phone_path = phone_path
    
    
    def set_up(self):
        ''' This functions prepares te webdriver for use
            
            @returns preped web driver
        '''
        # provide firefox path
        binary = FirefoxBinary(r"C:\Users\Vivek\Desktop\firefox-sdk\bin\firefox.exe")
        
        # stop indefinate page load
        fp = webdriver.FirefoxProfile()
        
        fp.set_preference('webdriver.load.strategy', 'unstable')
        fp.set_preference("http.response.timeout", 10)
        fp.set_preference("dom.max_script_run_time", 10)
        
        fp.set_preference("browser.startup.homepage","")
        
        # initialize driver
        driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=fp)
        
        driver.implicitly_wait(15)
    
        return driver

#
#    def clean_up(self, driver):
#        driver.close()
        
        
    def crawl(self, link, email_path, phone_path):
        '''
            This function returns 
        '''
        email = None
        phone = None
        
        driver = self.set_up()
        
        driver.get(link)
        try:
            # hit enter on view details
            driver.find_element_by_xpath("//a[@id='viewCont_trg']").send_keys(Keys.RETURN)
            try:
                email = driver.find_element_by_xpath(email_path).get_attribute('title')
            except Exception:
                ""
            
            try:
                phone = driver.find_element_by_xpath(phone_path).text
            except Exception:
                ""
                
        except Exception:
            ""
        
        finally:
            #self.clean_up(driver)
            driver.close()
            return (email, phone)
    
    
#sel = NaukriSelenium( )
#email, phone = sel.crawl(link="https://www.naukri.com/job-listings-Microsoft-Biztalk-Server-Developer-Bengaluru-Enkay-Technology-Solutions-Bengaluru-2-to-7-years-190817000029?src=jobsearchDesk&sid=15374683669611&xp=7&px=1&qp=&srcPage=s",
#                     email_path= "//div[@id='viewContact']/p/em[contains(text(), 'Email Address:')]/following-sibling::span[1]/img",
#                     phone_path= "//div[@id='viewContact']/p/em[contains(text(), 'Telephone:')]/following-sibling::span[1]"
#                  )
#
#
#print(email, phone)