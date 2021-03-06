# -*- coding: utf-8 -*-
"""
@author: Vivek
"""

import requests
import lxml.html

import pandas as pd
import time 
import random

#from scrapers import naukri_selenium
import definations

class NaukriScraper:
    '''
        defines methods neede to scrape data from Naukri.com
    '''
    
    def __init__(self):
        self.df = pd.DataFrame(columns=['job_src_link', 'source', 'job_type', 'sector', 'skills_kw', 'exp_range', 'salary', 'job_role', 'description', 'email', 'phone', 'education'])
        
    def scrape(self, no_pages):
        
        base_url = 'https://www.naukri.com/jobs-in-bangalore'
        
        #df = pd.DataFrame(columns=['job_src_link', 'source', 'job_type', 'sector', 'skills_kw', 'exp_range', 'salary', 'job_role', 'description', 'email', 'phone', 'education'])
        # xpath for email
        #email_path = "//div[@id='viewContact']/p/em[contains(text(), 'Email Address:')]/following-sibling::span[1]/img"#/@title
        # xpath for phone
        #phone_path = "//div[@id='viewContact']/p/em[contains(text(), 'Telephone:')]/following-sibling::span[1]"#/text()
    
        # this will separate multiple values of same field
        element_separator = ', '
        
        page_no = 1
        
        while(page_no <= no_pages):
            
            if page_no == 1:
                # navigate to outer page
                outer_html = requests.get(base_url)
            else:
                # navigate to outer page
                outer_html = requests.get(base_url+'-'+page_no)
            # get contents of the outer page
            outer_html_content = lxml.html.fromstring(outer_html.content)
            
            # get all the listings from the outer page
            job_items = outer_html_content.xpath("//a[contains(@class,'content')]")            
            
            # iterate each job item
            for i in range(0, len(job_items)):
                
                # row to insert
                df_row = self.df.shape[0]
                
                job = job_items[i]
                
                link = job.xpath(".//@href")
                link = ''.join(link)
                #df.loc[df_row, 'job_src_link'] = link
                
                src = 'Naukri'
                #self.df.loc[df_row, 'source'] = src
                
                title = job.xpath(".//ul[1]/li[1]/@title")
                title = element_separator.join(title)
                job_type = 'part time' if 'part time' in title.lower() else 'full time'
                #df.loc[df_row, 'job_type'] = job_type
                
                experience = job.xpath(".//span[contains(@class,'exp')]/text()")
                experience = element_separator.join(experience)
                #df.loc[df_row, 'exp_range'] = experience
                
                ##################################################
                #                                                #
                # from here content from the links are collected #
                #                                                #
                ##################################################
                
                # follow the link to the particular job page
                inner_html = requests.get(link)
                inner_html_content = lxml.html.fromstring(inner_html.content)
                
                sector = inner_html_content.xpath("//div[@class='jDisc mt20']/p/em[contains(text(),'Industry')]/following-sibling::span/a/text()")
                sector = element_separator.join(sector)
                #df.loc[df_row, 'sector'] = sector
                
                skills_kw = inner_html_content.xpath("//div[contains(@class,'ksTags')]/descendant:: font[contains(@class,'hlite')]/text()")
                skills_kw = element_separator.join(skills_kw)
                #df.loc[df_row, 'skills_kw'] = skills_kw
                
                salary = inner_html_content.xpath("//span[@class='sal']/text()")
                salary = element_separator.join(salary)
                #df.loc[df_row, 'salary'] = salary
                
                job_role = inner_html_content.xpath("//div[@class='jDisc mt20']/p/em[contains(text(),'Role:')]/following-sibling::span/text()")
                job_role = element_separator.join(job_role)
                #df.loc[df_row, 'job_role'] = job_role
                
                description = inner_html_content.xpath("//div[@class='JD']/ul[@class='listing mt10 wb']/text()")
                description = element_separator.join(description)
                #df.loc[df_row, 'description'] =  description
                
                education = inner_html_content.xpath("//div[@class='jDisc mt10 edu']/p/span/text()")
                education = element_separator.join(education)
                #df.loc[df_row, 'education'] = education
                
                # use selenium
                #selenium = naukri_selenium.NaukriSelenium()
                
                #email, phone = selenium.crawl(link=link, email_path=email_path, phone_path=phone_path)
                
                self.df.loc[df_row, 'job_src_link'] = link
                self.df.loc[df_row, 'source'] = src
                self.df.loc[df_row, 'job_type'] = job_type
                self.df.loc[df_row, 'exp_range'] = experience
                self.df.loc[df_row, 'sector'] = sector
                self.df.loc[df_row, 'skills_kw'] = skills_kw
                self.df.loc[df_row, 'salary'] = salary
                self.df.loc[df_row, 'job_role'] = job_role
                self.df.loc[df_row, 'description'] =  description
                self.df.loc[df_row, 'education'] = education
                #df.loc[df_row, 'email'] = email
                #df.loc[df_row, 'phone'] = phone
        
        # wait randomly between 5 and 15 seconds
        time.sleep(random.randint(5, 15))
        # increment page number
        print(page_no)
        page_no+=1
        
        return self.df
    

if __name__ == '__main__':
    
    naukri = NaukriScraper()

    naukri_data = naukri.scrape(no_pages=10)

    naukri_data.to_csv(definations.ROOT_DIR+'\..\\output\\naukri.csv', index=False)

            
            
        
        
       