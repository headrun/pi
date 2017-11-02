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
        self.header_params = ['Name','Address','Phone','rating','timings','status']
        self.excel_file_name = 'popular_times.csv'
        oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
        
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(50)
        self.base_url = "https://www.google.co.in/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_google_popular2(self):
        driver = self.driver
	time.sleep(15)
        driver.get(self.base_url + "/")
        driver.find_element_by_id("lst-ib").clear()
        driver.find_element_by_id("lst-ib").send_keys("Apollo Speciality Cancer Hospital")
	time.sleep(20)
        driver.find_element_by_css_selector("div.sbqs_c").click()
	time.sleep(5)
        title = driver.find_element_by_xpath('//*[@id="rhs_title"]/span').text
        address = driver.find_element_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div/div/span[2]').text
	time.sleep(5)
        phone = driver.find_element_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/div[2]/div[2]/div/div[4]/div/div/span[2]/span/span').text
        rating = driver.find_element_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/div/span[1]').text
	time.sleep(5)
        list1=['4','5','6','7','8','9','10','11']
        list3 = ['9-10','10-11','11-12','12-1','1-2','2-3','3-4','4-5']
        list2 = []
        for i in list1:
	    time.sleep(25)
            height = driver.find_element_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/div[2]/div[4]/div/div[3]/div[3]/div[2]/div[1]/div[%s]'%i).get_attribute("style")
            hei = ''.join(height.split(':')[-1]).strip('px;').strip()
            list2.append(hei)
        for j,m in zip(list3,list2):
            if m >= '60':
                he_value = j
                status = 'Usually as busy as it gets'
            elif m < '60':
                he_value = j
                status = 'Usually a little busy'
            
            values=[title,address,phone,rating,he_value,status]
            self.todays_excel_file.writerow(values)
            
            
    
    '''def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True'''
    
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
