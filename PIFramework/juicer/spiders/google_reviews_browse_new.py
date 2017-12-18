from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import csv
import md5
import datetime
from scrapy.selector import Selector
import  MySQLdb
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from input_file import keyword

class GoogleReviews(object):

    def __init__(self):
        self.con = MySQLdb.connect(db   = 'urlqueue_dev', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='hdrn59!')
        self.cur = self.con.cursor()
        self.insert_query = 'insert into reviews_crawl(sk, url, crawl_status, main_keyword, sub_keyword, ref_url, created_at, modified_at)values(%s, %s, %s, %s,  %s, %s, now(), now()) on duplicate key update modified_at = now()'

        self.base_url = "https://www.google.co.in/"
        self.header_params = ['Processed Timestamp','keyword','reviewed_by', 'Review_text','Review_Star_Rating','Rating','No_of_Reviews','Time']
 
    def get_driver(self):
        profile = webdriver.FirefoxProfile() 
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "144.76.48.143")
        profile.set_preference("network.proxy.http_port", 3279)
        profile.update_preferences() 
        driver = webdriver.Firefox(profile)
        driver.get(self.base_url + "/maps/@12.9291104,77.6249622,15z")
	time.sleep(2)
        driver.get(self.base_url + "/maps/")
        driver.wait = WebDriverWait(driver, 5)
        driver.find_element_by_id("searchboxinput").clear()
        with open('input_file1.txt', 'r') as f: rows = f.readlines()
	counter = 0
        for row in rows:
	    counter += 1
            i = row.replace('\r\n','')
            driver.find_element_by_id("searchboxinput").clear()
            driver.find_element_by_id("searchboxinput").send_keys(i)
            time.sleep(4)
            driver.find_element_by_id("searchbox-searchbutton").click()
            time.sleep(2)
	    source_page = driver.page_source
	    sel = Selector(text=source_page)
            ref_url = driver.current_url
	    idx_lst = sel.xpath('//div[@class="section-result"]//@data-result-index').extract()
            if idx_lst :
		    for idx in idx_lst:
			driver.find_element_by_xpath('//div[@data-result-index=%s]'%int(idx)).click()
                        time.sleep(6)
			sk =  md5.md5(driver.current_url).hexdigest()
                        sub_keyword = driver.current_url.split('/')[5].replace('+',' ')
			vals = (sk,str(driver.current_url),100,str(i),str(sub_keyword),str(ref_url))
			self.cur.execute(self.insert_query,vals)
                        self.con.commit()
			try:
				driver.find_element_by_xpath('//button[@class="section-back-to-list-button blue-link noprint"]').click()
			except:
				pass
			time.sleep(6)
		    driver.get(self.base_url + "/maps/@12.9291104,77.6249622,15z")
                    time.sleep(4)
            else :
                sk =  md5.md5(driver.current_url).hexdigest()
                vals = (sk,str(driver.current_url),100,i,'',str(ref_url))
                self.cur.execute(self.insert_query,vals)
                self.con.commit()


    def main(self):
        driver = self.get_driver()

if __name__ == "__main__":
     GoogleReviews().main()
