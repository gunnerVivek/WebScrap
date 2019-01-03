# -*- coding: utf-8 -*-
"""
@author: Vivek
"""

import requests
import lxml.html
import datetime
from dateutil.parser import parse
import pandas as pd
import re

import definations

class MonsterScrapper:
    '''
        defines methods needed to scrape data from monsterindia.com
        
    '''
    
    def __init__(self, days):
        '''
            initializes the class variables
            @parameter - no of days for which data is scraped
        '''
        self.days = days
        self.today = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d")
        self.end_day = self.today + datetime.timedelta(days=self.days)
        self.phone_pattern = re.compile(r'\d{10}')
        self.email_pattern = re.compile(r'\S+@\S+')
        self.salary_pattern = re.compile(r'\d*\s?[-]?\d+[.]?\d+\s?[lL][pP][aA]')
    
    
#    today = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d")
#    end_day = today + datetime.timedelta(days=5)
#    
#    df =  pd.DataFrame(columns=['job_src_link', 'source', 'exp_range','job_type'])
    
    def scrape_landing(self):
        '''
            This method takes care of first phase of scrapeing 
            @returns - a df with part of the information
        '''
        
        df = pd.DataFrame(columns=['job_src_link', 'source', 'exp_range','job_type'])
        base_url = 'https://www.monsterindia.com/jobs-in-bangalore'#.html
        go_next_page = True
        page_no = 1
        while(go_next_page):
            # todo -- look for status
            if page_no == 1:
                html_content = requests.get(base_url+'.html')
            else:
                html_content = requests.get(base_url + '-' +str(page_no)+'.html')    # www.monsterindia.com/jobs-in-bangalore-2.html
            
            doc = lxml.html.fromstring(html_content.content)
            
            job_items  = doc.xpath("//li//div[contains(@class, 'jobwrap')]")
            #title = doc.xpath("//div [@class='jtxt jico ico2']/span/text()")
            for i in range(len(job_items)):
                job = job_items[i]
                
                date = job.xpath("string(.//div[contains(@ class, 'job_optitem ico7')]/text())").split(':')[1].strip()
                date = parse(date)
                if date > self.end_day:
                    # break whil loop
                    go_next_page = False
                    # break for loop
                    break
                link = job.xpath("string(.//a[@class='title_in']/@href)")
                title = job.xpath("string(.//a[@class='title_in']/@title)")
                exp = job.xpath("string(.//div [@class='jtxt jico ico2']/span/text())")#.text_content()
                job_type = 'part time' if 'part time' in title.lower() else 'full time'
                source = 'Monster'
                df.loc[df.shape[0]] = [link, source, exp, job_type]
                
            #print(page_no)
            page_no+=1
        
        return df
    
    
    def find_phone(self, description):
        '''
            Finds a phone number in a given text
        '''
        
        ls = []
        for des in description:
            found = self.phone_pattern.search(des)
            if (found):
                ls.append(found[0])
                
        return ', '.join(ls)
    
    
    def find_email(self, description):
        '''
            Finds an email in a given text
        '''
        
        ls = []
        for des in description:
            found = self.email_pattern.search(des)
            if (found):
                ls.append(found[0])
                
        return ', '.join(ls)
    
    
    def find_salary(self, description):
        '''
            Finds salary in a given text
        '''
        
        ls = []
        for des in description:
            found = self.salary_pattern.search(des)
            if (found):
                ls.append(found[0])
                
        return ', '.join(ls)
    
    
    def scrape_inner(self, outer):
        
       '''
            Scrapes the rest of the data
            Follows links collected from the first pass
            
            @returns - complete data
       ''' 
       
       # add the rest of the columns 
       cols = ['sector','skills_kw', 'salary', 'job_role', 'description', 'email', 'phone', 'education']
       outer = pd.concat([outer, pd.DataFrame(columns=cols)])
       
       for i in range(0, outer.shape[0]):
            link = outer.loc[i, 'job_src_link']
            html = requests.get('https:'+link)
            
            html_content = lxml.html.fromstring(html.content)
            
            skills = html_content.xpath("//div[contains(@class,'key_skills')]//a[contains(@class, 'keylink lft')]/text()")
            skills_kw = ', '.join(skills)
            outer.loc[i, 'skills_kw'] = skills_kw
            #print(skill_kw)
            
            job_role = html_content.xpath("//div[@class='col-md-3 col-xs-12 pull-right jd_rol_section']/div[contains(text(), 'Role')]/following-sibling::span[1]/a/text()")
            job_role = ', '.join(job_role)
            outer.loc[i, 'job_role'] = job_role
            #print(job_role)
            
            sector = html_content.xpath("//div[@class='col-md-3 col-xs-12 pull-right jd_rol_section']/div[contains(text(), 'Industry')]/following-sibling::span[1]/a/text()")
            sector = ', '.join(sector)
            outer.loc[i, 'sector'] = sector
            #print(sector)
            
            description = html_content.xpath("//div[contains(@class, 'col-md-9 col-xs-12 pull-left')]/div[contains(@class, 'job_description')]/div [contains(@class,'desc')]/descendant-or-self::*/text()")
            outer.loc[i, 'description'] = description
            #print(description)
            
            education = html_content.xpath("//div[@class='col-md-3 col-xs-12 pull-right jd_rol_section']/div[contains(text(), 'Education')]/following-sibling::span[1]/text()")
            education = ''.join(education)
            outer.loc[i, 'education'] = education
            #print(education)
            
            phone_number = self.find_phone(description)
            outer.loc[i, 'phone'] = phone_number
            #print(phone_number)
            
            email = self.find_email(description)
            outer.loc[i, 'email'] = email
            #print(email)
            
            salary = html_content.xpath("//div[@class='col-md-3 col-xs-12 pull-right jd_rol_section']/div[contains(text(), 'Salary')]/following-sibling::span[1]/text()")
            if not salary:
                salary = self.find_salary(description)
            outer.loc[i, 'salary'] = salary 
       
       # order the columns as needed
       order_of_cols = ['job_src_link', 'source', 'job_type', 'sector', 'skills_kw', 'exp_range', 'salary', 'job_role', 'description', 'email', 'phone', 'education']
       outer = outer[order_of_cols]
       
       return outer
   
    
    def scrape(self):
        '''
            Calls the two inner scrapinf functions
            
            @returns - data scraped from monster
        '''
        
        outer = self.scrape_landing()
        monster_data = self.scrape_inner(outer)
        
        return monster_data



if __name__ == '__main__':
    
    # create object
    monster = MonsterScrapper(5)
    # call the scraper
    monster_data = monster.scrape()
    
    # write the data to the disk
    monster_data.to_csv(definations.ROOT_DIR+'\..\\output\\monster_test.csv', index=False)