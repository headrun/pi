from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import md5
import  MySQLdb
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

class GoogleReviewsTerminal(object):

    def __init__(self):
        
        self.con = MySQLdb.connect(db='google_reviews', host='localhost', charset="utf8", use_unicode=True, user='root', passwd='root')
        self.cur = self.con.cursor()
	self.insert_query = 'insert into reviewslink_crawl(sk, url, crawl_type, content_type, related_type, crawl_status, meta_data, created_at, modified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now(), meta_data=%s, url=%s'
	self.select_query = 'select sk,url,main_keyword,sub_keyword from reviews_crawl where crawl_status=0'
        self.upd_qry1 = "update reviews_crawl set crawl_status=1 where sk='%s' "
        self.upd_qry2 = "update reviews_crawl set crawl_status=2 where sk='%s'"
	self.insert_qry1 = 'insert into Reviews_meta(sk, program_sk, main_keyword, sub_keyword, reviewed_by, Review_text, Review_Star_Rating, Rating, No_of_Reviews, Time, reference_url, main_url, status, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(),now()) on duplicate key update modified_at = now()'
 
    def get_driver(self):
	PROXY = '103.56.30.128'
	PORT = 8080
        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['proxy']={
            "proxyType":"manual",
            "httpProxy":PROXY,
            "httpProxyPort": PORT,
            "ftpProxy":PROXY,
            "ftpProxyPort": PORT,
            "sslProxy":PROXY,
            "sslProxyPort" : PORT}
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        firefox_profile.set_preference("intl.accept_languages", "en")
        driver = webdriver.Firefox(firefox_profile=firefox_profile)
        self.cur.execute(self.select_query)
        data = self.cur.fetchall()
        for row in data :
            program_sk, url, main_keyword, sub_keyword = row
	    meta_data = {"url":url, "main_keyword":main_keyword, "sub_keyword":sub_keyword}
            driver.get(url)
            time.sleep(6)
            driver.wait = WebDriverWait(driver, 3)
	    try : 
                driver.find_element_by_css_selector("button.widget-pane-link").click()
		time.sleep(10)
		ref_url = driver.current_url
		no_of_rev = driver.find_element_by_xpath('//div[@class="section-reviewchart-numreviews"]').text.split(' ')[0].replace(',', '')
		main_rating = driver.find_element_by_xpath('//div[@class="section-reviewchart-right"]/span/span').text
		meta_data.update({"reviews":str(no_of_rev), "main_rating":str(main_rating)})
                driver.wait = WebDriverWait(driver, 3)
                time.sleep(2)
		nodes = driver.find_elements_by_xpath('//div[@style="position:relative"]')
		time.sleep(5)
		reviews_list = []
		for nod in nodes:
		    re_by = nod.find_element_by_xpath('.//div[@class="section-review-title"]/span').text
                    time.sleep(1)
                    rev_rat = nod.find_element_by_xpath('.//div[@class="section-review-metadata section-review-metadata-with-note"]/span[2]').get_attribute('aria-label')
                    time.sleep(2)
                    r_rating = str(''.join(re.findall('(\d+) stars', rev_rat)))
                    r_on = nod.find_element_by_xpath('.//div[@class="section-review-metadata section-review-metadata-with-note"]/span[@class="section-review-publish-date"]').text
                    time.sleep(2)
		    try:
			nod.find_element_by_xpath('.//button[@class="section-expand-review blue-link"]').click()
			time.sleep(5)
			rew_text = nod.find_element_by_xpath('.//span[@class="section-review-text"]').text
		    except: rew_text = nod.find_element_by_xpath('.//span[@class="section-review-text"]').text
		    try: sk = md5.md5(driver.current_url+re_by).hexdigest()
		    except: sk = md5.md5(driver.current_url+rew_text).hexdigest()
                    values = (sk, str(program_sk), str(main_keyword), str(sub_keyword), re_by.encode('utf-8'), rew_text.encode('utf-8'), str(r_rating), main_rating, str(no_of_rev), str(r_on), ref_url, url, 'Available')

		    values1 = (str(main_keyword).replace('\n', ''), '', re_by.encode('utf-8'), rew_text.encode('utf-8'),str(r_rating),main_rating,str(no_of_rev), str(r_on) , ref_url, url,'Available')
		    reviews_list.append(values1)
                    self.cur.execute(self.insert_qry1, values)
                    self.con.commit()
		    meta_data.update({"reviews_list":reviews_list})
		    vals = (program_sk, str(ref_url), '', '', '', 0, json.dumps(meta_data), json.dumps(meta_data), str(ref_url))
		    self.cur.execute(self.insert_query,vals)
		    self.con.commit()
		    self.cur.execute(self.upd_qry1%program_sk)
		    self.con.commit()
            except :
		self.cur.execute(self.upd_qry2%program_sk)
                self.con.commit()

    def main(self):
        driver = self.get_driver()

if __name__ == "__main__":
     GoogleReviewsTerminal().main()
