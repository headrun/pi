import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
from selenium.webdriver.common.keys import Keys
from linkedin_functions import *

class TestProd(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '') 
        self.query1 = 'select sk, original_url from linkedin_connectionprofiles limit 10'
	self.query2 = 'update linkedin_connectionprofiles set profile_url= "%s" where sk = "%s"'

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
	time.sleep(2)
	rec = execute_query(self.query1)
	for re in rec:
		driver.get(re[0])
		url = driver.get_current_url
		time.sleep(1)
		print url, sk

    def tearDown(self):
        self.driver.get('https://www.linkedin.com/logout/')
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	unittest.main()
	
	

