# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.exceptions import DropItem
from Facebook.items import *
import time
import datetime

DB_NAME = 'FACEBOOK'
DB_HOST = 'localhost'

class FacebookPipeline(object):

    def __init__(self):
	self.conn = MySQLdb.connect(db = DB_NAME, host = DB_HOST , user = 'root' , passwd='root')
        self.conn.set_character_set('utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.cursor.execute('SET autocommit=1')

    def process_item(self, item, spider):

	if isinstance(item, Fbpagesmeta):
		query = 'insert into facebook_pages_meta(page_sk, page_url, page_id, page_name, created_at, modified_at, last_seen) values (%s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_url=%s, page_id=%s, page_name=%s'
		values = (item['page_sk'], item.get('page_url', ''), item.get('page_id', ''), item.get('page_name', ''), item['page_sk'], item.get('page_url', ''), item.get('page_id', ''), item.get('page_name', ''))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item,Fbpagespost):
		query = 'insert into facebook_pages_posts(page_sk, page_id, post_sk, post_id, post_shares_count, post_url, post_message, post_created_time, post_updated_time, post_picture, post_from_name, post_from_id, post_to_name, post_to_id, post_comments_total_count, post_reactions_total_count, post_like_count, post_love_count, post_wow_count, post_haha_count, post_sad_count, post_angry_count, post_json_url, created_at, modified_at, last_seen) values (%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, post_shares_count=%s, post_url=%s, post_message=%s, post_created_time=%s, post_updated_time=%s, post_picture=%s, post_from_name=%s, post_from_id=%s, post_to_name=%s, post_to_id=%s, post_comments_total_count=%s, post_reactions_total_count=%s, post_like_count=%s, post_love_count=%s, post_wow_count=%s, post_haha_count=%s, post_sad_count=%s, post_angry_count=%s, post_json_url=%s'
		values = (item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('post_shares_count', ''), item.get('post_url', ''), item.get('post_message', ''), item.get('post_created_time', ''), item.get('post_updated_time', ''), item.get('post_picture', ''), item.get('post_from_name', ''), item.get('post_from_id', ''), item.get('post_to_name', ''), item.get('post_to_id', ''), item.get('post_comments_total_count', ''), item.get('post_reactions_total_count', ''), item.get('post_like_count', ''), item.get('post_love_count', ''), item.get('post_wow_count', ''), item.get('post_haha_count', ''), item.get('post_sad_count', ''), item.get('post_angry_count', ''), item.get('post_json_url', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('post_shares_count', ''), item.get('post_url', ''), item.get('post_message', ''), item.get('post_created_time', ''), item.get('post_updated_time', ''), item.get('post_picture', ''), item.get('post_from_name', ''), item.get('post_from_id', ''), item.get('post_to_name', ''), item.get('post_to_id', ''), item.get('post_comments_total_count', ''), item.get('post_reactions_total_count', ''), item.get('post_like_count', ''), item.get('post_love_count', ''), item.get('post_wow_count', ''), item.get('post_haha_count', ''), item.get('post_sad_count', ''), item.get('post_angry_count', ''), item.get('post_json_url', ''))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item, Fbpagespostcomment):
		query = 'insert into facebook_pages_posts_comments(page_sk, page_id, post_sk, post_id, comment_sk, comment_id, comment_from_id, comment_from_name, comment_message, comment_created_time, inner_comments_total_count, comment_reactions_total_count, comment_like_count, comment_love_count, comment_wow_count, comment_haha_count, comment_sad_count, comment_angry_count, created_at, modified_at, last_seen) values ( %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, comment_from_id=%s, comment_from_name=%s, comment_message=%s, comment_created_time=%s, inner_comments_total_count=%s, comment_reactions_total_count=%s, comment_like_count=%s, comment_love_count=%s, comment_wow_count=%s, comment_haha_count=%s, comment_sad_count=%s, comment_angry_count=%s'
                values = (item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('comment_from_id', ''), item.get('comment_from_name', ''), item.get('comment_message', ''), item.get('comment_created_time', ''), item.get('inner_comments_total_count', ''), item.get('comment_reactions_total_count', ''), item.get('comment_like_count', ''), item.get('comment_love_count', ''), item.get('comment_wow_count', ''), item.get('comment_haha_count', ''), item.get('comment_sad_count', ''), item.get('comment_angry_count', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('comment_from_id', ''), item.get('comment_from_name', ''), item.get('comment_message', ''), item.get('comment_created_time', ''), item.get('inner_comments_total_count', ''), item.get('comment_reactions_total_count', ''), item.get('comment_like_count', ''), item.get('comment_love_count', ''), item.get('comment_wow_count', ''), item.get('comment_haha_count', ''), item.get('comment_sad_count', ''), item.get('comment_angry_count', ''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Fbpagespostinnercomment):
		query = 'insert into facebook_pages_posts_inner_comments(page_sk, page_id, post_sk, post_id, comment_sk, comment_id, inner_comment_sk, inner_comment_id, inner_comment_from_id, inner_comment_from_name, inner_comment_message, inner_comment_created_time, innercomment_like_count, inner_comment_love_count, inner_comment_wow_count, inner_comment_haha_count, inner_comment_sad_count, inner_comment_angry_count, inner_comment_reactions_total_count, created_at, modified_at, last_seen) values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, inner_comment_sk=%s, inner_comment_id=%s, inner_comment_from_id=%s, inner_comment_from_name=%s, inner_comment_message=%s, inner_comment_created_time=%s, innercomment_like_count=%s, inner_comment_love_count=%s, inner_comment_wow_count=%s, inner_comment_haha_count=%s, inner_comment_sad_count=%s, inner_comment_angry_count=%s, inner_comment_reactions_total_count=%s'
                values = (item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('inner_comment_sk', ''), item.get('inner_comment_id', ''), item.get('inner_comment_from_id', ''), item.get('inner_comment_from_name', ''), item.get('inner_comment_message', ''), item.get('inner_comment_created_time', ''), item.get('innercomment_like_count', ''), item.get('inner_comment_love_count', ''), item.get('inner_comment_wow_count', ''), item.get('inner_comment_haha_count', ''), item.get('inner_comment_sad_count', ''), item.get('inner_comment_angry_count', ''), item.get('inner_comment_reactions_total_count', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('inner_comment_sk', ''), item.get('inner_comment_id', ''), item.get('inner_comment_from_id', ''), item.get('inner_comment_from_name', ''), item.get('inner_comment_message', ''), item.get('inner_comment_created_time', ''), item.get('innercomment_like_count', ''), item.get('inner_comment_love_count', ''), item.get('inner_comment_wow_count', ''), item.get('inner_comment_haha_count', ''), item.get('inner_comment_sad_count', ''), item.get('inner_comment_angry_count', ''), item.get('inner_comment_reactions_total_count', ''))
                self.cursor.execute(query, values)
                self.conn.commit()


	if isinstance(item, Fbpagespostreactions):
		query = 'insert into facebook_pages_posts_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
                values = (item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type'), item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type', ''))
                self.cursor.execute(query, values)
                self.conn.commit()


	if isinstance(item, Fbpagepostcommentreac):
		query = 'insert into facebook_pages_posts_comments_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, comment_sk, comment_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
                values = (item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type'), item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type', ''))
                self.cursor.execute(query, values)
                self.conn.commit()


	if isinstance(item, Fbpagepostinnercommnetreac):
		query = 'insert into facebook_pages_posts_comments_inner_reactions(reaction_sk, page_sk, page_id, post_sk, post_id, comment_sk, comment_id, inner_comment_sk, inner_comment_id, member_id, member_name, reaction_type, created_at, modified_at, last_seen) values(  %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), reaction_sk=%s, page_sk=%s, page_id=%s, post_sk=%s, post_id=%s, comment_sk=%s, comment_id=%s, inner_comment_sk=%s, inner_comment_id=%s, member_id=%s, member_name=%s, reaction_type=%s'
                values = (item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('inner_comment_sk', ''), item.get('inner_comment_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type'), item.get('reaction_sk', ''), item.get('page_sk', ''), item.get('page_id', ''), item.get('post_sk', ''), item.get('post_id', ''), item.get('comment_sk', ''), item.get('comment_id', ''), item.get('inner_comment_sk', ''), item.get('inner_comment_id', ''), item.get('member_id', ''), item.get('member_name', ''), item.get('reaction_type',''))
                self.cursor.execute(query, values)
                self.conn.commit()
