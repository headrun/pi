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

class GoogleReviewsTerminaln(object):

    def __init__(self):
        
        self.con = MySQLdb.connect(db   = 'urlqueue_dev', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd = 'hdrn59!')
        self.cur = self.con.cursor()
        self.base_url = "https://www.google.co.in/"
        self.header_params = ['Main_keyword','Sub_keyword','reviewed_by', 'Review_text','Review_Star_Rating','Rating','No_of_Reviews','Time','reference_url', 'main_url', 'status']
        self.insert_qry2 = 'insert into Reviews_meta(sk, program_sk, main_keyword, sub_keyword, reviewed_by, Review_text, Review_Star_Rating, Rating, No_of_Reviews, Time, reference_url, main_url, status, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(),now()) on duplicate key update modified_at = now()' 
        self.select_query = 'select sk,url,main_keyword,sub_keyword,ref_url from reviews_crawl where crawl_status=0 limit 50'
	#self.select_query = 'select sk , url , main_keyword, sub_keyword, ref_url from reviews_crawl where sk = "0fc8cc6e9a7a9f477598da398c291f4a"'
        self.update_query1 = "update reviews_crawl set crawl_status=9 where sk='%s' and crawl_status=0"
        self.upd_qry2 = "update reviews_crawl set crawl_status=1 where sk='%s' "
        self.upd_qry3 = "update reviews_crawl set crawl_status=2 where sk='%s'"
        self.del_qry = 'delete from Reviews_meta where sk="%s"'
        self.base_url = "https://www.google.co.in/"
        self.header_params = ['Processed Timestamp','keyword','reviewed_by', 'Review_text','Review_Star_Rating','Rating','No_of_Reviews','Time']
        self.excel_file_name = 'google_places_reviews_data_20171115.csv'
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file.writerow(self.header_params)
 
    def get_driver(self):
        profile = webdriver.FirefoxProfile() 
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "144.76.48.143")
        profile.set_preference("network.proxy.http_port", 3279)
        profile.update_preferences() 
        driver = webdriver.Firefox(profile) 
        self.cur.execute(self.select_query)
        data = self.cur.fetchall()
        for row in data :
            program_sk, url, main_keyword, sub_keyword, ref_url = row
            time.sleep(2)
            driver.get(url)
            driver.wait = WebDriverWait(driver, 3)
	    try : 
		time.sleep(5)
                driver.find_element_by_css_selector("button.widget-pane-link").click()
                driver.wait = WebDriverWait(driver, 3)
            except : 
                try :
		    time.sleep(5) 
                    driver.find_element_by_class_name("section-reviewchart-numreviews").click() 
                except :
			print 'nodata', url
                        sk = md5.md5(driver.current_url).hexdigest() 
                        values = (sk, program_sk, main_keyword, sub_keyword, '', '', '', 0, 0, '', str(driver.current_url), ref_url, 'Reviews Not Available')
                        self.cur.execute(self.del_qry % sk)
			self.cur.execute(self.insert_qry2,values)
                        self.cur.execute(self.update_query1 % program_sk)
                        self.con.commit()
                        continue
	    time.sleep(5)
            try : no_of_rev = int(driver.find_element_by_xpath('//div[@class="section-reviewchart-numreviews"]').text.split()[0])
            except : no_of_rev = 0
	    print no_of_rev
	    if no_of_rev == 0:
	    	print 'no_reviews', url
            time.sleep(2)
            if no_of_rev > 10 : page_counter  = int(no_of_rev)/10
            else : page_counter = 1
	    if no_of_rev != 1 or no_of_rev != 0:
		    try : 
			    dk = driver.find_element_by_xpath('//div[@class="section-listbox section-scrollbox scrollable-y scrollable-show"]')
			    time.sleep(10)
			    scroll = True
			    counter = 0
			    while scroll:
				driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dk)
				time.sleep(5)
				counter += 1
				time.sleep(2)
				if counter == int(page_counter):
				    scroll = False

		    except : 
			    try : self.cur.execute(self.upd_qry2 % program_sk)
			    except : print "wrong one"
			    self.con.commit()
			    continue
            try : 
	        reviews_count = driver.find_element_by_xpath('//div[@class="section-reviewchart-numreviews"]').text
                time.sleep(3)
	        count_review = ''.join(re.findall('(\d+) reviews', reviews_count))
		if not count_review:
			count_review = 0
                main_rating = driver.find_element_by_xpath('//div[@class="section-reviewchart-right"]/span/span').text
		if not main_rating:
			main_rating = 0
	        nodes = driver.find_elements_by_xpath('//div[@style="position:relative"]')
		time.sleep(2)
	        for nod in nodes:
		    re_by = nod.find_element_by_xpath('.//div[@class="section-review-title"]/span').text
                    time.sleep(1)
		    rew_text = nod.find_element_by_xpath('.//span[@class="section-review-text"]').text
		    rev_rat = nod.find_element_by_xpath('.//div[@class="section-review-metadata section-review-metadata-with-note"]/span').get_attribute('aria-label')
                    time.sleep(2)
		    r_rating = str(''.join(re.findall('(\d+) stars', rev_rat)))
		    r_on = nod.find_element_by_xpath('.//div[@class="section-review-metadata section-review-metadata-with-note"]/span[@class="section-review-publish-date"]').text
                    time.sleep(2)
                    sk = md5.md5(driver.current_url+re_by).hexdigest()
	            if str(count_review) == '':
			count_reivew = 0
		    values = (sk, str(program_sk), str(main_keyword), str(sub_keyword), re_by.encode('utf-8'), rew_text.encode('utf-8'), str(r_rating), main_rating, count_review, str(r_on), str(driver.current_url), ref_url, 'Available')
                    self.cur.execute(self.insert_qry2, values)
                    self.cur.execute(self.upd_qry3 % program_sk)
                    self.con.commit()
            except : 
                    
                    self.cur.execute(self.upd_qry2 % program_sk)
                    self.con.commit()
                    continue
                  

             
		    

    def main(self):
        driver = self.get_driver()
        #self.open_home_page(driver)

if __name__ == "__main__":
     GoogleReviewsTerminaln().main()
