# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.exceptions import DropItem
from Linkedin.items import *
import time
import datetime
#from scrapy.pipelines.images import ImagesPipeline
from scrapy.contrib.pipeline.images import ImagesPipeline

DB_NAME = 'FACEBOOK'
DB_HOST = 'localhost'
 
class LinkedinPipeline(object):
    def __init__(self):
	self.conn = MySQLdb.connect(db = DB_NAME, host = DB_HOST , user = 'root' , passwd='root')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.cursor.execute('SET autocommit=1')

    def process_item(self, item, spider):
	if isinstance(item, LinkedinItem):
            query = 'INSERT INTO linkedin_connections(sk, profile_sk, connections_profile_url, member_id, headline, name, image_url, image_path, aux_info, reference_url,created_at, modified_at, last_seen) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, connections_profile_url=%s, member_id=%s, headline=%s, name=%s, image_url=%s, image_path=%s, aux_info=%s'
            values = (item['sk'], item.get('profile_sk',''), item.get('connections_profile_url','') ,\
		    item.get('member_id',''), item.get('headline',''), item.get('name',''), \
                      item.get('image_url',''), item.get('image_path',''),item.get('aux_info',''), item.get('reference_url',''),\
		     item['sk'], item.get('profile_sk','') , item.get('connections_profile_url',''),\
			item.get('member_id',''), item.get('headline',''), item.get('name',''), \
		     item.get('image_url',''), item.get('image_path',''),item.get('aux_info',''))
            self.cursor.execute(query, values)
            self.conn.commit()
        if isinstance(item, Linkedinaccounts):
	    query = 'INSERT INTO linkedin_accounts(profile_sk, status, username, password, aux_info, reference_url,created_at, modified_at, last_seen) values (%s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), profile_sk=%s, status=%s, username=%s, password=%s, aux_info=%s, reference_url=%s'
	    values = (item['profile_sk'], item.get('status',''), item.get('username',''), item.get('password',''), item.get('aux_info',''), item.get('reference_url',''), item['profile_sk'], item.get('status',''), item.get('username',''), item.get('password',''), item.get('aux_info',''), item.get('reference_url',''))
	    self.cursor.execute(query, values)
            self.conn.commit()
        #return item

class MyImagesPipeline(ImagesPipeline):
    def __init__(self):
        self.conn = MySQLdb.connect(db = DB_NAME, host = DB_HOST , user = 'root' , passwd='root')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.cursor.execute('SET autocommit=1')

    """def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
	

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
    def image_key(self, url):
        image_guid = url.split('/')[-1]
        return 'full/%s' % (image_guid)
    def file_path(self, request, response=None, info=None):
	image_guid = url.split('/')[-1]
	return 'full/%s' % (image_guid)"""

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
	   self.myBaseImageName = item['accessionNo'][0]
           yield Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = request.meta['model'][0]
        return 'full/%s' % (image_guid)

    """def image_key(self, url):
        return 'full/%s.jpg' % (str(self.myBaseImageName))

    def file_path(self, request, response=None, info=None):
        #item = request.meta['item']
        #image_guid = request.url.split('/')[-1]
	image_guid = request.meta['model'][0]
        image_name = item['image_titles']+image_guid[-8:]
        return image_name"""
