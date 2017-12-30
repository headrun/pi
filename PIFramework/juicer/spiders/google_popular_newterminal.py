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
import  MySQLdb
import md5
from scrapy.selector import Selector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class GooglePopularTimes(object):
    
    def __init__(self):
        self.con = MySQLdb.connect(db   = 'Popular_times', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd = 'root')
        self.cur = self.con.cursor()
        self.base_url = "https://www.google.co.in/"
        self.select_query = 'select sk,url,main_keyword,ref_url from popular_crawl limit 312,1'
	self.insert_qry = 'insert into Popular_meta(sk,program_sk,search_keyword,Name,Address,Phone,Rating,day,timings,status,processed_time, keyword_popular_times_availability,search_state,reference_url,main_url,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()' 
	self.update_query = "update popular_crawl set crawl_status=9 where sk='%s' and crawl_status=0"
        self.header_params = ['Name','Address','Phone','rating','day','timings','status','processed time']
        self.excel_file_name = 'popular_times_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
	self.main()
        
    
    def get_driver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "144.76.48.143")
        profile.set_preference("network.proxy.http_port", 3279)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile)
        self.cur.execute(self.select_query)
        data = self.cur.fetchall()
        for row in data :
            program_sk, url, main_keyword, ref_url = row
            time.sleep(2)
            driver.get(url)
            driver.wait = WebDriverWait(driver, 3)
	    time.sleep(4)
	    source_page = driver.page_source
	    sel = Selector(text=source_page)
	    time.sleep(2)
	    title = ''.join(sel.xpath('//div[contains(@id,"rhs_title")]/span/text()').extract())
	    if title:
		    no_of_searches = 'single_search'
		    rat= ''.join(sel.xpath('//div[@class="_A8k"]/div/span/text()').extract())
		    add= ''.join(sel.xpath('//div[@class="_mr kno-fb-ctx"]//span[@class="_Xbe"]/text()').extract())
		    ph= ''.join(sel.xpath('//span[@class="_Xbe _ZWk kno-fv"]/span/span/text()').extract())
		    main_nodes = sel.xpath('//div[contains(@class, "_Idv _Fdv")]')
		    if main_nodes:
		        availability='available'
	      	        for main_node in main_nodes:
	            	    time.sleep(5)
	            	    day = ''.join(main_node.xpath('./@aria-label').extract()).split('Histogram showing popular times on ')[-1].encode('utf-8')
	            	    if day:
		        	nodes = main_node.xpath('.//div[contains(@class, "_ndv")]//div[@class="lubh-bar"]')
		        	for node in nodes:
		            		time.sleep(5)
		            		times = ''.join(node.xpath('./@aria-label').extract()).split(':')[0]
					sk= md5.md5(driver.current_url+title+rat+add+times+day).hexdigest()
		            		status = ''.join(node.xpath('./@aria-label').extract()).split(':')[-1].encode('utf-8')
		            		run_time = datetime.datetime.now()
		            		values = (sk,program_sk,main_keyword,title,add,ph,rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches,url,url)
					self.cur.execute(self.insert_qry,values)
					self.cur.execute(self.update_query % program_sk)
					self.con.commit()
		    else:
			sk= md5.md5(driver.current_url+title+rat+add).hexdigest()
	    	        day,times,status='','',''
		        availability='not available'
	                run_time = datetime.datetime.now()
	                values = (sk,program_sk,main_keyword,title,add,ph,rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches,url,url)
			self.cur.execute(self.insert_qry,values)
			self.cur.execute(self.update_query % program_sk)
			self.con.commit()
			time.sleep(3)
	    else:
			link = driver.find_elements_by_xpath('//div[@class="_iPk"]/div[@class="_rl"]')[0].click()
			time.sleep(5)
			source_page = driver.page_source
			sel = Selector(text=source_page)
			no_of_searches = 'multiple_search_first_value'
			time.sleep(5)
			search_title = ''.join(sel.xpath('//div[contains(@class, "kno-ecr-pt kno-fb-ctx _nBg rhstl")]/span/text()').extract())
			search_rat = ''.join(sel.xpath('//div[@class="_A8k"]/div/span/text()').extract())
                        search_add = ''.join(sel.xpath('//div[@class="_mr kno-fb-ctx"]//span[@class="_Xbe"]/text()').extract())
			search_ph = ''.join(sel.xpath('//span[@class="_Xbe _ZWk kno-fv"]/span/span/text()').extract())
			refe_url = driver.current_url
			search_main_nodes = sel.xpath('//div[contains(@class, "_Idv _Fdv")]')
			if search_main_nodes:
			    availability='available'
			    for main_node in search_main_nodes:
				time.sleep(5)
				day = ''.join(main_node.xpath('./@aria-label').extract()).split('Histogram showing popular times on ')[-1].encode('utf-8')
				if day:
				    nodes = main_node.xpath('.//div[contains(@class, "_ndv")]//div[@class="lubh-bar"]')
				    for node in nodes:
					time.sleep(5)
					times = ''.join(node.xpath('./@aria-label').extract()).split(':')[0]
					sk= md5.md5(driver.current_url+search_title+search_rat+search_add+times+day).hexdigest()
					status = ''.join(node.xpath('./@aria-label').extract()).split(':')[-1].encode('utf-8')
					run_time = datetime.datetime.now()
					values = (sk,program_sk,main_keyword,search_title,search_add,search_ph,search_rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches,refe_url,url)
					self.cur.execute(self.insert_qry,values)		
					self.cur.execute(self.update_query % program_sk)
					self.con.commit()
					time.sleep(2)
		        else:	
			    sk= md5.md5(driver.current_url+search_title+search_rat+search_add).hexdigest()
			    day,times,status='','',''
			    availability='not available'
			    run_time = datetime.datetime.now()
			    values = (sk,program_sk,main_keyword,search_title,search_add,search_ph,search_rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches,refe_url,url)
			    self.cur.execute(self.insert_qry,values)
                            self.cur.execute(self.update_query % program_sk)
                            self.con.commit()
			    time.sleep(3)
	driver.close()		
    def main(self):
        driver = self.get_driver() 

if __name__ == "__main__":
    GooglePopularTimes()
