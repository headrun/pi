from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
import re
import json
import datetime
import csv

class KaggleBrowse(BaseSpider):

    name = 'kaggle_browse'
    start_urls = ['https://www.kaggle.com/aharless']

    def __init__(self):
        self.load_dict = {}
        self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
	self.excel_file_name = 'kaggle_data_%s.csv'%self.today_date
	self.header = ['First Name','Last Name','Summary','Location','Joined','Last Seen','Url','Github_url','Twitter_url','Linkedin_url','Followers','Following','Progression','Competitions','Kernels','Discussion','Datasets','Competitions Expert_current rank','Competitions Expert_highest rank','Competitions Expert_gold_cnt','Competitions Expert_silver_cnt','Competitions Expert_bronze_cnt','Competition1_rank','Competition1_total','Competition1_updated','Competition1_status','Competition2_rank','Competition2_total','Competition2_updated','Competition2_status','Competition3_rank','Competition3_total','Competition3_updated','Competition3_status','Kernels Master_current rank','Kernels Master_highest rank','Kernels Master_gold_cnt','Kernels Master_silver_cnt','Kernels Master_bronze_cnt','Kernel1_updated','Kernel1_votes','Kernel2_updated','Kernel2_votes','Kernel3_updated','Kernel3_votes','Discussion_Master_current_rank','Discussion_Master_highest_rank','Discussion_gold_cnt','Discussion_silver_cnt','Discussion_bronze_cnt','Discussion1_updated','Discussion1_votes','Discussion2_updated','Discussion2_votes','Discussion3_updated','Discussion3_votes','Bio','Follower1_name','Follower2_name','Follower3_name','Follower4_name','Follower5_name','Follower6_name','Follower7_name','Follower8_name','Follower9_name']
	self.oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.header)

    def parse(self, response):
	sel = Selector(response)
	script_data = ''.join(sel.xpath('//div[@data-component-name="ProfileContainerReact"]/following-sibling::script[1]/text()').extract())
	data = ''.join(re.findall('\((.*)\)', script_data)).split(';')[0].strip(')')
	if data:
	    data = json.loads(data)
	    firstname, lastname = data['displayName'].split(' ')
	    occupation = data['occupation']
	    organization = data['organization']
	    summary = '%s at %s'%(occupation, organization)
	    city = data['city']
	    region = data['region']
	    country = data['country']
	    location = '%s, %s, %s'%(city, region, country)
	    joined = data['userJoinDate']
	    last_seen = data['userLastActive']
	    website_url = data['websiteUrl']
	    github = data['gitHubUserName']
	    git_link = 'https://github.com/%s'%github
	    twitter = data['twitterUserName']
	    twitter_link = 'https://twitter.com/%s'%twitter
	    linked_link = data['linkedInUrl']
	    followers = data['followers']['count']
	    following = data['following']['count']
	    tier1 = data['performanceTierCategory']
	    tier2 = data['performanceTier']
	    progression = '%s %s'%(tier1.title(), tier2.title())
	    competition_data = data['competitionsSummary']
	    c_count = competition_data['totalResults']
	    kernels_data = data['scriptsSummary']
	    kernels = kernels_data['totalResults']
            discussion_data = data['discussionsSummary']
            discussion = discussion_data['totalResults']
            datasets = data['totalDatasets']
	    c_cur_rank = competition_data['rankCurrent']
            c_high_rank = competition_data['rankHighest']
            c_gold_medals = competition_data['totalGoldMedals']
            c_silver_medals = competition_data['totalSilverMedals']
            c_bronze_medals = competition_data['totalBronzeMedals']
	    values = [firstname, lastname, summary, location, joined, last_seen, website_url, git_link, twitter_link, linked_link, followers, following, progression, c_count, kernels, discussion, datasets, c_cur_rank, c_high_rank, c_gold_medals, c_silver_medals, c_bronze_medals]
	    c_highlights = competition_data['highlights']
	    c_list = []
	    for c_highlight in c_highlights:
	    	c_rank = c_highlight['score']
		c_total = c_highlight['scoreOutOf']
		c_updated = c_highlight['date']
		c_status = c_highlight['isOngoingCompetition']
		c_lst = [c_rank, c_total, c_updated, c_status]
		c_list.extend(c_lst)
	    values.extend(c_list)
	    dict_ = {'kernels':kernels_data, 'discussion':discussion_data}
	    for value in dict_.values():
            	cur_rank = value['rankCurrent']
	    	high_rank = value['rankHighest']
            	gold_medals = value['totalGoldMedals']
            	silver_medals = value['totalSilverMedals']
            	bronze_medals = value['totalBronzeMedals']
	    	highlights = value['highlights']
		values.extend([cur_rank, high_rank, gold_medals, silver_medals, bronze_medals])
	    	list_ = []
	    	for highlight in highlights:
		    updated = highlight['date']
		    votes = highlight['score']
		    lst = [updated, votes]
		    list_.extend(lst)
	    	values.extend(list_)
	    bio = data['bio']
	    values.append(bio)
	    follower_list = data['followers']['list']
	    for i in range(0, 9):
		follower = follower_list[i]['displayName']
		values.append(follower)
	    self.todays_excel_file.writerow(values)
