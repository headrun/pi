import unittest
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
from selenium.webdriver.common.keys import Keys
from linkedin_functions import *

class TestProd(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(100)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.url1 = 'https://www.linkedin.com/search/results/content/?keywords=%23'
        self.url2 = '&origin=GLOBAL_SEARCH_HEADER'
        self.url3 = 'https://www.linkedin.com/pulse-fe/api/v1/comments?urn='
        self.url4 = '&start=0&count='
        self.url5 = '&sort=REV_CHRON'
        self.con, self.cur = get_mysql_connection(DB_HOST, 'urlqueue_dev', '')
        self.query1 = 'insert into comments_crawl(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values(%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at=now(), content_type=%s, crawl_status=0,meta_data=%s'
        self.pattern1 = re.compile(r'\d+')

    def test_prod(self):
        driver = self.driver
        self.driver.get("https://www.linkedin.com/")
        time.sleep(3)
        usr = self.driver.find_element_by_xpath("//input [@id='login-email' and @class='login-email']")
        passw = self.driver.find_element_by_xpath("//input [@id='login-password' and @class='login-password' ]")
        logbtn = self.driver.find_element_by_xpath("//input [@id='login-submit' and  @class='login submit-button']")
        usr.send_keys('cheedellach@gmail.com')
        passw.send_keys('cheedellach427')
        logbtn.click()
        time.sleep(10)
        user_name = self.driver.find_element_by_xpath('//a[@data-control-name="identity_welcome_message"]')
        if user_name.text: print "Logged In: %s" % user_name.text
        driver_url = "%s%s%s"%(self.url1, keyword, self.url2)
        self.driver.get(driver_url)
        time.sleep(10)
        scroll = True
        counter = 0
        while scroll:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            counter += 1
            time.sleep(2)
            if counter == 30:
                scroll = False
        time.sleep(2)
        article_nodes = self.driver.find_elements_by_xpath('//ul[@class="results-list"]/li[contains(@class,"search-entity")]')
        for article in article_nodes:
            article_id = article.find_element_by_xpath('./article').get_attribute('data-id')
            article_name = article.find_element_by_xpath('.//h3/span[contains(@class,"feed-s-post-meta__name")]').text
            check_button = [i.get_attribute('data-control-name') for i in article.find_elements_by_tag_name("button")]
            if 'comments_count' in check_button:
                href_list = [ad.get_attribute('href') for ad in article.find_elements_by_tag_name('a')]
                matching = [sp for sp in href_list if "/pulse" in sp]
                comments_l = article.find_element_by_xpath('.//li[@class="feed-s-social-counts__item"]/button[@data-control-name="comments_count"]/span[@aria-hidden="true"]').text
                if comments_l and self.pattern1.search(comments_l):
                    comments_count = textify(self.pattern1.findall(comments_l))
                    meta_data = {}
                    if matching:
                        pulse_url = article.find_element_by_xpath('.//div[@class="display-content ember-view"]/div/a[contains(@href,"/pulse")]').get_attribute('href')
                        meta_data.update({"pulse_url":pulse_url})
                        time.sleep(3)
                        self.driver.execute_script("window.open('%s');"%pulse_url)
                        self.driver.switch_to_window(driver.window_handles[-1])
                        article_id = self.driver.find_element_by_xpath('//section[@id="comments"]//div[@class="comments-container"]').get_attribute('id').replace('pulse-comments-','')
                        time.sleep(3)
                        self.driver.close()
                        self.driver.switch_to_window(driver.window_handles[0])
                    comments_count = textify(self.pattern1.findall(comments_l))
                    if comments_count and article_id:
                        comments_url = "%s%s%s%s%s"%(self.url3, article_id, self.url4, comments_count, self.url5)
                        sk = md5(comments_url)
                        meta_data.update({"name":article_name, "comments_count":comments_count, "main_url":driver_url})
                        values = (sk, comments_url, 'comments', 0, json.dumps(meta_data),'comments', json.dumps(meta_data))
                        self.cur.execute(self.query1, values)
    
    def tearDown(self):
        self.driver.get('https://www.linkedin.com/logout/')
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("command-line parameter keyword must be given -- keyword")
    keyword = sys.argv[1]
    del sys.argv[1:]
    unittest.main()
    

