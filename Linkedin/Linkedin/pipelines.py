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
		query = 'INSERT INTO linkedin_connections(sk, profile_sk, connections_profile_url, member_id, headline, name, image_url, image_path, background_image_url, aux_info, reference_url,created_at, modified_at, last_seen) values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, connections_profile_url=%s, member_id=%s, headline=%s, name=%s, image_url=%s, image_path=%s, background_image_url=%s, aux_info=%s'
		values = (item['sk'], item.get('profile_sk',''), item.get('connections_profile_url','') ,\
		    item.get('member_id',''), item.get('headline',''), item.get('name',''), \
		      item.get('image_url',''), item.get('image_path',''), item.get('background_image_url', ''), item.get('aux_info',''), item.get('reference_url',''),\
		     item['sk'], item.get('profile_sk','') , item.get('connections_profile_url',''),\
			item.get('member_id',''), item.get('headline',''), item.get('name',''), \
		     item.get('image_url',''), item.get('image_path',''), item.get('background_image_url', ''), item.get('aux_info',''))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item, Linkedincompanymeta):
		query = 'INSERT INTO linkedin_company_meta(sk, company_given_url, company_given_sno, company_given_name, company_name,company_page_url, number_of_employees, no_of_followers, industry, city, geographic_area, line1, line2, postal_code, company_type, company_description,created_at, modified_at, last_seen) values (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, company_given_url=%s, company_given_sno=%s, company_given_name=%s, company_name=%s, company_page_url=%s, number_of_employees=%s, no_of_followers=%s, industry=%s, city=%s, geographic_area=%s, line1=%s, line2=%s, postal_code=%s, company_type=%s, company_description=%s'
		values = (item['sk'], item.get('company_given_url', ''), item.get('company_given_sno', ''), item.get('company_given_name', ''), item.get('company_name', ''), item.get('company_page_url', ''), item.get('number_of_employees', ''), item.get('no_of_followers', ''), item.get('industry', ''), item.get('city', ''), item.get('geographic_area', ''), item.get('line1', ''), item.get('line2', ''), item.get('postal_code', ''), item.get('company_type', ''), item.get('company_description', ''), item['sk'], item.get('company_given_url', ''), item.get('company_given_sno', ''), item.get('company_given_name', ''), item.get('company_name', ''), item.get('company_page_url', ''), item.get('number_of_employees', ''), item.get('no_of_followers', ''), item.get('industry', ''), item.get('city', ''), item.get('geographic_area', ''), item.get('line1', ''), item.get('line2', ''), item.get('postal_code', ''), item.get('company_type', ''), item.get('company_description', ''))
		self.cursor.execute(query, values)
		self.conn.commit()

        if isinstance(item, Linkedincourse):
                query = 'INSERT INTO linkedin_courses(sk, profile_sk, course_name, course_number, created_at, modified_at, last_seen) values(%s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, course_name=%s, course_number=%s'
                values = (item['sk'], item.get('profile_sk',''), item.get('course_name',''), item.get('course_number',''), item['sk'], item.get('profile_sk',''), item.get('course_name',''), item.get('course_number',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedintestscore):
		query = 'INSERT INTO linkedin_testscore(sk, profile_sk, testscore_name, testscore_description, testscore, testscore_day, testscore_month, testscore_year, created_at, modified_at, last_seen) values(%s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, testscore_name=%s, testscore_description=%s, testscore=%s, testscore_day=%s, testscore_month=%s, testscore_year=%s'
		values = (item['sk'], item.get('profile_sk',''),item.get('testscore_name',''), item.get('testscore_description',''), item.get('testscore',''), item.get('testscore_day',''), item.get('testscore_month',''), item.get('testscore_year',''),item['sk'], item.get('profile_sk',''),item.get('testscore_name',''), item.get('testscore_description',''), item.get('testscore',''), item.get('testscore_day',''), item.get('testscore_month',''), item.get('testscore_year',''))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item, Linkedintrack):
		query = 'INSERT INTO linkedin_track(sk, member_id, login_mail_id, machine_ip, crawl_status, given_key, aux_info, created_at, modified_at, last_seen) values(%s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, member_id=%s, login_mail_id=%s, machine_ip=%s, crawl_status=%s, given_key=%s, aux_info=%s'
		values = (item['sk'], item.get('member_id',''), item.get('login_mail_id',''), item.get('machine_ip',''), item.get('crawl_status', ''), item.get('given_key',''), MySQLdb.escape_string(item.get('aux_info', '')), item['sk'], item.get('member_id',''), item.get('login_mail_id',''), item.get('machine_ip',''), item.get('crawl_status',''), item.get('given_key',''), MySQLdb.escape_string(item.get('aux_info', '')))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item, Linkedinpublications):
		query = 'INSERT INTO linkedin_publications(sk, profile_sk, publication_title, publication_url, publisher, publication_description, publication_date,   created_at, modified_at, last_seen) values(%s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, publication_title=%s, publication_url=%s, publisher=%s, publication_description=%s, publication_date=%s'
		values = (item['sk'], item.get('profile_sk',''),item.get('publication_title',''), item.get('publication_url',''), item.get('publisher',''), item.get('publication_description',''), item.get('publication_date',''), item['sk'], item.get('profile_sk',''),item.get('publication_title',''), item.get('publication_url',''), item.get('publisher',''), item.get('publication_description',''), item.get('publication_date',''))
		self.cursor.execute(query, values)
		self.conn.commit()

        if isinstance(item, Linkedinaccounts):
                query = 'INSERT INTO linkedin_accounts(profile_sk, status, exact_connections_count, username, password, aux_info, reference_url,created_at, modified_at, last_seen) values (%s,%s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), profile_sk=%s, status=%s, exact_connections_count=%s, username=%s, password=%s, aux_info=%s, reference_url=%s'
                values = (item['profile_sk'], item.get('status',''), item.get('exact_connections_count', ''), item.get('username',''), item.get('password',''), item.get('aux_info',''), item.get('reference_url',''), item['profile_sk'], item.get('status',''), item.get('exact_connections_count', ''), item.get('username',''), item.get('password',''), item.get('aux_info',''), item.get('reference_url',''))
                self.cursor.execute(query, values)
                self.conn.commit()


	if isinstance(item, Linkedinmeta):
		query = 'INSERT INTO linkedin_meta(sk, profile_url, profileview_url, name, first_name, last_name, member_id, headline, no_of_followers, profile_post_url, summary, number_of_connections, industry, location, languages, emails, websites, addresses, message_handles, phone_numbers, birthday, birth_year, birth_month, twitter_accounts, profile_image, interests,location_postal_code, location_country_code, background_image, image_path, created_at, modified_at, last_seen) values (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_url=%s, profileview_url=%s, name=%s, first_name=%s, last_name=%s, member_id=%s, headline=%s, no_of_followers=%s, profile_post_url=%s, summary=%s, number_of_connections=%s, industry=%s, location=%s, languages=%s, emails=%s, websites=%s, addresses=%s, message_handles=%s, phone_numbers=%s, birthday=%s, birth_year=%s, birth_month=%s, twitter_accounts=%s, profile_image=%s, interests=%s, location_postal_code=%s, location_country_code=%s, background_image=%s, image_path=%s'
		values = (item.get('sk',''), item.get('profile_url',''), item.get('profileview_url',''), item.get('name',''), item.get('first_name',''), item.get('last_name',''), item.get('member_id',''), item.get('headline',''), item.get('no_of_followers',''), item.get('profile_post_url',''), item.get('summary',''), item.get('number_of_connections',''), item.get('industry',''), item.get('location',''), item.get('languages',''), item.get('emails',''), item.get('websites',''), item.get('addresses',''), item.get('message_handles',''), item.get('phone_numbers',''), item.get('birthday',''), item.get('birth_year',''), item.get('birth_month',''), item.get('twitter_accounts',''), item.get('profile_image',''), item.get('interests',''), item.get('location_postal_code',''),item.get('location_country_code',''), item.get('background_image',''), item.get('image_path',''), item.get('sk',''), item.get('profile_url',''), item.get('profileview_url',''), item.get('name',''), item.get('first_name',''), item.get('last_name',''), item.get('member_id',''), item.get('headline',''), item.get('no_of_followers',''), item.get('profile_post_url',''), item.get('summary',''), item.get('number_of_connections',''), item.get('industry',''), item.get('location',''), item.get('languages',''), item.get('emails',''), item.get('websites',''), item.get('addresses',''), item.get('message_handles',''), item.get('phone_numbers',''), item.get('birthday',''), item.get('birth_year',''), item.get('birth_month',''), item.get('twitter_accounts',''), item.get('profile_image',''), item.get('interests',''), item.get('location_postal_code',''),item.get('location_country_code',''), item.get('background_image',''), item.get('image_path',''))
		self.cursor.execute(query, values)
		self.conn.commit()
	if isinstance(item, Linkedinposts):
		query = 'INSERT INTO linkedin_posts(sk, profile_sk, post_url, post_image, post_title, post_author_id, post_state, post_date, post_article_id, created_at, modified_at, last_seen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, post_url=%s, post_image=%s, post_title=%s, post_author_id=%s, post_state=%s, post_date=%s, post_article_id=%s'
		values = (item.get('sk',''), item.get('profile_sk',''), item.get('post_url',''), item.get('post_image',''), item.get('post_title',''), item.get('post_author_id',''), item.get('post_state',''), item.get('post_date',''), item.get('post_article_id',''),item.get('sk',''), item.get('profile_sk',''), item.get('post_url',''), item.get('post_image',''), item.get('post_title',''), item.get('post_author_id',''), item.get('post_state',''), item.get('post_date',''), item.get('post_article_id',''))
		self.cursor.execute(query, values)
		self.conn.commit()

	if isinstance(item, Linkedingroups):
		query = 'INSERT INTO linkedin_groups(sk, profile_sk, group_link, group_name, no_of_members, group_logo, group_id, group_description, created_at, modified_at, last_seen)values(%s, %s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, group_link=%s, group_name=%s, no_of_members=%s, group_logo=%s, group_id=%s, group_description=%s'
		values = (item.get('sk',''), item.get('profile_sk',''), item.get('group_link',''), item.get('group_name',''), item.get('no_of_members',''), item.get('group_logo',''), item.get('group_id',''), item.get('group_description',''), item.get('sk',''), item.get('profile_sk',''), item.get('group_link',''), item.get('group_name',''), item.get('no_of_members',''), item.get('group_logo',''), item.get('group_id',''), item.get('group_description',''))
                self.cursor.execute(query, values)
                self.conn.commit()
	if isinstance(item, Linkedineducations):
		query = 'INSERT INTO linkedin_educations(sk, profile_sk, edu_start_year, edu_start_month, edu_start_date, edu_end_year, edu_end_date, edu_end_month, edu_degree, edu_field_of_study, edu_school_name, school_logo, edu_grade, edu_activities, post_article_id, education_id, school_id, created_at, modified_at, last_seen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, edu_start_year=%s, edu_start_month=%s, edu_start_date=%s, edu_end_year=%s, edu_end_date=%s, edu_end_month=%s, edu_degree=%s, edu_field_of_study=%s, edu_school_name=%s, school_logo=%s, edu_grade=%s, edu_activities=%s,  post_article_id=%s, education_id=%s, school_id=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('edu_start_year',''), item.get('edu_start_month',''), item.get('edu_start_date',''), item.get('edu_end_year',''), item.get('edu_end_date',''), item.get('edu_end_month',''), item.get('edu_degree',''), item.get('edu_field_of_study',''), item.get('edu_school_name',''), item.get('school_logo',''), item.get('edu_grade',''), item.get('edu_activities',''), item.get('post_article_id',''), item.get('education_id',''), item.get('school_id',''),item.get('sk',''), item.get('profile_sk',''), item.get('edu_start_year',''), item.get('edu_start_month',''), item.get('edu_start_date',''), item.get('edu_end_year',''), item.get('edu_end_date',''), item.get('edu_end_month',''), item.get('edu_degree',''), item.get('edu_field_of_study',''), item.get('edu_school_name',''), item.get('school_logo',''),item.get('edu_grade',''), item.get('edu_activities',''), item.get('post_article_id',''), item.get('education_id',''), item.get('school_id',''))
                self.cursor.execute(query, values)
                self.conn.commit()
	if isinstance(item, Linkedingivenrecommendations):
		query = 'INSERT INTO linkedin_given_recommendations(sk, profile_sk, last_name, name, date_and_relationship, title, created_date, summary, profile_image, profile_member_id, profile_url, recommendation_id, created_at, modified_at, last_seen)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, last_name=%s, name=%s, date_and_relationship=%s, title=%s, created_date=%s, summary=%s, profile_image=%s, profile_member_id=%s, profile_url=%s, recommendation_id=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('last_name',''), item.get('name',''), item.get('date_and_relationship',''), item.get('title',''), item.get('created_date',''), item.get('summary',''), item.get('profile_image',''), item.get('profile_member_id',''), item.get('profile_url',''), item.get('recommendation_id',''),item.get('sk',''), item.get('profile_sk',''), item.get('last_name',''), item.get('name',''), item.get('date_and_relationship',''), item.get('title',''), item.get('created_date',''), item.get('summary',''), item.get('profile_image',''), item.get('profile_member_id',''), item.get('profile_url',''), item.get('recommendation_id',''))
                self.cursor.execute(query, values)
                self.conn.commit()
	if isinstance(item, Linkedinrecrecommendations):
		query = 'INSERT INTO linkedin_received_recommendations(sk, profile_sk, role, profile_member_id, id, edu_start_date, name, organization, created_date, date_and_relationship, headline, profile_url, profile_image, summary, created_at, modified_at, last_seen)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, role=%s, profile_member_id=%s, id=%s, edu_start_date=%s, name=%s, organization=%s, created_date=%s, date_and_relationship=%s, headline=%s, profile_url=%s, profile_image=%s, summary=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('role',''), item.get('profile_member_id',''), item.get('id',''), item.get('edu_start_date',''), item.get('name',''), item.get('organization',''), item.get('created_date',''), item.get('date_and_relationship',''), item.get('headline',''), item.get('profile_url',''), item.get('profile_image',''), item.get('summary',''), item.get('sk',''), item.get('profile_sk',''), item.get('role',''), item.get('profile_member_id',''), item.get('id',''), item.get('edu_start_date',''), item.get('name',''), item.get('organization',''), item.get('created_date',''), item.get('date_and_relationship',''), item.get('headline',''), item.get('profile_url',''), item.get('profile_image',''), item.get('summary',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinexperiences):
		query = 'INSERT INTO linkedin_experiences(sk, profile_sk, exp_location, exp_company_name, exp_company_url, exp_title, start_date, end_date, exp_company_logo, exp_duration, exp_company_id, exp_position_id, exp_summary,created_at, modified_at, last_seen)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, exp_location=%s, exp_company_name=%s, exp_company_url=%s, exp_title=%s, start_date=%s, end_date=%s, exp_company_logo=%s, exp_duration=%s, exp_company_id=%s, exp_position_id=%s, exp_summary=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('exp_location',''), item.get('exp_company_name',''), item.get('exp_company_url',''), item.get('exp_title',''), item.get('start_date',''), item.get('end_date',''), item.get('exp_company_logo',''), item.get('exp_duration',''), item.get('exp_company_id',''), item.get('exp_position_id',''),item.get('exp_summary',''), item.get('sk',''), item.get('profile_sk',''), item.get('exp_location',''), item.get('exp_company_name',''), item.get('exp_company_url',''), item.get('exp_title',''), item.get('start_date',''), item.get('end_date',''), item.get('exp_company_logo',''), item.get('exp_duration',''), item.get('exp_company_id',''), item.get('exp_position_id',''), item.get('exp_summary',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedincertifications):
		query = 'INSERT INTO linkedin_certifications(sk, profile_sk, certification_id, certification_date, certification_title, certification_company_logo, certification_company_name, created_at, modified_at, last_seen)values(%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, certification_id=%s, certification_date=%s, certification_title=%s, certification_company_logo=%s, certification_company_name=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('certification_id',''), item.get('certification_date',''), item.get('certification_title',''), item.get('certification_company_logo',''),item.get('certification_company_name','') ,item.get('sk',''), item.get('profile_sk',''), item.get('certification_id',''), item.get('certification_date',''), item.get('certification_title',''), item.get('certification_company_logo',''), item.get('certification_company_name',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinprojects):
		query = 'INSERT INTO linkedin_projects(sk, profile_sk, project_date, number_of_project_members, project_member_names, project_occupation_name, project_title, project_url, project_start_date, project_end_date, project_description, created_at, modified_at, last_seen)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, project_date=%s, number_of_project_members=%s, project_member_names=%s, project_occupation_name=%s, project_title=%s, project_url=%s, project_start_date=%s, project_end_date=%s, project_description=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('project_date',''), item.get('number_of_project_members',''), item.get('project_member_names',''), item.get('project_occupation_name',''), item.get('project_title',''), item.get('project_url',''), item.get('project_start_date',''), item.get('project_end_date',''), item.get('project_description',''), item.get('sk',''), item.get('profile_sk',''), item.get('project_date',''), item.get('number_of_project_members',''), item.get('project_member_names',''), item.get('project_occupation_name',''), item.get('project_title',''), item.get('project_url',''), item.get('project_start_date',''), item.get('project_end_date',''), item.get('project_description',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinhonors):
		query = 'INSERT INTO linkedin_honors(sk, profile_sk, honor_on, honor_issuer, honor_summary, honor_title, occupation, created_at, modified_at, last_seen) values (%s, %s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, honor_on=%s, honor_issuer=%s, honor_summary=%s, honor_title=%s, occupation=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('honor_on',''), item.get('honor_issuer',''), item.get('honor_summary',''), item.get('honor_title',''), item.get('occupation',''), item.get('sk',''), item.get('profile_sk',''), item.get('honor_on',''), item.get('honor_issuer',''), item.get('honor_summary',''), item.get('honor_title',''), item.get('occupation',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedincourserecom):
		query = 'INSERT INTO linkedin_courserecommendations(sk, profile_sk, course_title, duration_seconds, duration_minutes, duration_hrs, no_of_viewers, course_image, course_url, created_at, modified_at, last_seen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, course_title=%s, duration_seconds=%s, duration_minutes=%s, duration_hrs=%s, no_of_viewers=%s, course_image=%s, course_url=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('course_title',''), item.get('duration_seconds',''), item.get('duration_minutes',''), item.get('duration_hrs',''), item.get('no_of_viewers',''), item.get('course_image',''), item.get('course_url',''), item.get('sk',''), item.get('profile_sk',''), item.get('course_title',''), item.get('duration_seconds',''), item.get('duration_minutes',''), item.get('duration_hrs',''), item.get('no_of_viewers',''), item.get('course_image',''), item.get('course_url',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinskills):
		query = 'INSERT INTO linkedin_skills(sk, profile_sk, skill_name, endoresement_count, member_topic_skill_url, public_topic_skill_url, created_at, modified_at, last_seen) values (%s, %s, %s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, skill_name=%s, endoresement_count=%s, member_topic_skill_url=%s, public_topic_skill_url=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('skill_name',''), item.get('endoresement_count',''), item.get('member_topic_skill_url',''), item.get('public_topic_skill_url',''), item.get('sk',''), item.get('profile_sk',''), item.get('skill_name',''), item.get('endoresement_count',''), item.get('member_topic_skill_url',''), item.get('public_topic_skill_url',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinfollowcompanies):
		query = 'INSERT INTO linkedin_following_companies(sk, profile_sk, company_canonical_name, total_followee_count, company_logo, company_universal_name, company_url, created_at, modified_at, last_seen) values (%s, %s, %s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, company_canonical_name=%s, total_followee_count=%s, company_logo=%s, company_universal_name=%s, company_url=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('company_canonical_name',''), item.get('total_followee_count',''), item.get('company_logo',''), item.get('company_universal_name',''), item.get('company_url',''), item.get('sk',''), item.get('profile_sk',''), item.get('company_canonical_name',''), item.get('total_followee_count',''), item.get('company_logo',''), item.get('company_universal_name',''), item.get('company_url',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinfollowinfluencers):
		query = 'INSERT INTO linkedin_following_influencers(sk, profile_sk, inflencer_name, influencer_firstname, influencer_lastname, influencer_image, influencer_profile_url, influencer_headline, influencer_followers_count,  created_at, modified_at, last_seen) values(%s,%s, %s, %s,%s,%s,%s,%s,%s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, inflencer_name=%s, influencer_firstname=%s, influencer_lastname=%s, influencer_image=%s, influencer_profile_url=%s, influencer_headline=%s, influencer_followers_count=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('inflencer_name',''), item.get('influencer_firstname',''), item.get('influencer_lastname',''), item.get('influencer_image',''), item.get('influencer_profile_url',''), item.get('influencer_headline',''), item.get('influencer_followers_count',''), item.get('sk',''), item.get('profile_sk',''), item.get('inflencer_name',''), item.get('influencer_firstname',''), item.get('influencer_lastname',''), item.get('influencer_image',''), item.get('influencer_profile_url',''), item.get('influencer_headline',''), item.get('influencer_followers_count',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinfollowschools):
		query = 'INSERT INTO linkedin_following_schools(sk, profile_sk, school_name, school_image, school_region, school_link, total_followee_count, created_at, modified_at, last_seen) values(%s, %s, %s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, school_name=%s, school_image=%s, school_region=%s, school_link=%s, total_followee_count=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('school_name',''), item.get('school_image',''), item.get('school_region',''), item.get('school_link',''), item.get('total_followee_count',''), item.get('sk',''), item.get('profile_sk',''), item.get('school_name',''), item.get('school_image',''), item.get('school_region',''), item.get('school_link',''), item.get('total_followee_count',''))
                self.cursor.execute(query, values)
                self.conn.commit()

		
	if isinstance(item, Linkedinfollowchannels):
		query = 'INSERT INTO linkedin_following_channels(sk, profile_sk, channel_followers, channel_title, channel_link, channel_image, created_at, modified_at, last_seen) values(%s, %s, %s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(),sk=%s, profile_sk=%s, channel_followers=%s, channel_title=%s, channel_link=%s, channel_image=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('channel_followers',''), item.get('channel_title',''), item.get('channel_link',''), item.get('channel_image',''), item.get('sk',''), item.get('profile_sk',''), item.get('channel_followers',''), item.get('channel_title',''), item.get('channel_link',''), item.get('channel_image',''))
                self.cursor.execute(query, values)
                self.conn.commit()
	if isinstance(item, Linkedinvolunteerexp):
		query = 'INSERT INTO linkedin_volunteer_experiences(sk, profile_sk, volunteer_interests, volunteer_role, volunteer_cause, organization_name, organization_logo, description, start_date_year, start_date_month, volunteer_date, end_date_year, end_date_month, organization_id, created_at, modified_at, last_seen) values (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, volunteer_interests=%s, volunteer_role=%s, volunteer_cause=%s, organization_name=%s, organization_logo=%s, description=%s, start_date_year=%s, start_date_month=%s, volunteer_date=%s, end_date_year=%s, end_date_month=%s, organization_id=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('volunteer_interests',''), item.get('volunteer_role',''), item.get('volunteer_cause',''), item.get('organization_name',''), item.get('organization_logo',''), item.get('description',''), item.get('start_date_year',''), item.get('start_date_month',''), item.get('volunteer_date',''), item.get('end_date_year'), item.get('end_date_month', ''), item.get('organization_id',''), item.get('sk',''), item.get('profile_sk',''), item.get('volunteer_interests',''), item.get('volunteer_role',''), item.get('volunteer_cause',''), item.get('organization_name',''), item.get('organization_logo',''), item.get('description',''), item.get('start_date_year',''), item.get('start_date_month',''), item.get('volunteer_date',''), item.get('end_date_year'), item.get('end_date_month', ''), item.get('organization_id',''))
		self.cursor.execute(query, values)
                self.conn.commit()

	if isinstance(item, Linkedinorganizations):
		query = 'INSERT INTO linkedin_organizations(sk, profile_sk, name, position, start_date, end_date, description, occupation_name, created_at, modified_at, last_seen) values( %s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk=%s, profile_sk=%s, name=%s, position=%s, start_date=%s, end_date=%s, description=%s, occupation_name=%s'
                values = (item.get('sk',''), item.get('profile_sk',''), item.get('name',''), item.get('position',''), item.get('start_date',''), item.get('end_date',''), item.get('description',''), item.get('occupation_name',''), item.get('sk',''), item.get('profile_sk',''), item.get('name',''), item.get('position',''), item.get('start_date',''), item.get('end_date',''), item.get('description',''), item.get('occupation_name',''))
                self.cursor.execute(query, values)
                self.conn.commit()

	
        #return item

class MyImagesPipeline(ImagesPipeline):
    def __init__(self):
        self.conn = MySQLdb.connect(db = DB_NAME, host = DB_HOST , user = 'root', passwd='root')
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
