# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import datetime
import csv
import md5
import  MySQLdb
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy.selector import Selector



class GooglePopular(object):
    
    def __init__(self):
	self.header_params = ['Name','Address','Phone','rating','day','timings','status','processed time']
        self.excel_file_name = 'popular_times_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
	self.con = MySQLdb.connect(db   = 'Popular_times', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.insert_query = 'insert into popular_crawl(sk, url, crawl_status, main_keyword, ref_url,created_at, modified_at)values(%s,%s, %s, %s,  %s, now(), now()) on duplicate key update modified_at = now()'
	self.base_url = "https://www.google.co.in/"
	self.main()
        
    def get_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "144.76.48.146")
        profile.set_preference("network.proxy.http_port", 3279)
        profile.update_preferences()
        driver = webdriver.Firefox(profile)
	time.sleep(4)
        driver.get(self.base_url + "/")
        driver.find_element_by_id("lst-ib").clear()
        time.sleep(3)
	with open('hospitals_chennai_popular_times1.txt', 'r') as f: rows = f.readlines()
	counter = 0
        for row in rows:
                time.sleep(2)
                counter += 1
		i = row.replace('\r\n','')
		driver.find_element_by_id("lst-ib").clear()
		driver.wait = WebDriverWait(driver, 3)
        	driver.find_element_by_id("lst-ib").send_keys(i)
		time.sleep(3)
		ref_url = driver.current_url
		sk = md5.md5(driver.current_url).hexdigest()
		vals = (sk,str(driver.current_url),0,str(i),str(ref_url))
		self.cur.execute(self.insert_query,vals)
		self.con.commit()
			
 
   
    def main(self):
        driver = self.get_driver()


if __name__ == "__main__":
    GooglePopular()
