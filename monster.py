# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 23:34:56 2018

@author: Vivek
"""
# disable popup
    #fp = webdriver.FirefoxProfile(r'C:\Users\Vivek\AppData\Roaming\Mozilla\Firefox\Profiles\f49tsxfy.default')
    #fp.set_preference('dom.disable_beforeunload', True)






from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

import pandas as pd
import datetime
from dateutil.parser import parse


def set_up():
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
    
    driver.implicitly_wait(10)
    
    return driver


# get the ready to use web driver
driver = set_up()

# navigate to url
driver.get('https://www.monsterindia.com')#/jobs-in-bangalore.html')

# Enter job search location
driver.find_element_by_xpath("//input[@id='lmy']").send_keys('Bangalore')
# click on search
driver.find_element_by_xpath("//input[contains(@value, 'Search')]").send_keys(Keys.RETURN)

# no of days to collect data
# collect data for 10 days
# notified by end day
today = today = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d")
end_day = today + datetime.timedelta(days=10)

# get the job elements
elements = driver.find_elements_by_xpath("//li//div[contains(@class, 'jobwrap')]")
for i in range(len(elements)):
    print('Elememt : %d' %(i+1))
    
    # Step 1: look for date 
    date = elements[i].find_element_by_xpath("//div[contains(@ class, 'job_optitem ico7')]").text.split(':')[1].strip()
    
    
    job = elements[i].find_element_by_xpath("//a[@class='title_in']")
    job_title = job.get_attribute('title').strip()
    job_link = job.get_attribute('href').strip()
    exp = elements[i].find_element_by_xpath("//div[@class='jtxt jico ico2']/span").text.strip()

    print(date)
    print(job_title)
    print(job_link)
    print(exp)
    
    print('-------------------------------')

    
#print(date.get_attribute('text'))

driver.close()