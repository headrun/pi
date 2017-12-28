# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import datetime
import csv



class GooglePopular2(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(GooglePopular2, self).__init__(*args, **kwargs)
        self.header_params = ['Name','Address','Phone','rating','day','timings','status','processed time','keyword_popular_times_availability','no_of_search']
        self.excel_file_name = 'popular_times_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
        
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "https://www.google.co.in/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_google_popular2(self):
        driver = self.driver
	time.sleep(4)
        driver.get(self.base_url + "/")
        driver.find_element_by_id("lst-ib").clear()
        time.sleep(3)
	with open('hospitals_chennai_popular_times.txt', 'r') as f: rows = f.readlines()
	counter = 0
        for row in rows:
                time.sleep(2)
                counter += 1
		i = row.replace('\r\n','')
        	driver.find_element_by_id("lst-ib").send_keys(i)
		time.sleep(3)
        	#driver.find_element_by_css_selector("div.sbqs_c").click()
		time.sleep(4)
		try:
		    title = driver.find_element_by_xpath('//div[contains(@class, "kno-ecr-pt kno-fb-ctx _hdf rhstl")]').text
		    no_of_searches = 'single_search'
		    rat= driver.find_element_by_xpath('//div[@class="_A8k"]/div/span').text
		    add= driver.find_element_by_xpath('//div[@class="_mr kno-fb-ctx"]//span[@class="_Xbe"]').text
		    ph= driver.find_element_by_xpath('//span[@class="_Xbe _ZWk kno-fv"]/span/span').text
		    main_nodes = driver.find_elements_by_xpath('//div[contains(@class, "_Idv _Fdv")]')
		    if main_nodes:
		        availability='available'
	      	        for main_node in main_nodes:
	            	    time.sleep(5)
	            	    day = main_node.get_attribute('aria-label').split('Histogram showing popular times on ')[-1].encode('utf-8')
	            	    if day:
		        	nodes = main_node.find_elements_by_xpath('.//div[contains(@class, "_ndv")]//div[@class="lubh-bar"]')
		        	for node in nodes:
		            		time.sleep(5)
		            		times = node.get_attribute('aria-label').split(':')[0]
		            		status = node.get_attribute('aria-label').split(':')[-1].encode('utf-8')
		            		run_time = datetime.datetime.now()
		            		values = [title,add,ph,rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches]
		            		self.todays_excel_file.writerow(values)
		    else:
	    	        day,times,status='','',''
		        availability='not available'
	                run_time = datetime.datetime.now()
	                values = [title,add,ph,rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches]
	                self.todays_excel_file.writerow(values)
			time.sleep(3)
		except:
			link = driver.find_elements_by_xpath('//div[@class="_iPk"]/div[@class="_rl"]')[0].click()
			no_of_searches = 'multiple_search_first_value'
			time.sleep(5)
			search_title = driver.find_element_by_xpath('//div[contains(@class, "kno-ecr-pt kno-fb-ctx _nBg rhstl")]').text
			search_rat = driver.find_element_by_xpath('//div[@class="_A8k"]/div/span').text
                        search_add = driver.find_element_by_xpath('//div[@class="_mr kno-fb-ctx"]//span[@class="_Xbe"]').text
			search_ph = driver.find_element_by_xpath('//span[@class="_Xbe _ZWk kno-fv"]/span/span').text
			search_main_nodes = driver.find_elements_by_xpath('//div[contains(@class, "_Idv _Fdv")]')
			if search_main_nodes:
			    availability='available'
			    for main_node in main_nodes:
				time.sleep(5)
				day = main_node.get_attribute('aria-label').split('Histogram showing popular times on ')[-1].encode('utf-8')
				if day:
				    nodes = main_node.find_elements_by_xpath('.//div[contains(@class, "_ndv")]//div[@class="lubh-bar"]')
				    for node in nodes:
					time.sleep(5)
					times = node.get_attribute('aria-label').split(':')[0]
					status = node.get_attribute('aria-label').split(':')[-1].encode('utf-8')
					run_time = datetime.datetime.now()
					values = [search_title,search_add,search_ph,search_rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches]
					self.todays_excel_file.writerow(values)
					time.sleep(2)
		        else:	
			    day,times,status='','',''
			    availability='not available'
			    run_time = datetime.datetime.now()
			    values = [search_title,search_add,search_ph,search_rat.replace(',','.'),day,times,status,run_time,availability,no_of_searches]
			    self.todays_excel_file.writerow(values)
			    time.sleep(3)
			
 
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
