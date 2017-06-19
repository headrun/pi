# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LinkedinItem(Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	sk          = Field()
	profile_sk 	= Field()
	connections_profile_url = Field()
	member_id   = Field()
	headline	= Field()
	name        = Field()
	image_url       = Field()
	image_path 	= Field()
	aux_info    = Field()
	reference_url = Field()
class Linkedintestscore(Item):
	sk 	= Field()
	profile_sk = Field()
	testscore_name = Field()
	testscore_description = Field()
	testscore = Field()
	testscore_day = Field()
	testscore_month = Field()
	testscore_year = Field()
class Linkedintrack(Item):
	sk	= Field()
	member_id = Field()
	login_mail_id	= Field()
	machine_ip = Field()
	crawl_status = Field()
class Linkedincourse(Item):
        sk = Field()
        profile_sk = Field()
        course_name = Field()
        course_number = Field()
class Linkedinpublications(Item):
        sk = Field()
        profile_sk = Field()
	publication_title = Field()
	publication_url = Field()
	publisher = Field()
	publication_description = Field()
	publication_date = Field()
class Linkedinaccounts(Item):
	profile_sk 	= Field()
	status	= Field()
	username	= Field()
	password	= Field()
	aux_info	= Field()
	reference_url = Field()
class ImageItem(Item):
	image_urls = Field()
	images = Field()
class Linkedinmeta(Item):
	sk = Field()
	profile_url  = Field()
	profileview_url  = Field()
	name  = Field()
	first_name  = Field()
	last_name  = Field()
	member_id  = Field()
	headline  = Field()
	no_of_followers  = Field()
	profile_post_url  = Field()
	summary  = Field()
	number_of_connections  = Field()
	industry  = Field()
	location  = Field()
	languages  = Field()
	emails  = Field()
	websites  = Field()
	addresses  = Field()
	message_handles  = Field()
	phone_numbers  = Field()
	birthday  = Field()
	birth_year  = Field()
	birth_month  = Field()
	twitter_accounts  = Field()
	profile_image  = Field()
	interests  = Field()
	location_postal_code = Field()
	location_country_code = Field()
	background_image = Field()
	image_path = Field()

class Linkedinposts(Item):
	sk  = Field()
	profile_sk  = Field()
	post_url  = Field()
	post_image  = Field()
	post_title  = Field()
	post_author_id  = Field()
	post_state  = Field()
	post_date  = Field()
	post_article_id  = Field()
class Linkedingroups(Item):
	sk  = Field()
	profile_sk  = Field()
	group_link  = Field()
	group_name  = Field()
	no_of_members  = Field()
	group_logo  = Field()
	group_id  = Field()
	group_description = Field()
class Linkedineducations(Item):
	sk  = Field()
	profile_sk  = Field()
	edu_start_year  = Field()
	edu_start_month  = Field()
	edu_start_date  = Field()
	edu_end_year  = Field()
	edu_end_date  = Field()
	edu_end_month  = Field()
	edu_degree  = Field()
	edu_field_of_study  = Field()
	edu_school_name  = Field()
	school_logo  = Field()
	edu_grade = Field()
	edu_activities = Field()
	post_article_id  = Field()
	education_id  = Field()
	school_id  = Field()
class Linkedingivenrecommendations(Item):
	sk  = Field()
	profile_sk  = Field()
	last_name  = Field()
	name  = Field()
	date_and_relationship  = Field()
	title  = Field()
	created_date  = Field()
	summary  = Field()
	profile_image  = Field()
	profile_member_id  = Field()
	profile_url  = Field()
	recommendation_id  = Field()	
class Linkedinrecrecommendations(Item):
	sk  = Field()
	profile_sk  = Field()
	role  = Field()
	profile_member_id  = Field()
	id  = Field()
	edu_start_date  = Field()
	name  = Field()
	organization  = Field()
	created_date  = Field()
	date_and_relationship  = Field()
	headline  = Field()
	profile_url  = Field()
	profile_image  = Field()
	summary  = Field()
class Linkedinexperiences(Item):
	sk  = Field()
	profile_sk  = Field()
	exp_location  = Field()
	exp_company_name  = Field()
	exp_company_url  = Field()
	exp_title  = Field()
	start_date  = Field()
	end_date  = Field()
	exp_company_logo  = Field()
	exp_duration  = Field()
	exp_company_id  = Field()
	exp_position_id  = Field()
	exp_summary = Field()
class Linkedincertifications(Item):
	sk  = Field()
	profile_sk  = Field()
	certification_id  = Field()
	certification_date  = Field()
	certification_title  = Field()
	certification_company_logo  = Field()
	certification_company_name = Field()
	certification_licence = Field()
class Linkedinprojects(Item):
	sk  = Field()
	profile_sk  = Field()
	project_date  = Field()
	number_of_project_members  = Field()
	project_member_names  = Field()
	project_occupation_name  = Field()
	project_title  = Field()
	project_url  = Field()
	project_start_date  = Field()
	project_end_date  = Field()
	project_description  = Field()
class Linkedinhonors(Item):
	sk  = Field()
	profile_sk  = Field()
	honor_on  = Field()
	honor_issuer  = Field()
	honor_summary  = Field()
	honor_title  = Field()
	occupation = Field()
class Linkedincourserecom(Item):
	sk  = Field()
	profile_sk  = Field()
	course_title  = Field()
	duration_seconds  = Field()
	duration_minutes  = Field()
	duration_hrs  = Field()
	no_of_viewers  = Field()
	course_image  = Field()
	course_url  = Field()
class Linkedinskills(Item):
	sk  = Field()
	profile_sk  = Field()
	skill_name  = Field()
	endoresement_count  = Field()
	member_topic_skill_url  = Field()
	public_topic_skill_url  = Field()
class Linkedinfollowcompanies(Item):
	sk  = Field()
	profile_sk  = Field()
	company_canonical_name  = Field()
	total_followee_count  = Field()
	company_logo  = Field()
	company_universal_name  = Field()
	company_url  = Field()
class Linkedinfollowinfluencers(Item):
	sk  = Field()
	profile_sk  = Field()
	inflencer_name  = Field()
	influencer_firstname  = Field()
	influencer_lastname  = Field()
	influencer_image  = Field()
	influencer_profile_url  = Field()
	influencer_headline  = Field()
	influencer_followers_count = Field()
		
class Linkedinfollowschools(Item):
	sk  = Field()
	profile_sk  = Field()
	school_name  = Field()
	school_image  = Field()
	school_region  = Field()
	school_link  = Field()
	total_followee_count  = Field()
class Linkedinfollowchannels(Item):
	sk  = Field()
	profile_sk  = Field()
	channel_followers  = Field()
	channel_title  = Field()
	channel_link  = Field()
	channel_image  = Field()
class Linkedinvolunteerexp(Item):
	sk  = Field()
	profile_sk  = Field()
	volunteer_interests  = Field()
	volunteer_role  = Field()
	volunteer_cause  = Field()
	organization_name  = Field()
	organization_logo  = Field()
	description  = Field()
	start_date_year  = Field()
	start_date_month  = Field()
	volunteer_date  = Field()
	end_date_year	= Field()
	end_date_month	= Field()
	organization_id	= Field()
class Linkedinorganizations(Item):
	sk  = Field()
	profile_sk  = Field()
	name  = Field()
	position  = Field()
	start_date  = Field()
	end_date  = Field()
	description  = Field()
	occupation_name  = Field()
