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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class GooglePopular(object):
    
    def __init__(self):
	self.con = MySQLdb.connect(db   = 'Baby_Names',host = 'localhost', charset="utf8", use_unicode=True,user = 'root', passwd ='root')
        self.cur = self.con.cursor()
	self.base_url = "https://www.google.co.in/"
	self.select_query = "select sk,url,meta_data from baby_crawl where crawl_status=0"
	self.insert_query = "insert into baby_names(sk,name,gender,similar_names,meaning_name,popularity,name_usage,origin_usage,famous_names,reference_url,main_url,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now(),reference_url=%s,origin_usage=%s"
	self.update_query = 'update baby_crawl set crawl_status=1 where crawl_status=0 and url="%s"'
	self.main()
        
    def get_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "138.0.152.164")
        profile.set_preference("network.proxy.http_port", 3128)
        profile.update_preferences()
	driver = webdriver.Firefox(firefox_profile=profile)
	self.cur.execute(self.select_query)
	data = self.cur.fetchall()
	counter=0
	for row in data :
		sk,url,meta_data = row
		ref_url = meta_data.replace("{'ref_url': '",'').replace("'}",'')
                time.sleep(2)
		driver.get(url)
		driver.wait = WebDriverWait(driver, 3)
		time.sleep(2)
		source_page = driver.page_source
		sel = Selector(text=source_page)	
		time.sleep(2)
		name = sel.xpath('//section[main(@class, "single left")]//table//tr//td/b[contains(text(),"Name:")]/../../td/text()').extract()
		gender = sel.xpath('//main[contains(@class, "single left")]//table//tr//td/b[contains(text(),"Gender:")]/../../td/text()').extract()
		names_similar = '<>'.join(sel.xpath('//div[contains(text(),"Names Similar")]/../div/a/text()').extract())
		meaning_name = ''.join(sel.xpath('//div/b[contains(text(),"Meaning of")]/..//following-sibling::div/div/text()').extract()).replace('; ','<>')
		popularity = sel.xpath('//main[contains(@class, "single left")]//table//tr//td/s/text()').extract()
		origin = '<>'.join(sel.xpath('//div/b[contains(text(),"Origin / Tag / Usage")]/..//following-sibling::div/div/ul/li/em/i[not(contains(@style,"width:0%"))]/../../a/text()').extract())
		origin1 = '<>'.join(sel.xpath('//div/b[contains(text(),"Origin / Tag / Usage")]/..//following-sibling::div/div/ul/li/a/text()').extract())
		famous_pe,famous_people=[],[]
		nodes = sel.xpath('//div[@class="celeb"]/div')
		for node in nodes:
			ra=node.xpath('./div/text()').extract()
			famous_pe.append(ra)
		for fa in famous_pe:
			people = ','.join(fa)
			famous_people.append(people)
		famous_names='<>'.join(famous_people)
		if name and sk:
			values = (''.join(sk),''.join(name),''.join(gender),''.join(names_similar),''.join(meaning_name),''.join(popularity),''.join(origin),''.join(origin1),''.join(famous_names),''.join(url),''.join(ref_url),''.join(url),''.join(origin1))
			counter +=1
			self.cur.execute(self.insert_query,values)
			self.cur.execute(self.update_query % ''.join(url))
			self.con.commit()
	driver.quit()

    def main(self):
        driver = self.get_driver()


if __name__ == "__main__":
    GooglePopular()
