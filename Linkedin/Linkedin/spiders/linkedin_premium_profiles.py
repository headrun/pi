import scrapy
import md5
import json
import re
import requests
import MySQLdb
import hashlib
import time
from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.xlib.pydispatch import dispatcher
from linkedin_queries import *
from Linkedin.items import *
class LinkedinpremiumprofilesBrowse(scrapy.Spider):
    name = "linkedinpremiumprofiles_browse"
    allowed_domains = ["linkedin.com"]
    start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

    def __init__(self, *args, **kwargs):
	super(LinkedinpremiumprofilesBrowse, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login', 'ramanujan')
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd = 'root')
	self.cur = self.con.cursor()
	get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 limit 15"
	self.cur.execute(get_query_param)
	self.profiles_list = [i for i in self.cur.fetchall()]
	dispatcher.connect(self.spider_closed, signals.spider_closed)
	self.ajax1 = "https://www.linkedin.com/profile/mappers?x-a=profile_v2_megaphone_articles%2Cprofile_v2_discovery%2Cprofile_v2_browse_map%2Cprofile_v2_references%2Cprofile_v2_background%2Cprofile_v2_courses%2Cprofile_v2_test_scores%2Cprofile_v2_patents%2Cprofile_v2_badge%2Cprofile_v2_basic_info%2Cprofile_v2_publications%2Cprofile_v2_name_bi%2Cprofile_v2_additional_info%2Cprofile_v2_volunteering%2Cprofile_v2_location_bi%2Cprofile_v2_contact_info%2Cprofile_v2_groups%2Cprofile_v2_skills%2Cprofile_v2_connections%2Cprofile_v2_follow%2Cprofile_v2_educations%2Cprofile_v2_summary%2Cprofile_v2_positions%2Cprofile_v2_honors%2Cprofile_v2_certifications%2Cprofile_v2_languages%2Cprofile_v2_projects%2Cprofile_v2_organizations%2Cprofile_v2_course_recommendations%2Cprofile_v2_endorsements&x-p=profile_v2_connections.distance%3A1%2Ctop_card.profileContactsIntegrationStatus%3A0%2Cprofile_v2_right_fixed_discovery.records%3A12%2Cprofile_v2_right_fixed_discovery.offset%3A0%2Cprofile_v2_browse_map.pageKey%3Anprofile_view_nonself%2Cprofile_v2_discovery.offset%3A0%2Cprofile_v2_discovery.records%3A12%2Cprofile_v2_discovery.records%3A12%2Ctop_card.tc%3Atrue%2Cprofile_v2_discovery.offset%3A0%2Cprofile_v2_summary_upsell.summaryUpsell%3Atrue&x-oa=bottomAliases&id="
	self.ajax2 = "&locale=en_US&snapshotID=&authToken="
	self.ajax3 = "&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
	self.allcompanies_ajax = 'https://www.linkedin.com/profile/profile-v2-follow-companies?id="%s"&count=-1'
	self.domain = "https://www.linkedin.com"

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def md5(self, x):
        return hashlib.md5(self.xcode(x)).hexdigest()

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###').replace(u'\u2013','').strip()
        return text

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

    def clean(self, text):
        if not text: return text
        value = text
        value = re.sub("&amp;", "&", value)
        value = re.sub("&lt;", "<", value)
        value = re.sub("&gt;", ">", value)
        value = re.sub("&quot;", '"', value)
        value = re.sub("&apos;", "'", value)

        return value

    def normalize(self, text):
        return self.clean(self.compact(self.xcode(text)))

    def compact(self, text, level=0):
    	if text is None: return ''
	if level == 0:
	    text = text.replace("\n", " ")
	    text = text.replace("\r", " ")
        compacted = re.sub("\s\s(?m)", " ", text)
	if compacted != text:
	    compacted = self.compact(compacted, level+1)
        return compacted.strip()

    def parse(self, response):
	sel = Selector(response)
	logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
	csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
	source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
	account_mail, account_password = '', ''
	if self.login == 'ccv':
		account_mail = 'ccvy1.pavani1886@gmail.com'
		account_password = 'ccvy1.pavani@1886'
	elif self.login=='meatproject':
		account_mail = 'meatproject05@gmail.com'
		account_password = 'ram123123'
	elif self.login== 'ramanujan':
		account_mail = 'srinivasaramanujan427@gmail.com'
		account_password = 'dotoday1#'
	elif self.login == 'raja':
		account_mail = 'rajaqx@gmail.com'
		account_password = 'linkedinpw'
	if account_mail:	
	        return [FormRequest.from_response(response, formname = 'login_form',\
                    formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]

    def spider_closed(self, spider):
	cv = requests.get('https://www.linkedin.com/logout/').text
	
    def parse_next(self, response):
	sel = Selector(response)
	for li in self.profiles_list:
            meta_data = json.loads(li[2])
            email_address = meta_data.get('email_address','')
            sk = li[0]
	    #sk = self.md5(li[1])
            vals = (sk, li[1], sk, li[1])
	    self.cur.execute(update_get_params%(9,sk))
            #yield Request(li[1], callback=self.parse_again, headers=meat_headers,meta={"sk":sk, 'email_address':email_address})
	    yield Request(li[1], callback=self.parse_correct, meta={"sk":sk, 'email_address':email_address})

    def parse_again(self, response):
        sel = Selector(response)
        if 'unsupported-browser.html' in response.url:
                anywa = ''.join(sel.xpath('//a[contains(text(),"anyway")]/@href').extract())
                if anywa: yield Request(anywa, callback=self.parse_correct, dont_filter=True, meta={"sk":response.meta['sk']})
        else: yield Request(response.url, callback=self.parse_correct, dont_filter=True, meta={"sk":response.meta['sk']})

    def parse_correct(self, response):
        sel = Selector(response)
	sk = response.meta.get('sk','')
	meb = sel.xpath('//code[contains(text(),"PatentView")][contains(text(),"objectUrn")][contains(text(),"urn:li:member:")]').extract() 
	linkedin_auth, memb_id = '',''
	"""try: linkedin_auth = ''.join(re.findall('authToken=(.*?)&',(json.loads(sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').strip())['included'][-1].get('requestUrl',''))))
	except : linkedin_auth = ''"""
	linke_a, linkd_javatex = {},''
	try: linke_a = json.loads(sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').strip()).get('included','')
	except: linke_a = {}
	if linke_a:
		enum_l = [i for i,j in enumerate(linke_a) if 'authToken' in j.get('requestUrl','')]
		if enum_l:
			enumd = enum_l[0]
			linkd_javatex = linke_a[enumd].get('requestUrl','')
			linkedin_auth = ''.join(re.findall('authToken=(.*?)&',linke_a[enumd].get('requestUrl','')))
	if meb:
	    cvv = re.findall('\?id=(.*?)&',linkd_javatex)
	    if cvv:
	    	tys = '"urn:li:member:(\d+)","entityUrn":"urn:li:fs_miniProfile:%s"'%cvv[0]
	        memb_id = ''.join(re.findall(tys,meb[0]))
	if not memb_id: self.cur.execute(update_get_params%(6,sk))
	if memb_id and linkedin_auth:
	    req_url = "{}{}{}{}{}".format(self.ajax1, memb_id,self.ajax2, linkedin_auth, self.ajax3)
	    self.cur.execute(update_get_params%(1,sk))
	    yield Request(req_url, callback=self.parse_ajax,meta={"sk":sk,"ref_url":response.url,"memb_id":memb_id,"linkedin_auth":linkedin_auth})

    def parse_ajax(self, response):
	temp = json.loads(response.body)
 	all_keys = temp.get('content',{})
	sk = response.meta.get('sk','')
	ref_url = response.meta.get('ref_url','')
	memb_id = response.meta.get('memb_id','')
	linkedin_auth = response.meta.get('linkedin_auth','')
	first_name, lastName, name, member_headline,member_id, member_followers = ['']*6
	member_post_url, summart_des, number_of_connections, industry, location, lang_list = ['']*6
	top_edu_schoo, top_edu_field, top_edu_degree = ['']*3
	emails_list, message_handles_list, websites_list, twitters_list, address_list, phone_number_list, birthday, birthmonth, birthyear = ['']*9
	if all_keys:
	    certifications = all_keys.get('Certifications',{})
	    honors = all_keys.get('Honors',{})
	    projects = all_keys.get('Projects',{})
	    languages = all_keys.get('Languages',{})
	    course_recommendations = all_keys.get('course_recommendations',{})
	    groups = all_keys.get('groupsMpr',{})
	    discovery = all_keys.get('Discovery',{})
	    megaphone_articles = all_keys.get('profile_v2_megaphone_articles',{})
	    education = all_keys.get('Education',{})
	    skills = all_keys.get('Skills',{})
	    contact_info = all_keys.get('ContactInfo',{})
	    endorsements = all_keys.get('Endorsements',{})
	    following = all_keys.get('Following',{})
	    experience = all_keys.get('Experience',{})
	    organizations = all_keys.get('Organizations',{})
	    summary = all_keys.get('Summary',{})
	    additional_info = all_keys.get('AdditionalInfo',{})
	    basic_info = all_keys.get('BasicInfo',{}) 
	    voluneetering = all_keys.get('Volunteering',{})
	    another_basic_info = all_keys.get('basic_info',{})
            if basic_info:
                basic_info_inner = basic_info.get('basic_info',{})
                if basic_info_inner:
                    name = basic_info_inner.get('fullname','')
                    if not name: name = megaphone_articles.get("formattedInfluencerFullName" ,'')
                    member_id = basic_info_inner.get('memberID','')
		    member_headline = basic_info_inner.get('memberHeadline','')
                    industry = basic_info_inner.get('industry_highlight','')
                    location = basic_info_inner.get('location_highlight','')
                    if not location: location = basic_info_inner.get('fmt_location','')
            if summary:
                summary_inner = summary.get('summary',{})
                if summary_inner: summart_des =summary_inner.get('summary_lb','').replace('<br>','').replace('</br>','')
            if languages:
                languages_inner = languages.get('languages',{}).get('languagesData',[])
		lang_list = []
                for lani in languages_inner:
                    lan_name = lani.get('displayName','')
                    if not lan_name: lan_name = lani.get('lang','')
		    if lan_name: lang_list.append(lan_name)
		if lang_list: lang_list= ','.join(lang_list)
		else: lang_list = ''
            if contact_info:
                number_of_connections = contact_info.get('distance',{}).get('numberOfConnections','')
                relations_ship_info = contact_info.get('relationship_info',{})
                contact_details = relations_ship_info.get('contactDetails',{})
                contact_info_inner = contact_info.get('contact_info',{})
                if contact_info_inner:
                    emails = contact_info_inner.get('emails',[])
                    websites = contact_info_inner.get('websites',[])
                    twitter_accounts = contact_info_inner.get('twitterAccounts',[])
                    address = contact_info.get('addresses',[])
                    if address:
                        address_list = self.parse_list(address, 'fmt_address','')
                        if not address_list: address_list = self.parse_list(address, 'address','')

                    phone_number = contact_info.get('phones',[])
                    if phone_number: phone_number_list = self.parse_list(phone_number, 'number','fmt_type')
                    if emails:
                        emails_list = self.parse_list(emails, 'email','')
		    ims_instant_message = contact_info.get('IMs',[])
		    if ims_instant_message: message_handles_list = self.parse_list(message_handles, 'username','fmt_type')

                    if websites: websites_list = self.parse_list(websites, 'URL','fmt_type')
                    if twitter_accounts: twitters_list = self.parse_list(twitter_accounts, 'twitterHandle','')
                if contact_details:
                    if not first_name: first_name = contact_details.get('firstName','')
                    if not lastName: lastName = contact_details.get('lastName','')
                    if not name: name = contact_details.get('name','')
                    birthday = str(contact_details.get('birthDay',''))
                    birthmonth = str(contact_details.get('birthMonth',''))
                    birthyear = str(contact_details.get('birthYear',''))
                    emails = contact_details.get('emails',[])
                    websites = contact_details.get('websites',[])
                    address = contact_details.get('addresses',[])
                    phone_number = contact_details.get('phoneNumbers',[])
		    message_handles = contact_details.get('instantMessageHandles',[])
                    if address and not address_list:
                        address_list = self.parse_list(address, 'fmt_address','')
                        if not address_list: address_list = self.parse_list(address, 'rawAddress','')
                    if phone_number and not phone_number_list:
                        phone_number_list = self.parse_list(phone_number, 'text','type')
		    if message_handles and not message_handles_list:
			message_handles_list = self.parse_list(message_handles, 'text','type')
                    if emails and not emails_list:
                        emails_list = self.parse_list(emails, 'text','')
                    if websites and not websites_list:
                        websites_list = self.parse_list(websites, 'text','name')
            if not first_name:
                first_name = discovery.get('viewee',{}).get('firstName','')
                lastName = discovery.get('viewee',{}).get('lastName','')
	    member_posts  = []

	    if megaphone_articles:
	    	if not name:name = megaphone_articles.get("formattedInfluencerFullName" ,'')
		mega_basic = megaphone_articles.get('basic_info',{})
		if mega_basic:
		    if not member_headline: member_headline = mega_basic.get("memberHeadline",'')
		    if not member_id: member_id = mega_basic.get('memberID','')
		member_followers = str(megaphone_articles.get('followers',{}).get('numberFollowers',''))
		if not number_of_connections: number_of_connections = str(megaphone_articles.get('distance',{}).get('numberOfConnections',''))
                inner_mega = megaphone_articles.get("megaphone_articles",{})
                if inner_mega:
                    member_post_url = inner_mega.get('readerPostsUrl','')
                    member_posts = inner_mega.get('articles',[])

            member_pview_url = all_keys.get('browse_map',{}).get("url_current_profile_view",'')
            endore_member_pic =  endorsements.get('recosMpr', {}).get('viewee',{}).get('pictureID','')
            if endore_member_pic: endore_member_pic = "%s%s"%("https://media.licdn.com/mpr/mpr/shrink_100_100",endore_member_pic)
            if another_basic_info:
                if not member_headline: member_headline = another_basic_info.get("memberHeadline",'')
                if not member_id: member_id = another_basic_info.get('memberID','')
            memb_intere_lists = []
            if additional_info:
                add_inner = additional_info.get('additional_info',{}).get('interestsList',[])
                add_distacne = additional_info.get('distance',{})
                if add_distacne:
                    if not number_of_connections: number_of_connections = str(add_distacne.get('numberOfConnections',''))
                for adin in add_inner:
                    inter = adin.get('interests_highlight','')
                    if inter:
                        memb_intere_lists.append(inter)
            if memb_intere_lists: memb_intere_lists = ', '.join(memb_intere_lists)
            else: memb_intere_lists = ''

	    if name:
		linkedin_meta = Linkedinmeta()
		linkedin_meta['sk'] = self.normalize(sk)
		linkedin_meta['profile_url'] = self.normalize(ref_url)
		linkedin_meta['profileview_url'] = self.normalize(member_pview_url)
		linkedin_meta['name'] = self.normalize(name)
		linkedin_meta['first_name'] = self.normalize(first_name)
		linkedin_meta['last_name'] = self.normalize(lastName)
		linkedin_meta['member_id'] = self.normalize(str(member_id))
		linkedin_meta['headline'] = self.normalize(member_headline)
		linkedin_meta['no_of_followers'] = self.normalize(str(member_followers))
		linkedin_meta['profile_post_url'] = self.normalize(member_post_url)
		linkedin_meta['summary'] = self.normalize(summart_des.replace('<br>','').replace('</br>',''))
		linkedin_meta['number_of_connections'] = self.normalize(str(number_of_connections))
		linkedin_meta['industry'] = self.normalize(industry)
		linkedin_meta['location'] = self.normalize(location)
		linkedin_meta['languages'] = self.normalize(lang_list)
		linkedin_meta['emails'] = self.normalize(emails_list)
		linkedin_meta['websites'] = self.normalize(websites_list)
		linkedin_meta['addresses'] = self.normalize(address_list)
		linkedin_meta['message_handles'] = self.normalize(message_handles_list)
		linkedin_meta['phone_numbers'] = self.normalize(phone_number_list)
		linkedin_meta['birthday'] = self.normalize(str(birthday))
		linkedin_meta['birth_year'] = self.normalize(str(birthyear))
		linkedin_meta['birth_month'] = self.normalize(str(birthmonth))
		linkedin_meta['twitter_accounts'] = self.normalize(twitters_list)
		linkedin_meta['profile_image'] = self.normalize(endore_member_pic)
		linkedin_meta['interests'] = self.normalize(memb_intere_lists)
		yield linkedin_meta

		if member_posts:
		    for mep in member_posts:
			post_image = mep.get('image','')
			if not post_image: post_image = mep.get('imageUrl','')
			post_title = mep.get('title','')
			if not post_title: post_title = mep.get('truncatedTitle','')
			post_author_id = str(mep.get('authorId',''))
			post_url = mep.get('dynamicPostUrl','')	
			sk_post = str(mep.get('articleId',''))
			post_state = mep.get('state','')
			post_date = mep.get('formattedPublishedDate','')#November 25, 2016
			post_date = mep.get('publishDateAsString','')#Fri Nov 25 13:47:11 UTC 2016
			if not post_date: post_date = str(mep.get('publishedDate',''))#1480081631000
			if not post_date: post_date = str(mep.get('publishDate',''))#1480081631000
			linkedin_posts_ = Linkedinposts()
			linkedin_posts_['sk'] = self.normalize(self.md5("%s%s%s%s%s"%(sk_post, post_title, sk, post_date, post_state)))
			linkedin_posts_['profile_sk'] = self.normalize(sk)
			linkedin_posts_['post_url'] = self.normalize(post_url)
			linkedin_posts_['post_image'] = self.normalize(post_image)
			linkedin_posts_['post_title'] = self.normalize(post_title)
			linkedin_posts_['post_author_id'] = self.normalize(post_author_id)
			linkedin_posts_['post_state'] = self.normalize(post_state)
			linkedin_posts_['post_date'] = self.normalize(post_date)
			linkedin_posts_['post_article_id'] = self.normalize(sk_post)
			yield linkedin_posts_


	    """if education:
		top_edu = education.get('educationsMpr',{}).get('topEducations',[])
		if top_edu:
		    top_edu_school = top_edu.get('schoolName','')
		    top_edu_field = top_edu.get('fieldOfStudy','')
		    top_edu_degree = top_edu.get('degree','')"""

	    if course_recommendations:
		course_inner = course_recommendations.get('courseRecommendations',[])
		for cor in course_inner:
		    cor_title = cor.get('courseTitle','')
		    if not cor_title: cor_title = cor.get('fmt_course_title','')
		    cor_dur_hrs = str(cor.get('durationHours',''))
		    cor_dur_mins = str(cor.get('durationMinutes',''))
		    cor_dur_sec = str(cor.get('durationSeconds',''))
		    cor_viewers = str(cor.get('fmt_viewers',''))
		    if not cor_viewers : cor_viewers = str(cor.get('numViewers',''))
		    cor_image_url = cor.get('courseImageUrl','')
		    cor_url = cor.get('courseUrl','')
		    if 'http' not in cor_url and cor_url: cor_url = "%s%s"%(self.domain,cor_url)
		    linkedin_cour_ = Linkedincourserecom()
		    linkedin_cour_['sk'] = self.md5("%s%s%s%s%s"%(cor_title, sk, cor_viewers, cor_image_url, cor_url))
		    linkedin_cour_['profile_sk'] = self.normalize(sk)
		    linkedin_cour_['course_title'] = self.normalize(cor_title)
		    linkedin_cour_['duration_seconds'] = self.normalize(cor_dur_sec)
		    linkedin_cour_['duration_minutes'] = self.normalize(cor_dur_mins)
		    linkedin_cour_['duration_hrs'] = self.normalize(cor_dur_hrs)
		    linkedin_cour_['no_of_viewers'] = self.normalize(cor_viewers)
		    linkedin_cour_['course_image'] = self.normalize(cor_image_url)
		    linkedin_cour_['course_url'] = self.normalize(cor_url)
		    if linkedin_cour_['course_title']: yield linkedin_cour_


	    if voluneetering:
		volunter_inner = voluneetering.get('volunteer',{})
		if volunter_inner:
		    volun_interests = volunter_inner.get('volunteerInterests',{}).get('supportedPreDefinedCauses',[])
		    volun_interests = ''.join(volun_interests)
		    volun_experiences = volunter_inner.get('volunteerExperiences',[])
		    for volu in volun_experiences:
			vol_single_date_iso = volu.get('single_date_iso','')
			vol_role = volu.get('role','')
			vol_cause = volu.get('lookup_vc_1','')
			if not vol_cause: vol_cause = volu.get('cause','')
			vol_desc = volu.get('summary_lb','')
			vol_start_date_month = str(volu.get('startDate',{}).get('month',''))
			vol_start_date_year = str(volu.get('startDate',{}).get('year',''))
			vol_org_name = volu.get('organization',{}).get('name','')
			if not vol_org_name: vol_org_name = volu.get('organization',{}).get('company_name','')
			vol_media_logo = volu.get('organization',{}).get('media_logo','')
			vol_company_id = str(volu.get('organization',{}).get('companyID',''))
			vol_id = str(volu.get('id',''))
			linkedin_volun_ = Linkedinvolunteerexp()
			linkedin_volun_['sk'] = self.md5("%s%s%s%s%s"%(sk,volun_interests, vol_desc, vol_cause, vol_org_name))
			linkedin_volun_['profile_sk'] = self.normalize(sk)
			linkedin_volun_['volunteer_interests'] = self.normalize(volun_interests)
			linkedin_volun_['volunteer_role'] = self.normalize(vol_role)
			linkedin_volun_['volunteer_cause'] = self.normalize(vol_cause)
			linkedin_volun_['organization_name'] = self.normalize(vol_org_name)
			linkedin_volun_['organization_logo'] = self.normalize(vol_media_logo)
			linkedin_volun_['description'] = self.normalize(vol_desc)
			linkedin_volun_['start_date_year'] = self.normalize(vol_start_date_year)
			linkedin_volun_['start_date_month'] = self.normalize(vol_start_date_month)
			linkedin_volun_['volunteer_date'] = self.normalize(vol_single_date_iso)
			if linkedin_volun_['volunteer_role'] or linkedin_volun_['volunteer_cause'] or linkedin_volun_['organization_name']: yield linkedin_volun_

            if organizations:
                inner_org = organizations.get('orgsMpr', {}).get('organizations', [])
                for org in inner_org:
                    org_occupation_name = org.get('occupationName', '')
                    org_position = org.get('positionString', '')
                    if not org_position:
                        org_position = org.get('fmt_highlight_keyword_4', '')
                    org_ended_dateiso = org.get('enddate_iso', '')
                    org_st_dateiso = org.get('startdate_iso', '')
                    org_st_datemy = org.get('startdate_my', '')
                    org_end_datemy = org.get('enddate_my', '')
                    org_name = org.get('name', '')
                    if not org_name:
                        prg_name = org.get('fmt__keyword_highlight', '')
                    org_desc = org.get('desc', '')
		    linkedin_org_ = Linkedinorganizations()
		    linkedin_org_['sk'] = self.md5("%s%s%s%s%s"%(sk, org_name, org_position, org_st_dateiso, org_desc))
		    linkedin_org_['profile_sk'] = self.normalize(sk)
		    linkedin_org_['name'] = self.normalize(org_name)
		    linkedin_org_['position'] = self.normalize(org_position)
		    linkedin_org_['start_date'] = self.normalize(org_st_dateiso)
		    linkedin_org_['end_date'] = self.normalize(org_ended_dateiso)
		    linkedin_org_['description']  = self.normalize(org_desc)
	 	    linkedin_org_['occupation_name'] = self.normalize(org_occupation_name)
		    if linkedin_org_['name'] or linkedin_org_['position']: yield linkedin_org_

                    
                    
            if honors:
                inn_honors = honors.get('honorsMpr', {}).get('honors', [])
                for hon in inn_honors:
                    hon_issuer = hon.get('issuer', '')
                    if not hon_issuer:
                        hon_issuer = hon.get('issuerHighlight', '')
                    hon_title = hon.get('title', '')
                    if not hon_title:
                        hon_title = hon.get('titleHighlight', '')
                    hon_desc = hon.get('descriptionString', '')
                    if not hon_desc:
                        hon_desc = hon.get('summary_lb', '')
                    hon_id = str(hon.get('id', ''))
                    hon_occupathion = hon.get('occupationString', '')
		    hon_on = hon.get('mdydate','')#March 2015
		    linkedin_hon_ = Linkedinhonors()
		    linkedin_hon_['sk']  = self.md5("%s%s%s%s%s%s"%(sk, hon_title, hon_issuer, hon_on, hon_desc, hon_id))
		    linkedin_hon_['profile_sk'] = self.normalize(sk)
		    linkedin_hon_['honor_on'] = self.normalize(hon_on)
		    linkedin_hon_['honor_issuer'] = self.normalize(hon_issuer)
		    linkedin_hon_['honor_summary'] = self.normalize(hon_desc)
		    linkedin_hon_['occupation'] = self.normalize(hon_occupathion)
		    yield linkedin_hon_

                    
            if certifications:
                inner_certifications = certifications.get('certsMpr',{}).get('certifications', [])
                for cer in inner_certifications:
                    authority = cer.get('authorityV2', {})
                    au_com_name = authority.get('name', '')
                    au_media_logo = authority.get('media_logo', '')
                    cer_name = cer.get('certificationName', '')
                    if not cer_name:
                        cer_name = cer.get('fmt__keyword_highlight', '')
                    cer_st_date = cer.get('startdate_my', '')
                    cer_id = str(cer.get('id', ''))
		    cer_dataid = str(cer.get('certificationIdData',''))
                    cer_iso_stdate = cer.get('startdate_iso', '')
		    linkedin_cer_ = Linkedincertifications()
		    linkedin_cer_['sk'] = self.md5("%s%s%s%s%s"%(sk, cer_id, cer_name, cer_iso_stdate,au_com_name))
		    linkedin_cer_['profile_sk'] = self.normalize(sk)
		    linkedin_cer_['certification_id']= self.normalize(cer_id)
		    linkedin_cer_['certification_date'] = self.normalize(cer_iso_stdate)
		    linkedin_cer_['certification_title'] = self.normalize(cer_name)
		    linkedin_cer_['certification_company_logo'] = self.normalize(au_media_logo)
		    linkedin_cer_['certification_company_name'] = self.normalize(au_com_name)
		    if cer_id or cer_name or au_media_logo: yield linkedin_cer_


            if endorsements:
            	end_inner = endorsements.get('recosMpr', {})
                rec_inner = endorsements.get('refsMpr', {})
                if end_inner:
                    giv_recommendations = end_inner.get('recommendations', [])
                    if giv_recommendations:
			for giv_recom in giv_recommendations:
			    giv_lastname = giv_recom.get('lastName', '')
                            giv_date_relationship = giv_recom.get('i18n__Date_and_Relationship', '')
                            giv_fullname = giv_recom.get('fmt__recommendeeFullName', '')
                            giv_title = giv_recom.get('title', '')
                            giv_created_date = giv_recom.get('fmt__dateRecCreated', '')#March 28, 2016
                            giv_text = giv_recom.get('text', '')
                            giv_relationship = giv_recom.get('relationship', '')
                            giv_mem_id = str(giv_recom.get('memberId', ''))
                            giv_profile_link = giv_recom.get('link__recommendeeProfileLink', '')
                            giv_recom_id = str(giv_recom.get('recommendationId', ''))
                            giv_mem_pic = giv_recom.get('mem_pic', '')
                            giv_first_name = giv_recom.get('firstName', '')
                            giv_created_at = str(giv_recom.get('createdDate', ''))#epoch
			    linkedin_give_rec_ = Linkedingivenrecommendations()
			    linkedin_give_rec_['sk'] = self.md5("%s%s%s%s%s%s%s"%(sk, giv_lastname, giv_fullname, giv_text, giv_title, giv_recom_id, giv_recom_id))
			    linkedin_give_rec_['profile_sk'] = self.normalize(sk)
		    	    linkedin_give_rec_['last_name'] = self.normalize(giv_lastname)
			    linkedin_give_rec_['name'] = self.normalize(giv_fullname)
			    linkedin_give_rec_['date_and_relationship'] = self.normalize(giv_date_relationship)
			    linkedin_give_rec_['title'] = self.normalize(giv_title)
			    linkedin_give_rec_['created_date'] = self.normalize(giv_created_date)
			    linkedin_give_rec_['summary'] = self.normalize(giv_text)
			    linkedin_give_rec_['profile_image'] =  self.normalize(giv_mem_pic)
			    linkedin_give_rec_['profile_member_id'] = self.normalize(giv_mem_id)
			    linkedin_give_rec_['profile_url'] = self.normalize(giv_profile_link)
			    linkedin_give_rec_['recommendation_id'] = self.normalize(giv_recom_id)
			    if giv_lastname or giv_fullname or giv_title or giv_mem_id or giv_recom_id: yield linkedin_give_rec_

			    
                if rec_inner:
                    rec_lst = rec_inner.get('results', [])
                    for rec_ref in rec_lst:
			rec_role = rec_ref.get('role','')
			rec_references = rec_ref.get('references',[])
			rec_organization = rec_ref.get('organization','')
			if rec_references:
			    for rein in rec_references:
				rec_refer_dic = rein.get('referrer',{})
				rec_fmt_Datec = rec_refer_dic.get('fmt__dateReferenceCreated','')#June 3, 2016
				rec_date_rela = rec_refer_dic.get('i18n__Date_and_Relationship','')
				rec_mem_pic = rec_refer_dic.get('mem_pic','')
				rec_name_full = rec_refer_dic.get('fmt__referrerfullName','')
				rec_profile_link = rec_refer_dic.get('link__referrerProfileLink', '')
                                rec_headline = rec_refer_dic.get('headline', '')
                                rec_memid = str(rec_refer_dic.get('memberID', ''))
				rec_id = str(rein.get('id', ''))
                                rec_text = rein.get('text', '')
                                rec_relationship = rein.get('relationship', '')
				linkedin_rec_ = Linkedinrecrecommendations()
				linkedin_rec_['sk'] = self.md5("%s%s%s%s%s%s%s"%(sk, rec_role, rec_id, rec_fmt_Datec, rec_date_rela, rec_profile_link, rec_mem_pic))
				linkedin_rec_['profile_sk'] = self.normalize(sk)
				linkedin_rec_['role'] = self.normalize(rec_role)
				linkedin_rec_['profile_member_id'] = self.normalize(rec_memid)
				linkedin_rec_['id'] = self.normalize(rec_id)
				linkedin_rec_['edu_start_date'] = ''
				linkedin_rec_['name'] = self.normalize(rec_name_full)
				linkedin_rec_['organization'] = self.normalize(rec_organization)
				linkedin_rec_['created_date'] = self.normalize(rec_fmt_Datec)
				linkedin_rec_['date_and_relationship'] = self.normalize(rec_date_rela)
				linkedin_rec_['headline'] = self.normalize(rec_headline)
				linkedin_rec_['profile_url'] = self.normalize(rec_profile_link)
				linkedin_rec_['profile_image'] = self.normalize(rec_mem_pic)
				linkedin_rec_['summary'] = self.normalize(rec_text)
				if rec_id or rec_name_full or rec_headline or rec_mem_pic or rec_role:yield linkedin_rec_

	    if groups:
		inner_groups = groups.get('groups',[])
		for ing in inner_groups:
		    grp_id = ing.get('groupID','')
		    grp_link = ing.get('link_groups','')
		    grp_members = ing.get('fmt_numMembers','')
		    if not grp_members:
			grp_members = ing.get('i18n_numMembers','')
		    grp_name = ing.get('name','')
		    grp_logo = ing.get('link_media','')
		    if grp_link and 'http' not in grp_link: grp_link = "%s%s"%(self.domain,grp_link)
		    linkedin_groups_ = Linkedingroups()
		    linkedin_groups_['sk'] = self.md5("%s%s%s%s%s"%(sk, grp_link, grp_name, grp_members, grp_id))
		    linkedin_groups_['profile_sk'] = self.normalize(sk)
		    linkedin_groups_['group_link'] = self.normalize(grp_link)
		    linkedin_groups_['group_name'] = self.normalize(grp_name)
		    linkedin_groups_['no_of_members'] = self.normalize(grp_members)
		    linkedin_groups_['group_logo'] = self.normalize(grp_logo)
		    linkedin_groups_['group_id'] = self.normalize(str(grp_id))
		    if grp_link or grp_name or grp_members or grp_id: yield linkedin_groups_


	    if following:
		compan_follow = following.get('follow',{})
	        influencers = following.get('follow_people',{}).get('influencers',[])
		foll_schools = following.get('follow_school',{}).get('schoolFollowees',[])
		foll_schools_counts = str(following.get('follow_school', {}).get('schoolFolloweeCount',''))
	  	foll_channels = following.get('follow_channels',{}).get('channels',[])
		if foll_channels:
		    for foc in foll_channels:
		  	foc_followerscount = str(foc.get('followers',''))
			if not foc_followerscount: foc_followerscount = foc.get('fmt_following_count','')
			foc_channel_dic = foc.get('channel',{})
			if foc_channel_dic:
			   foc_name = foc_channel_dic.get('title','')
			   if not foc_name: foc_name = foc_channel_dic.get('vanityName','')
			   foc_link_channel = foc_channel_dic.get('link_channel','')
			   if foc_link_channel and 'http' not in foc_link_channel: foc_link_channel = "%s%s"%(self.domain, foc_link_channel)
			   foc_image = foc_channel_dic.get('link_channel_image','')
			   foc_id = str(foc_channel_dic.get('id',''))
			   linkedin_foc_ = Linkedinfollowchannels()
			   linkedin_foc_['sk'] = self.md5("%s%s%s%s%s"%(sk, foc_followerscount, foc_name, foc_link_channel, foc_image))
			   linkedin_foc_['profile_sk'] = self.normalize(sk)
			   linkedin_foc_['channel_followers'] = self.normalize(foc_followerscount)
			   linkedin_foc_['channel_title'] = self.normalize(foc_name)
			   linkedin_foc_['channel_link'] =self.normalize(foc_link_channel)
			   linkedin_foc_['channel_image'] = self.normalize(foc_image)
			   if linkedin_foc_['channel_title']: yield linkedin_foc_
			
		if influencers:
    		    for inf in influencers:
			inf_titf = inf.get('_memberFullName','')
			if not inf_titf: inf_titf = inf.get('fmtFullName','')
			inf_profile_url = inf.get('profileUrl','')
			inf_last_name  = inf.get('lastName','')
			inf_first_name = inf.get('firstName','')
			inf_id = str(inf.get('id',''))	
		   	inf_headline = inf.get('headline','')
			inf_member_logo = inf.get('partial',{}).get('media_picture_link_400','')
			linkedin_inf_ = Linkedinfollowinfluencers()
			linkedin_inf_['sk'] = self.md5("%s%s%s%s%s"%(inf_titf, sk, inf_profile_url, inf_id, inf_headline))
			linkedin_inf_['profile_sk'] = self.normalize(sk)
			linkedin_inf_['inflencer_name'] = self.normalize(inf_titf)
			linkedin_inf_['influencer_firstname'] = self.normalize(inf_first_name)
			linkedin_inf_['influencer_lastname'] = self.normalize(inf_last_name)
			linkedin_inf_['influencer_image'] = self.normalize(inf_member_logo)
			linkedin_inf_['influencer_profile_url'] = self.normalize(inf_profile_url)
			linkedin_inf_['influencer_headline'] = self.normalize(inf_headline)
			if linkedin_inf_['inflencer_name']: yield linkedin_inf_


		if foll_schools:
		    for scf in foll_schools:
			sch_image = scf.get('_partial__school_image',{}).get('media_picture_link_400','')
		  	if not sch_image: sch_image = scf.get('_partial__school_image',{}).get('media_picture_link','')
			sch_region = scf.get('geoRegion','')
			sch_link = scf.get('link_school','')
			sch_name = scf.get('canonicalName','')
			sch_id = str(scf.get('id',''))
			if sch_link:
			    if 'http' not in sch_link: sch_link = "%s%s"%(self.domain,sch_link)
			linkedin_scho_ = Linkedinfollowschools()
			linkedin_scho_['sk'] = self.md5("%s%s%s%s%s"%(sk, sch_image, sch_name, sch_id, sch_region))
			linkedin_scho_['profile_sk'] = self.normalize(sk)
			linkedin_scho_['school_name'] = self.normalize(sch_name)
			linkedin_scho_['school_image'] = self.normalize(sch_image)
			linkedin_scho_['school_region'] = self.normalize(sch_region)
			linkedin_scho_['school_link'] = self.normalize(sch_link)
			linkedin_scho_['total_followee_count'] = self.normalize(str(foll_schools_counts))	
			if sch_name or sch_region : yield linkedin_scho_

	

	        if compan_follow:
		    get_allc = compan_follow.get('getAllCompaniesUrl','')
		    if not get_allc: get_allc = "https://www.linkedin.com/profile/profile-v2-follow-companies?id=%s&count=-1"%(memb_id)
		    if 'http' not in get_allc: get_allc = "%s%s"%(self.domain, get_allc)
		    if get_allc:
			yield Request(get_allc, callback=self.parse_allcompanies, meta={"sk":sk,"ref_url":ref_url,"memb_id":memb_id,"linkedin_auth":linkedin_auth})
		    
		
	    if experience:
		postitions = experience.get('positionsMpr',{}).get('positions',[])
		for pos in postitions:
		    pos_fmt_location = pos.get('fmt_location','') 
		    pos_company_name = pos.get('companyName','')
		    if not pos_company_name:pos_company_name = pos.get('company_name','')
		    pos_title = pos.get('title','')
		    if not pos_title: pos_title = pos.get('title_highlight','')
		    pos_cpny_url = pos.get('biz_prof','')
		    if not pos_cpny_url: pos_cpny_url = pos.get('biz_prof_v2','')
		    if pos_cpny_url and 'http' not in pos_cpny_url:pos_cpny_url = "%s%s"%(self.domain,pos_cpny_url)
		    pos_enddate_iso = pos.get('enddate_iso','')
		    pos_summary = pos.get('summary_lb','')
		    pos_startdate_iso = pos.get('startdate_iso','')
		    pos_fmt_duration = pos.get('fmt_duration','')
		    pos_media_image = pos.get('media_logo','')
		    pos_end_date = str(pos.get('endDate',{}).get('asDate',''))
		    pos_end_year = str(pos.get('endDate',{}).get('year',''))
		    pos_end_month = str(pos.get('endDate',{}).get('month',''))
		    #formatend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pos_end_date)/1000))
		    pos_start_date = str(pos.get('startDate',{}).get('asDate',''))
		    pos_start_year = str(pos.get('startDate',{}).get('year',''))
		    pos_start_month = str(pos.get('startDate',{}).get('month',''))
		    pos_company_id = str(pos.get('companyId',''))
		    pos_position_id = str(pos.get('positionId',''))
		    #formatstart  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pos_start_date)/1000))
		    linkedin_epx_ = Linkedinexperiences()
		    linkedin_epx_['sk']= self.md5("%s%s%s%s%s%s"%(sk, pos_fmt_location, pos_position_id, pos_company_id, pos_startdate_iso, pos_summary))
		    linkedin_epx_['profile_sk'] = self.normalize(sk)
		    linkedin_epx_['exp_location'] = self.normalize(pos_fmt_location)
		    linkedin_epx_['exp_company_name'] = self.normalize(pos_company_name)
		    linkedin_epx_['exp_company_url'] = self.normalize(pos_cpny_url)
		    linkedin_epx_['exp_title']  =self.normalize(pos_title)
		    linkedin_epx_['start_date'] = self.normalize(pos_startdate_iso)
		    linkedin_epx_['end_date'] = self.normalize(pos_enddate_iso)
		    linkedin_epx_['exp_company_logo'] = self.normalize(pos_media_image)
		    linkedin_epx_['exp_duration'] = self.normalize(pos_fmt_duration)
		    linkedin_epx_['exp_company_id'] = self.normalize(pos_company_id)
		    linkedin_epx_['exp_position_id'] = self.normalize(pos_position_id)
		    linkedin_epx_['exp_summary'] = self.normalize(pos_summary)
		    if pos_title or pos_cpny_url or pos_fmt_location: yield linkedin_epx_

		    """pos_associated_proj = pos.get('associatedWith',{}).get('projects',{}).get('items',[])
		    for projp in pos_associated_proj:
			pos_items_tit = projp.get('title','')
			pos_items_desc = projp.get('desc','').replace('\n','')"""

	    if education:
		educations_inner = education.get('educationsMpr',{}).get('educations',[])
		for eduin in educations_inner:
		    edu_name = eduin.get('fmt__school_highlight','')
		    if not edu_name: edu_name = eduin.get('schoolName','')
		    edu_degree = eduin.get('degree','')
		    if not edu_degree:edu_degree = eduin.get('fmt__degree_highlight','')
		    edu_field_ofstdy = eduin.get('fieldOfStudy','')
		    if not edu_field_ofstdy:
			edu_ofstdy = eduin.get('fosList',[])
			if edu_ofstdy:
			    edu_field_ofstdy = self.parse_list(edu_ofstdy, 'name','')
		    edu_schoologo = eduin.get('school_logo',{}).get('media_picture_link','')
		    edu_start_date_my = eduin.get('startdate_my','')#year
		    edu_enddate_my = eduin.get('enddate_my','')
		    edu_start_date = str(eduin.get('startDate',{}).get('asDate',''))
		    edu_start_year = str(eduin.get('startDate',{}).get('year',''))
		    edu_start_month = str(eduin.get('startDate',{}).get('month',''))
		    formatedustart = ''
		    if edu_start_date: formatedustart = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(edu_start_date)/1000)))
		    edu_end_date = str(eduin.get('endDate',{}).get('asDate',''))
		    formatedusend = ''
		    if edu_end_date: formatedusend = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(edu_end_date)/1000)))
		    edu_end_year = str(eduin.get('endDate',{}).get('year',''))
		    edu_end_month = str(eduin.get('endDate',{}).get('month',''))
		    edu_id = str(eduin.get('educationId',''))
		    edu_scho_id = str(eduin.get('schoolId',''))
		    linkedin_educations_ = Linkedineducations()
		    linkedin_educations_['sk'] = self.md5("%s%s%s%s%s%s"%(sk, edu_degree, edu_field_ofstdy, edu_name, edu_id, edu_scho_id))
		    linkedin_educations_['profile_sk'] = self.normalize(sk)
		    linkedin_educations_['edu_start_year'] = self.normalize(edu_start_year)
		    linkedin_educations_['edu_start_month'] = self.normalize(edu_start_month)
		    linkedin_educations_['edu_start_date'] = self.normalize(formatedustart)
		    linkedin_educations_['edu_end_year'] = self.normalize(edu_end_year)
		    linkedin_educations_['edu_end_date'] = self.normalize(formatedusend)
		    linkedin_educations_['edu_end_month'] = self.normalize(edu_end_month)
		    linkedin_educations_['edu_degree'] = self.normalize(edu_degree)
		    linkedin_educations_['edu_field_of_study'] = self.normalize(edu_field_ofstdy)
		    linkedin_educations_['edu_school_name'] = self.normalize(edu_name.replace('&#39;',''))
		    linkedin_educations_['school_logo'] = self.normalize(edu_schoologo)
		    linkedin_educations_['post_article_id'] = ''
		    linkedin_educations_['education_id'] = self.normalize(edu_id)
		    linkedin_educations_['school_id'] = self.normalize(edu_scho_id)
		    if edu_degree or edu_field_ofstdy or edu_name: yield linkedin_educations_

            if skills:
		skills_inner = skills.get('skillsMpr',{}).get('skills',[])
		for ski in skills_inner:
		    ski_name = ski.get('fmt__skill_name','')
		    if not ski_name: ski_name = ski.get('name','')
		    ski_endo_count = str(ski.get('endorsementCount',''))
		    if not ski_endo_count: ski_endo_count = ski.get('i18n_count_display','')
		    ski_id = str(ski.get('id',''))
	  	    member_topic_url = ski.get('url_userpMemberTopic','')	
		    public_topic_url = ski.get('url_userpPublicTopic','')
		    linkedin_ski_ = Linkedinskills()
		    linkedin_ski_['sk'] = self.md5("%s%s%s%s"%(sk, ski_name, ski_endo_count, public_topic_url))
		    linkedin_ski_['profile_sk']= self.normalize(sk)
		    linkedin_ski_['skill_name'] = self.normalize(ski_name)
		    linkedin_ski_['endoresement_count'] = self.normalize(ski_endo_count)
		    linkedin_ski_['member_topic_skill_url'] = self.normalize(member_topic_url)
		    linkedin_ski_['public_topic_skill_url'] = self.normalize(public_topic_url)
		    if ski_name: yield linkedin_ski_

	


		

            if projects:
		projects_inner = projects.get('projectsMpr',{}).get('projects',[])
		for proj in projects_inner:
		    pro_single_date = proj.get('single_date_iso','')
		    pro_team_mates = str(proj.get('numContributors',''))
		    pro_occp_name = proj.get('occupationName','')
		    pro_title = proj.get('title','')
		    if not pro_title: pro_title = proj.get('proj_title','')
		    pro_desc = proj.get('desc','')
		    pro_url = proj.get('URL','')
		    if not pro_url: pro_url = proj.get('proj_url','')
		    if pro_url and 'http' not in pro_url: pro_url = "%s%s"%(self.domain, pro_url)
		    pro_startdate_iso = proj.get('startdate_iso','')
		    pro_enddate_iso = proj.get('enddate_iso','')
		    pro_end_datm = proj.get('enddate_my','')
		    pro_id = str(proj.get('id',''))
		    pro_start_datm = proj.get('startdate_my','')
		    pro_hidden_con = str(proj.get('numHiddenContributors',''))
		    pro_team_members = proj.get('members',[])
		    team_mates_list = []
		    for prot in pro_team_members:
			pro_team_url = prot.get('pview','')
			pro_team_name = prot.get('formatted_name','')
			pro_team_headline = prot.get('headline','')
		  	pro_team_image = prot.get('mem_pic','')
			pro_team_memid = prot.get('memberID','')
			if pro_team_name: team_mates_list.append(pro_team_name)
		    if team_mates_list: team_mates_list = ', '.join(team_mates_list)
		    else: team_mates_list = ''
		    linkedin_proj_ = Linkedinprojects()
		    linkedin_proj_['sk'] = self.md5("%s%s%s%s%s"%(sk,pro_title, pro_url, pro_desc, pro_team_mates))
		    linkedin_proj_['profile_sk'] = self.normalize(sk)
		    linkedin_proj_['project_date'] = self.normalize(pro_single_date)
		    linkedin_proj_['number_of_project_members'] = self.normalize(pro_team_mates)
		    linkedin_proj_['project_member_names'] = self.normalize(team_mates_list)
		    linkedin_proj_['project_occupation_name'] = self.normalize(pro_occp_name)
		    linkedin_proj_['project_title'] = self.normalize(pro_title)
		    linkedin_proj_['project_url']  = self.normalize(pro_url)
		    linkedin_proj_['project_start_date'] = self.normalize(pro_startdate_iso)
		    linkedin_proj_['project_end_date'] = self.normalize(pro_enddate_iso)
		    linkedin_proj_['project_description'] = self.normalize(pro_desc)
		    if linkedin_proj_['project_title'] or linkedin_proj_['project_description'] : yield linkedin_proj_

		   
		
    def parse_list(self, varlist, key, typef):
	vars_list = []
	typef = ''
	for em in varlist:
		id_ = em.get(key,'')
		if typef: typ = em.get(typef,'')
		if typef: id_ = "{}{}{}".format(id_,':-',typef)
		vars_list.append(id_)
	return ', '.join(vars_list)

    def parse_allcompanies(self, response):
	temp = json.loads(response.body)
	sk = response.meta.get('sk','')
	followingcomp = temp.get('content',{}).get('Following',{})
	if followingcomp:
	   companies_count = followingcomp.get('companyFolloweeCount','')
	   companieslist = followingcomp.get('companyFollowees',[])
	   for lc in companieslist:
		comp_lookup = lc.get('ind_lookup','')
		comp_logo = lc.get('logo','')
		comp_id = str(lc.get('id',''))
		comp_canonicalname = lc.get('canonicalName','')
		comp_universalname = lc.get('universalName','')
		comp_link = lc.get('link_biz','')
		if comp_link:
		    if 'http' not in comp_link: comp_link = "%s%s"%(self.domain,comp_link)
		linkedin_comp_ = Linkedinfollowcompanies()
		linkedin_comp_['sk'] = self.md5("%s%s%s%s%s"%(sk, comp_canonicalname, comp_logo, comp_link, companies_count))
		linkedin_comp_['profile_sk'] = self.normalize(sk)
		linkedin_comp_['company_canonical_name'] =  self.normalize(comp_canonicalname)
		linkedin_comp_['total_followee_count'] = self.normalize(str(companies_count))
		linkedin_comp_['company_logo'] = self.normalize(comp_logo)
		linkedin_comp_['company_universal_name'] = self.normalize(comp_universalname)
		linkedin_comp_['company_url'] = self.normalize(comp_link)
		if linkedin_comp_['company_canonical_name'] or linkedin_comp_['company_universal_name']: yield linkedin_comp_
			
					
		
		
	
	    



	

