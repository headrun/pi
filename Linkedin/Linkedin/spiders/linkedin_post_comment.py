from selenium import webdriver
from selenium.webdriver.common.by import By #1
from selenium.webdriver.support.ui import WebDriverWait #2
from selenium.webdriver.support import expected_conditions as EC #3
from pyvirtualdisplay import Display
from linkedin_functions import *
from linkedin_post_constants import *

from lxml import html
import time

def get_driver():
    driver = webdriver.Firefox()
    return driver

def open_home_page(driver):
    driver.get("https://www.linkedin.com/")
    time.sleep(2)
    usr = driver.find_element_by_xpath("//input [@id='login-email' and @class='login-email']")
    passw = driver.find_element_by_xpath("//input [@id='login-password' and @class='login-password' ]")
    logbtn = driver.find_element_by_xpath("//input [@id='login-submit' and  @class='login submit-button']")
    usr.send_keys('lckiranmayi9@gmail.com')
    passw.send_keys('')
    logbtn.click()
    time.sleep(10)
    user_name = driver.find_element_by_xpath('//a[@data-control-name="identity_welcome_message"]')
    if user_name.text:
    comment_url = 'https://www.linkedin.com/pulse/why-we-must-construct-different-world-work-women-mlambo-ngcuka?trk=v-feed&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_content%3BZakIT6Lr7Lh4mkbXUrdThw%3D%3D'
    driver.get(comment_url)
    comment_sk = md5(comment_url)
    time.sleep(4)
    comment_nex_p = True
    while comment_nex_p:
        next_commne = ''
        try:
            next_commne = driver.find_element_by_xpath('//div[@class="comments-more-button-section"]//button[@class="comments-more-button"]')
        except: comment_nex_p = False
        if next_commne:
            next_commne.click()
            time.sleep(2)

    comment_nodes = driver.find_elements_by_xpath('//div[@class="comments-threads"]//div[@class="comments-thread-container"]')
    for cmt in comment_nodes:
        comment_by = ''
        cmt_name = cmt.find_element_by_xpath('.//h2/a[@class="commenter-name"]').text
        cmt_time = cmt.find_element_by_xpath('.//span[@class="comment-time"]').text
        cmt_image = cmt.find_element_by_xpath('.//img[@class="commenter-image"]').get_attribute('src')
        cmt_url = cmt.find_element_by_xpath('.//h2/a[@class="commenter-name"]').get_attribute('href')
        cmt_desc = cmt.find_element_by_xpath('.//span[contains(@class,"message-holder")]').text
        cmt_title = cmt.find_element_by_xpath('.//h3[@class="commenter-title"]').text
        cmt_comment_count, cmt_total_likes = ['']*2
        try:
            cmt_total_likes = cmt.find_element_by_xpath('.//span[@class="comment-button-separator"]//span[@aria-label="Total Likes"]').text
        except:
            cmt_total_likes = ''
        try:
            cmt_comment_count = cmt.find_element_by_xpath('.//span[@class="comment-button-separator"]//span[@aria-label="Comment Count"]').text
        except:
            cmt_comment_count = ''

        comment_container = []
        try:
            comment_container = cmt.find_elements_by_xpath('.//section[@class="comment-container nested"]')
        except:
            comment_container = []
        inner_sk = md5("%s%s%s%s%s"%(cmt_name, cmt_desc, cmt_title, cmt_url, comment_sk))
        valss = (inner_sk, comment_sk, cmt_name, cmt_time, cmt_image, cmt_url, cmt_desc, cmt_title, cmt_total_likes, cmt_comment_count, comment_url, inner_sk)
        cur.execute(query1, valss)
        for repl in comment_container:
            reply_time = repl.find_element_by_xpath('.//span[@class="comment-time"]').text
            reply_image = repl.find_element_by_xpath('.//img[@class="commenter-image"]').get_attribute('src')
            reply_name = repl.find_element_by_xpath('./article/h2/a[@class="commenter-name"]').text
            reply_name_url = repl.find_element_by_xpath('./article/h2/a[@class="commenter-name"]').get_attribute('href')
            reply_title = repl.find_element_by_xpath('./article/h3[@class="commenter-title"]').text
            reply_text = repl.find_element_by_xpath('./article//span[contains(@class,"message-holder")]').text
            reply_likes = ''
            try:
                reply_likes = repl.find_element_by_xpath('./article//span[@class="comment-button-separator"]//span[@aria-label="Total Likes")]').text
            except:
                reply_likes = ''
            reply_comment_count = ''
            try:
                reply_comment_count = repl.find_element_by_xpath('./article//span[@class="comment-button-separator"]//span[@aria-label="Comment Count"]').text
            except:
                reply_comment_count = ''
            inner_reply_sk = md5("%s%s%s%s%s"%(reply_time, inner_sk,reply_text, reply_name, reply_name_url))
            vals_rply = (inner_reply_sk, inner_sk, comment_sk, reply_name, reply_time, reply_image, reply_name_url, reply_text, reply_title, reply_likes, reply_comment_count, comment_url, inner_reply_sk)
            cur.execute(query2, vals_rply)
    time.sleep(3)
    driver.get('https://www.linkedin.com/logout/')
    driver.quit()

def main():

    driver = get_driver()
    open_home_page(driver)


if __name__ == "__main__":
    main()
