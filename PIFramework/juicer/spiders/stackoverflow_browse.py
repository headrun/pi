from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import json
from scrapy.http import Request
import datetime
import csv
import re

class StackoverflowBrowse(BaseSpider):

    name = 'stackoverflow_browse'
    start_urls = []

    def __init__(self):
        self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'stackoverflow_data_%s.csv'%self.today_date
	self.header = ['Url', 'First Name','Last Name','User Reputation League','Summary','About Me','Sites','Email','Answers','Questions','People Reached','Location','Twitter_url','Github_url','Member for','Profile Views','Last Seen','Reputation','Gold_badges','Silver_badges','Bronze_badges','Communities_cnt','Community1_name','Community1_reputation','Community2_name','Community2_reputation','Community3_name','Community3_reputation','Community4_name','Community4_reputation','Community5_name','Community5_reputation','Top Tags_cnt','Top Tag1_name','Top Tag1_score','Top Tag1_posts','Top Tag1_posts%','Top Tag2_name','Top Tag2_score','Top Tag2_posts','Top Tag3_name','Top Tag3_score','Top Tag3_posts','Top Tag4_name','Top Tag4_score','Top Tag4_posts','Top Tag5_name','Top Tag5_score','Top Tag5_posts','Meta_questions','Meta_answers','Meta Post1','Meta Post1_views','Meta Post2','Meta Post2_views','Meta Post3','Meta Post3_views','Top Network Post1','Top Network Post1_views','Top Network Post2','Top Network Post2_views','Top Network Post3','Top Network Post3_views','Top Network Post4','Top Network Post4_views','Top Network Post5','Top Network Post5_views','Top Network Post6','Top Network Post6_views','Top Network Post7','Top Network Post7_views','Top Posts_cnt','Top Post1','Top Post1_views','Top Post1_date','Top Post2','Top Post2_views','Top Post2_date','Top Post3','Top Post3_views','Top Post3_date','Top Post4','Top Post4_views','Top Post4_date','Top Post5','Top Post5_views','Top Post5_date','Top Post6','Top Post6_views','Top Post6_date','Top Post7','Top Post7_views','Top Post7_date','Top Post8','Top Post8_views','Top Post8_date','Top Post9','Top Post9_views','Top Post9_date','Top Post10','Top Post10_views','Top Post10_date','Gold_badge1_name','Gold_badge1_date','Gold_badge2_name','Gold_badge2_date','Gold_badge3_name','Gold_badge3_date','Silver_badge1_name','Silver_badge1_date','Silver_badge2_name','Silver_badge2_date','Silver_badge3_name','Silver_badge3_date','Bronze_badge1_name','Bronze_badge1_date','Bronze_badge2_name','Bronze_badge2_date','Bronze_badge3_name','Bronze_badge3_date']
        self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.header)

    def start_requests(self):
        with open('stackoverflow_input.txt', 'r') as f:
            rows = f.readlines()
        for row in rows:
            row = row.replace('\n', '')
            yield Request(row, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
	name_ = ''.join(sel.xpath('//h2[@class="user-card-name"]/text()').extract()).encode('utf8').replace('\n', '').strip()
	try:
	    f_name, l_name = name_.split(' ')
	except:
	    f_name = name_
  	    l_name = ''
	user_repuation = ''.join(sel.xpath('//span[@class="top-badge"]/a//text()').extract())
	summary = ''.join(sel.xpath('//div[@class="current-position"]/text()').extract())
	bio = ' '.join(sel.xpath('//div[@class="bio"]//p[not(contains(text(), "Sites:"))][not(contains(text(), "Email:"))]//text()').extract()).strip('\n')
	sites = '<>'.join(sel.xpath('//p[contains(text(), "Sites:")]/following-sibling::ul/li/a/text()').extract())
	email = ''.join(sel.xpath('//p[contains(text(), "Email:")]/text()').extract()).split('(')[0].split('Email:')[-1].strip()
	answers = ''.join(sel.xpath('//div[@class="stat answers col-3"]/span/text()').extract())
	qustns = ''.join(sel.xpath('//div[@class="stat questions col-3"]/span/text()').extract())
	reached = ''.join(sel.xpath('//div[@class="stat people-helped col-5"]/span/text()').extract())
	location = ''.join(sel.xpath('//li[svg[contains(@class, "Location")]]/text()').extract()).replace('\n', '').strip()
	twitter_link = ''.join(sel.xpath('//li[svg[contains(@class, "Twitter")]]/a/@href').extract())
	git_link = ''.join(sel.xpath('//li[svg[contains(@class, "GitHub")]]/a/@href').extract())
	member = ''.join(sel.xpath('//li[svg[contains(@class, "History")]]/span/text()').extract())
	views = ''.join(sel.xpath('//li[svg[contains(@class, "Eye")]]/text()').extract()).replace('\n', '').strip().replace(',', '')
	views = ''.join(re.findall('(\d+)', views))
	last_seen = ''.join(sel.xpath('//li[svg[contains(@class, "Clock")]]/span/text()').extract())
	reputation = ''.join(sel.xpath('//div[@class="reputation"]/text()').extract()).replace('\n', '').strip()
	gold = ''.join(sel.xpath('//div[contains(@title, "gold")]/span[@class="g-col g-center -total"]/text()').extract())
	silver = ''.join(sel.xpath('//div[contains(@title, "silver")]/span[@class="g-col g-center -total"]/text()').extract())
	bronze = ''.join(sel.xpath('//div[contains(@title, "bronze")]/span[@class="g-col g-center -total"]/text()').extract())
	community_node = sel.xpath('//div[@class="sidebar-element communities"]')
	values = [response.url, f_name, l_name, user_repuation, summary, bio, sites, email, answers, qustns, reached, location, twitter_link, git_link, member, views, last_seen, reputation, gold, silver, bronze]
	if community_node:
	    community_node = community_node[0]
	    c_cnt = ''.join(community_node.xpath('./h3/span[2]/text()').extract())
	    c_cnt = ''.join(re.findall('\((.*)\)', c_cnt))
	    values.append(c_cnt)
	    c_nodes = community_node.xpath('.//li/a')
	    for i in range(0, 5):
	        try:
	    	    c_node = c_nodes[i]
		    c_name = ''.join(c_node.xpath('./span[@class="community-name"]/text()').extract())
		    c_rep = ''.join(c_node.xpath('./span[@class="rep"]/text()').extract())
		    values.extend([c_name, c_rep])
	        except:
		    values.extend(['', ''])
	else:
	    values.append('')
	    for i in range(0, 5):
		values.extend(['', ''])
	top_tags_node = sel.xpath('//div[@id="top-tags"]')
	if top_tags_node:
	    top_tags_node = top_tags_node[0]
	    tt_cnt = ''.join(top_tags_node.xpath('./h3/span/text()').extract()).replace(',', '')
	    tt_cnt = ''.join(re.findall('\((.*)\)', tt_cnt))
	    tt_nodes = top_tags_node.xpath('.//div[contains(@class, "g-row -tag-group g-col")]')
	    values.append(tt_cnt)
	    for i in range(0, 5):
	        try:
		    tt_node = tt_nodes[i]
		    tt_name = ''.join(tt_node.xpath('.//a[@class="post-tag"]/text()').extract())
		    values.append(tt_name)
		    tt_list = tt_node.xpath('.//span[@class="g-col -number"]/text()').extract()
		    values.extend(tt_list)
	        except:
		    if i==0:
		        values.extend(['', '', '', ''])
		    else:
		        values.extend(['', '', ''])
	else:
	    values.append('')
	    for i in range(0, 5):
		if i==0:
                    values.extend(['', '', '', ''])
                else:
                    values.extend(['', '', ''])

	meta_posts_node = sel.xpath('//div[@class="sidebar-element communities-posts"][h3[contains(text(), "Top Meta Posts")]]')
	if meta_posts_node:
	    meta_posts_node = meta_posts_node[0]
	    m_ansrs = ''.join(meta_posts_node.xpath('.//span[contains(@title, "answer")]/text()').extract())
	    m_qnts = ''.join(meta_posts_node.xpath('.//span[contains(@title, "question")]/text()').extract())
	    values.extend([m_qnts, m_ansrs])
	    meta_nodes = meta_posts_node.xpath('./ul/li')
	    for i in range(0, 3):
	        try:
		    m_node = meta_nodes[i]
		    m_post = ''.join(m_node.xpath('./a/text()').extract())
		    m_score = ''.join(m_node.xpath('./a/span/text()').extract())
		    values.extend([m_post, m_score])
	        except:
		    values.extend(['', ''])
	else:
	    values.extend(['', ''])
	    for i in range(0, 3):
		values.extend(['', ''])
	network_nodes = sel.xpath('//div[@class="sidebar-element communities-posts"][h3[contains(text(), "Top Network Posts")]]/ul/li[not(@class)]')
	if network_nodes:
	    for i in range(0, 7):
	        try:
		    n_node = network_nodes[i]
		    n_post = ''.join(n_node.xpath('./a/text()').extract())
                    n_score = ''.join(n_node.xpath('./a/span/text()').extract())
                    values.extend([n_post, n_score])
                except:
                    values.extend(['', ''])
	else:
	    for i in range(0, 7):
		values.extend(['', ''])
	top_posts_node = sel.xpath('//div[@id="top-posts"]')
	if top_posts_node:
	    top_posts_node = top_posts_node[0]
            tp_cnt = ''.join(top_posts_node.xpath('./h3/span/text()').extract()).replace(',', '')
            tp_cnt = ''.join(re.findall('\((.*)\)', tp_cnt))
	    values.append(tp_cnt)
            tp_nodes = top_posts_node.xpath('.//div[@class="row post-container"]')
	    for i in range(0, 10):
	        try:
		    tp_node = tp_nodes[i]
		    tp_post = ''.join(tp_node.xpath('./a/text()').extract())
		    tp_views = ''.join(tp_node.xpath('./span[contains(@class, "vote")]/text()').extract())
		    tp_date = ''.join(tp_node.xpath('./span[@class="post-date"]/span/@title').extract()).split(' ')[0]
		    values.extend([tp_post, tp_views, tp_date])
	        except:
		    values.extend(['', '', ''])
	else:
	    values.append('')
	    for i in range(0, 10):
		values.extend(['', '', ''])
	badge_nodes = sel.xpath('//div[@id="badges"]//td')
	for badge in badge_nodes:
	    b_nodes = badge.xpath('.//li')
	    if b_nodes:
	        for i in range(0, 3):
		    try:
		        b_node = b_nodes[i]
		        b_name = ''.join(b_node.xpath('./a/text()').extract()).replace(u'\xa0', '')
		        b_date = ''.join(b_node.xpath('./span[@class="badge-date"]/text()').extract())
		        values.extend([b_name, b_date])
		    except:
		        values.extend(['', ''])
	    else:
		for i in range(0, 3):
		    values.extend(['', ''])
	self.todays_excel_file.writerow(values)
