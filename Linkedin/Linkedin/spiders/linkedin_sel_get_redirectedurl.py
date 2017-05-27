import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
from selenium.webdriver.common.keys import Keys
from linkedin_functions import *
from random_mails import mails_dict

class TestProd(unittest.TestCase):

    def setUp(self):
        #self.driver = webdriver.PhantomJS("/root/test/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
	#self.driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
	self.driver = webdriver.Firefox()
        self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '') 
        self.query1 = 'select sk, original_url from linkedin_connectionprofiles where profile_url like "%name&authToken%" order by rand() limit 10'
	self.query2 = 'update linkedin_connectionprofiles set profile_url= "%s" where sk = "%s"'

    def test_prod(self):
        driver = self.driver
        self.driver.get("https://www.linkedin.com/")
        time.sleep(2)
        usr = self.driver.find_element_by_xpath("//input [@id='login-email' and @class='login-email']")
        passw = self.driver.find_element_by_xpath("//input [@id='login-password' and @class='login-password' ]")
        logbtn = self.driver.find_element_by_xpath("//input [@id='login-submit' and  @class='login submit-button']")
	#maile, pwd  = keyword.split(',')
	maile, pwd = random.choice(list(mails_dict.items()))[1]
	usr.send_keys(maile)
	passw.send_keys(pwd)
	logbtn.click()
	time.sleep(2)
	rec = fetchmany(self.cur, self.query1)
	counter = 0
	for re in rec:
		driver.get(re[1])
		time.sleep(6)
		url = driver.current_url
		if '/in/' in url and '/in/unavailable/' not in url:
			execute_query(self.cur, self.query2%(url, re[0]))
		counter +=1
		print counter
		print url, re[0]
	close_mysql_connection(self.con, self.cur)
    def tearDown(self):
        self.driver.get('https://www.linkedin.com/logout/')
        self.driver.quit()

if __name__ == "__main__":
	#if len(sys.argv) != 2:
		#sys.exit("command-line parameter keyword must be given -- loginids")
	#keyword = sys.argv[1]
	#del sys.argv[1:]
	unittest.main()
	
	

