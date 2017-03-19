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
from scrapy.xlib.pydispatch import dispatcher
from linkedin_queries import *


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
	#get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 limit 5"
	pattern_search = "%"+"2017-03-16"+"%"
	patter_url = "%"+"prrashi/"+"%"
	get_query_param = 'select sk, url, meta_data, crawl_status from linkedin_crawl where created_at like "%s" and url like "%s" limit 1'%(pattern_search,patter_url)
	#self.cur.execute(get_query_param)
	#self.profiles_list = [i for i in self.cur.fetchall()]
	self.profiles_list = [('aaaaa','https://www.linkedin.com/in/rajaemmela/','{}'),('bbbb','https://www.linkedin.com/in/aravindrajanm/','{}'),('cccc','https://www.linkedin.com/in/prrashi/','{}'),('dddd','https://www.linkedin.com/in/karthikbalait/','{}'),('eeee','https://www.linkedin.com/in/prashanthazharuddin/','{}'),('ffff',"https://www.linkedin.com/in/phanipriya/",'{}')]
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
            vals = (sk, li[1], sk, li[1])
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
	    #self.cur.execute(update_get_params%(9,sk))
	    yield Request(req_url, callback=self.parse_ajax,meta={"sk":sk,"ref_url":response.url,"memb_id":memb_id,"linkedin_auth":linkedin_auth})

    def parse_ajax(self, response):
	temp = json.loads(response.body)
 	all_keys = temp.get('content',{})
	sk = response.meta.get('sk','')
	ref_url = response.meta.get('ref_url','')
	memb_id = response.meta.get('memb_id','')
	linkedin_auth = response.meta.get('linkedin_auth','')
	first_name, lastName, name = ['']*3
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
	    if additional_info:
		add_inner = additional_info.get('additional_info',{}).get('interestsList',[])
		for adin in add_inner:
		    inter = adin.get('interests_highlight','')

	    if course_recommendations:
		course_inner = course_recommendations.get('courseRecommendations',[])
		for cor in course_inner:
		    cor_title = cor.get('courseTitle','')
		    if not cor_title: cor_title = cor.get('fmt_course_title','')
		    cor_dur_hrs = cor.get('durationHours','')
		    cor_dur_mins = cor.get('durationMinutes','')
		    cor_viewers = cor.get('fmt_viewers','')
		    if not cor_viewers : cor_viewers = str(cor.get('numViewers',''))
		    cor_image_url = cor.get('courseImageUrl','')
		    cor_url = cor.get('courseUrl','')
		    if 'http' not in cor_url and cor_url: cor_url = "%s%s"%(self.domain,cor_url)
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
			vol_start_date_month = volu.get('startDate',{}).get('month','')
			vol_start_date_year = volu.get('startDate',{}).get('year','')
			vol_org_name = volu.get('organization',{}).get('name','')
			if not vol_org_name: vol_org_name = volu.get('organization',{}).get('company_name','')
			vol_media_logo = volu.get('media_logo','')
				
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
                    hon_id = hon.get('id', '')
                    hon_occupathion = hon.get('occupationString', '')
                    
                    
            if certifications:
                inner_certifications = certifications.get('certifications', [])
                for cer in inner_certifications:
                    authority = cer.get('authorityV2', {})
                    au_com_name = authority.get('name', '')
                    au_media_logo = authority.get('media_logo', '')
                    cer_name = cer.get('certificationName', '')
                    if not cer_name:
                        cer_name = cer.get('fmt__keyword_highlight', '')
                    cer_st_date = cer.get('startdate_my', '')
                    cer_id = cer.get('id', '')
                    cer_iso_stdate = cer.get('startdate_iso', '')
                    
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
                            giv_created_date = giv_recom.get('fmt__dateRecCreated', '')
                            giv_text = giv_recom.get('text', '')
                            giv_relationship = giv_recom.get('relationship', '')
                            giv_mem_id = giv_recom.get('memberId', '')
                            giv_profile_link = giv_recom.get('link__recommendeeProfileLink', '')
                            giv_recom_id = giv_recom.get('recommendationId', '')
                            giv_mem_pic = giv_recom.get('mem_pic', '')
                            giv_first_name = giv_recom.get('firstName', '')
                            giv_created_at = giv_recom.get('createdDate', '')#epoch
                if rec_inner:
                    rec_lst = rec_inner.get('results', [])
                    for rec_ref in rec_lst:
			rec_role = rec_ref.get('role','')
			rec_references = rec_ref.get('references',[])
			rec_organization = rec_ref.get('organization','')
			if rec_references:
			    for rein in rec_references:
				rec_refer_dic = rec_references.get('referrer',{})
				rec_fmt_Datec = rec_refer_dic.get('fmt__dateReferenceCreated','')
				rec_date_rela = rec_refer_dic.get('i18n__Date_and_Relationship','')
				rec_mem_pic = rec_refer_dic.get('mem_pic','')
				rec_name_full = rec_refer_dic.get('fmt__referrerfullName','')
				rec_profile_link = rec_refer_dic.get('link__referrerProfileLink', '')
                                rec_headline = rec_refer_dic.get('headline', '')
                                rec_memid = rec_refer_dic.get('memberID', '')
				rec_id = rein.get('id', '')
                                rec_text = rein.get('text', '')
                                rec_relationship = rein.get('relationship', '')
	    if groups:
		inner_groups = groups.get('groups',[])
		for ing in inner_groups:
		    grp_id = ing.get('groupID','')
		    grp_link = ing.get('link_groups','')
		    grp_members = ing.get('fmt_numMembers','')
		    grp_name = ing.get('name','')
		    grp_logo = ing.get('link_media','')

	    if following:
		compan_follow = following.get('follow',{})
	        influencers = following.get('follow_people',{}).get('influencers',[])
		foll_schools = following.get('follow_school',{}).get('schoolFollowees',[])
	  	foll_channels = following.get('follow_channels',{}).get('channels',[])
		if foll_channels:
		    for foc in foll_channels:
			foc_followerscount = foc.get('fmt_following_count','')
			foc_channel_dic = foc.get('channel',{})
			if foc_channel_dic:
			   foc_name = foc_channel_dic.get('title','')
			   foc_link_channel = foc_channel_dic.get('link_channel','')
			   if foc_link_channel and 'http' not in foc_link_channel: foc_link_channel = "%s%s"%(self.domain, foc_link_channel)
			   foc_image = foc_channel_dic.get('link_channel_image','')
			
		if influencers:
    		    for inf in influencers:
			inf_titf = inf.get('_memberFullName','')
			inf_profile_url = inf.get('profileUrl','')
			inf_last_name  = inf.get('lastName','')
			
		if foll_schools:
		    for scf in foll_schools:
		  	sch_image = scf.get('_partial__school_image',{}).get('media_picture_link','')
			sch_region = scf.get('geoRegion','')
			sch_link = scf.get('link_school','')
			sch_name = scf.get('canonicalName','')
			sch_id = scf.get('id','')
			if sch_link:
			    if 'http' not in sch_link: sch_link = "%s%s"%(self.domain,sch_link)
	

	        if compan_follow:
		    get_allc = compan_follow.get('getAllCompaniesUrl','')
		    companies_full_url = "%s%s"%(self.domain, get_allc)
		    if companies_full_url:
			yield Request(companies_full_url, callback=self.parse_allcompanies, meta={"sk":sk,"ref_url":ref_url,"memb_id":memb_id,"linkedin_auth":linkedin_auth})
		    
		
	    if experience:
		postitions = experience.get('positionsMpr',{}).get('positions',[])
		for pos in postitions:
		    pos_fmt_location = pos.get('fmt_location','') 
		    pos_company_name = pos.get('companyName','')
		    if not pos_company_name:pos_company_name = pos.get('company_name','')
		    pos_title = pos.get('title','')
		    pos_enddate_iso = pos.get('enddate_iso','')
		    pos_summary = pos.get('summary_lb','')
		    pos_startdate_iso = pos.get('startdate_iso','')
		    pos_fmt_duration = pos.get('fmt_duration','')
		    pos_media_image = pos.get('media_logo','')
		    pos_end_date = pos.get('endDate',{}).get('asDate','')
		    pos_end_year = pos.get('endDate',{}).get('year','')
		    pos_end_month = pos.get('endDate',{}).get('month','')
		    #formatend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pos_end_date)/1000))
		    pos_start_date = pos.get('startDate',{}).get('asDate','')
		    pos_start_year = pos.get('startDate',{}).get('year','')
		    pos_start_month = pos.get('startDate',{}).get('month','')
		    #formatstart  = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pos_start_date)/1000))
		    pos_associated_proj = pos.get('associatedWith',{}).get('projects',{}).get('items',[])
		    for projp in pos_associated_proj:
			pos_items_tit = projp.get('title','')
			pos_items_desc = projp.get('desc','').replace('\n','')

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
			    edu_field_ofstdy = ','.join(self.parse_list(edu_ofstdy, 'name',''))
			
		    edu_schoologo = eduin.get('school_logo',{}).get('media_picture_link','')
		    edu_start_date_my = eduin.get('startdate_my','')#year
		    edu_enddate_my = eduin.get('enddate_my','')
		    edu_start_date = eduin.get('startDate',{}).get('asDate','')
		    edu_start_year = eduin.get('startDate',{}).get('year','')
		    edu_start_month = eduin.get('startDate',{}).get('month','')
		    #formatedustart = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(edu_start_date)/1000))
		    edu_end_date = eduin.get('endDate',{}).get('asDate','')
		    #formatedusend = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(edu_end_date)/1000))
		    edu_end_year = eduin.get('endDate',{}).get('year','') 
		    edu_end_month = eduin.get('endDate',{}).get('month','')
            if skills:
		skills_inner = skills.get('skills',[])
		for ski in skills_inner:
		    ski_name = ski.get('fmt__skill_name','')
		    if not ski_name: ski_name = ski.get('name','')
		    ski_endo_count = str(ski.get('endorsementCount',''))
		    if not ski_endo_count: ski_endo_count = ski.get('i18n_count_display','')
	    if languages:
		languages_inner = languages.get('languages',{}).get('languagesData',[])
		for lani in languages_inner:
		    lan_name = lani.get('displayName','')
		    if not lan_name: lan_name = lani.get('lang','')
			
	    if basic_info:
		basic_info_inner = basic_info.get('basic_info',{})
		if basic_info_inner:
		    name = basic_info_inner.get('fullname','')
		    if not name: name = megaphone_articles.get("formattedInfluencerFullName" ,'')
		    member_id = basic_info_inner.get('memberID','')
		    industry = basic_info_inner.get('industry_highlight','')
		    location = basic_info_inner.get('location_highlight','')
		    if not location: location = basic_info_inner.get('fmt_location','')

	    if summary:
		summary_inner = summary.get('summary',{})
		if summary_inner: summart_des =summary_inner.get('summary_lb','')

            if projects:
		projects_inner = projects.get('projectsMpr',{}).get('projects',[])
		for proj in projects_inner:
		    pro_single_date = proj.get('single_date_iso','')
		    pro_team_mates = proj.get('numContributors','')
		    pro_occp_name = proj.get('occupationName','')
		    pro_title = proj.get('title','')
		    if not pro_title: pro_title = proj.get('proj_title','')
		    pro_desc = proj.get('desc','')
		    pro_url = proj.get('URL','')
		    pro_startdate_iso = proj.get('startdate_iso','')
		    pro_enddate_iso = proj.get('enddate_iso','')
		    pro_end_datm = proj.get('enddate_my','')
		    pro_start_datm = proj.get('startdate_my','')
		    pro_hidden_con = str(proj.get('numHiddenContributors',''))
		    pro_team_members = proj.get('members',[])
		    for prot in pro_team_members:
			pro_team_url = prot.get('pview','')
			pro_team_name = prot.get('formatted_name','')
			pro_team_headline = prot.get('headline','')
		  	pro_team_image = prot.get('mem_pic','')
			pro_team_memid = prot.get('memberID','')
		

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
		    
		    if websites: websites_list = self.parse_list(websites, 'URL','fmt_type')
		    if twitter_accounts: twitters_list = self.parse_list(twitter_accounts, 'twitterHandle','')
	
		if contact_details:
		    first_name = contact_details.get('firstName','')
		    lastName = contact_details.get('lastName','')
		    name = contact_details.get('name','')
		    birthday = contact_details.get('birthDay','')
		    birthmonth = contact_details.get('birthMonth','')
		    birthyear = contact_details.get('birthYear','')
		    emails = contact_details.get('emails',[])
		    websites = contact_details.get('websites',[])
		    address = contact_details.get('addresses',[])
		    phone_number = contact_details.get('phoneNumbers',[])
		    if address:
			address_list = self.parse_list(address, 'fmt_address','')
			if not address_list: address_list = self.parse_list(address, 'rawAddress','')
		    if phone_number:
			phone_number_list = self.parse_list(phone_number, 'text','type')
		    if emails:
		        emails_list = self.parse_list(emails, 'text','')
		    if websites:
			websites_list = self.parse_list(websites, 'text','name')
	    if not first_name:
		first_name = discovery.get('viewee',{}).get('firstName','')
		lastName = discovery.get('viewee',{}).get('lastName','')
	    if name:
		print first_name
		


    def parse_list(self, varlist, key, typef):
	vars_list = []
	for em in varlist:
		id_ = em.get(key,'')
		if typef: typ = em.get(typef,'')
		if typef: id_ = "{}{}{}".format(id_,':-',typef)
		vars_list.append(id_)
	return vars_list

    def parse_allcompanies(self, response):
	temp = json.loads(response.body)
	followingcomp = temp.get('content',{}).get('Following',{})
	if followingcomp:
	   companies_count = followingcomp.get('companyFolloweeCount','')
	   companieslist = followingcomp.get('companyFollowees',[])
	   for lc in companieslist:
		comp_lookup = lc.get('ind_lookup','')
		comp_logo = lc.get('logo','')
		comp_canonicalname = lc.get('canonicalName','')
		comp_universalname = lc.get('universalName','')
		comp_id = lc.get('id','')
		comp_link = lc.get('link_biz','')
		if comp_link:
		    if 'http' not in comp_link: comp_link = "%s%s"%(self.domain,comp_link)
	
				
		
		
	
	    



	

