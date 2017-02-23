from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import re
import json
import MySQLdb
import xlwt
import md5
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class linkedinBmerge(BaseSpider):
    name = "linkedin_merge"
    start_urls = ['https://www.linkedin.com/uas/login?goback=&trk=hb_signin']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999]
	
    
    def __init__(self, *args, **kwargs):
        super(linkedinBmerge, self).__init__(*args, **kwargs)
        self.ajax_one_url = "https://www.linkedin.com/profile/mappers?x-a=%2Cprofile_v2_contact_info%2Cprofile_v2_groups%2Cprofile_v2_skills%2Cprofile_v2_connections%2Cprofile_v2_follow%2Cprofile_v2_course_recommendations%2Cprofile_v2_endorsements&x-p=profile_v2_connections%2Edistance%3A1%2Ctop_card%2EprofileContactsIntegrationStatus%3A0%2Cprofile_v2_right_fixed_discovery%2Erecords%3A12%2Cprofile_v2_right_fixed_discovery%2Eoffset%3A0%2Cprofile_v2_browse_map%2EpageKey%3Anprofile_view_nonself%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_discovery%2Erecords%3A12%2Cprofile_v2_discovery%2Erecords%3A12%2Ctop_card%2Etc%3Atrue%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_summary_upsell%2EsummaryUpsell%3Atrue&x-oa=bottomAliases&id="
        self.ajax_second_url = "&locale=en_US&snapshotID=&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
        self.ajax_third_url = "&locale=en_US&snapshotID=&authToken=%s&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"

        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd = 'root')
        self.cur = self.con.cursor()
        self.selectall = 'select sk , name, aux_info, profile_url from linkedin_profiles'
        self.qry = 'insert into linkedin_profiles(sk, profile_url, aux_info, created_at, modified_at) values (%s, %s, "{}", now(), now())  on duplicate key update modified_at = now(), sk =%s, profile_url = %s, aux_info = "{}"'
        self.selectaux = 'select aux_info from linkedin_profiles where sk = "%s"'
        self.updateqry = "update linkedin_profiles set %s = '%s' where sk = '%s'"
        #header1 = ['Name', 'Profile_url', 'Phone Number', 'Email','Skills', 'Groups', 'Recommendations' , 'Following News', 'Following Companies', 'Following Influencers', 'Following Schools']
        header1 = ['Phone Number', 'Email','Skills', 'Groups', 'Recommendations' , 'Following News', 'Following Companies', 'Following Influencers', 'Following Schools']
        

        

        self.header2 = ['Linkedin', 'linkedin_firstName', 'linkedin_middleName', 'linkedin_lastName',\
            'linkedin_jobTitle', 'linkedin_company', 'linkedin_location', 'linkedin_industry',\
            'linkedin_connectionsCount', 'linkedin_summary', 'linkedin_experience1_title',\
            'linkedin_experience1_company', 'linkedin_experience1_dateStarted',\
            'linkedin_experience1_dateEnd', 'linkedin_experience1_city',\
            'linkedin_experience1_country', 'linkedin_experience2_title',\
            'linkedin_experience2_company', 'linkedin_experience2_dateStarted',\
            'linkedin_experience2_dateEnd', 'linkedin_experience2_city',\
            'linkedin_experience2_country', 'linkedin_experience3_title',\
            'linkedin_experience3_company', 'linkedin_experience3_dateStarted',\
            'linkedin_experience3_dateEnd', 'linkedin_experience3_city',\
            'linkedin_experience3_country', 'linkedin_honors1_title',\
            'linkedin_honors1_occupation', 'linkedin_honors1_issuer', 'linkedin_honors1_date',\
            'linkedin_honors1_description', 'linkedin_honors2_title', 'linkedin_honors2_occupation',\
            'linkedin_honors2_issuer', 'linkedin_honors2_date', 'linkedin_honors2_description',\
            'linkedin_honors3_title', 'linkedin_honors3_occupation', 'linkedin_honors3_issuer',\
            'linkedin_honors3_date', 'linkedin_honors3_description', 'linkedin_education1_school',\
            'linkedin_education1_dateStarted', 'linkedin_education1_dateEnd', 'linkedin_education1_degree',\
            'linkedin_education1_fieldOfStudy', 'linkedin_education1_grade', 'linkedin_education1_activities',\
            'linkedin_education1_description', 'linkedin_education2_school', 'linkedin_education2_dateStarted',\
            'linkedin_education2_dateEnd', 'linkedin_education2_degree', 'linkedin_education2_fieldOfStudy',\
            'linkedin_education2_grade', 'linkedin_education2_activities', 'linkedin_education2_description',\
            'linkedin_education3_school', 'linkedin_education3_dateStarted', 'linkedin_education3_dateEnd',\
            'linkedin_education3_degree', 'linkedin_education3_fieldOfStudy', 'linkedin_education3_grade',\
            'linkedin_education3_activities', 'linkedin_education3_description', 'linkedin_language1',\
            'linkedin_language2', 'linkedin_language3', 'linkedin_additionalInfo_interests',\
            'linkedin_additionalInfo_maritalStatus']
        header = self.header2+header1
        
        #self.listprofiles = ['http://www.linkedin.com/in/sanjay-gupta-7a7aa929','https://www.linkedin.com/in/aravindrajanm']
        #self.listprofiles = ['https://www.linkedin.com/in/phanipriya','https://www.linkedin.com/in/prrashi','https://www.linkedin.com/in/yatishteddla']
        #self.listprofiles = ['https://www.linkedin.com/in/saurabh-jain-597b8b41','https://www.linkedin.com/in/rajesh-thakur-0a5b876']
        #self.listprofiles = ['https://www.linkedin.com/in/aravindrajanm','http://www.linkedin.com/in/yogi-dave-a7687945','https://www.linkedin.com/in/lavanya-gr-51a497107']
        self.listprofiles = ['https://in.linkedin.com/in/sunderraj']
        '''self.listprofiles = [
                'http://www.linkedin.com/in/sanjay-gupta-7a7aa929',\
                'http://www.linkedin.com/in/jagdish-dalal-1a056710',\
                'http://www.linkedin.com/in/mahesh-bhagchandka-926838119',\
                'http://www.linkedin.com/in/mayur-navlani-439339a',\
                'https://www.linkedin.com/in/mala-jham-87467810',\
                'https://www.linkedin.com/in/jigish',\
                'http://www.linkedin.com/in/yogi-dave-a7687945',\
                'http://www.linkedin.com/in/umesh-kuttanda-58435420',\
                'http://www.linkedin.com/in/amit-mehra-0526393b',\
                'http://www.linkedin.com/in/mohammed-qureshi-87890b4',\
                'http://www.linkedin.com/in/shashir-narola-66aa3114',\
                'http://www.linkedin.com/in/kunal-jiwarajka-77a5767',\
                'http://www.linkedin.com/in/ashit-shah-41859052',\
                'http://www.linkedin.com/in/vivek-kakkad-8311a77',\
                'http://www.linkedin.com/in/renny-thomas-57785456',\
                'http://www.linkedin.com/in/uttam-kumar-chatterjee-9541a49',\
                'http://www.linkedin.com/in/manan-lahoty-2ab430',\
                'http://www.linkedin.com/in/sunilmistry',\
                'http://www.linkedin.com/in/giriraj-mohatta-94805440',\
                'http://www.linkedin.com/in/bimal-mody-234b5645',\
                'http://www.linkedin.com/in/anil-jain-5bb16124',\
                'http://www.linkedin.com/in/ghanshyam-biyani-37315820',\
                'http://www.linkedin.com/in/pratik-jain-2a72ba1b',\
                'http://www.linkedin.com/in/mayur-jain-056b1221',\
                'http://www.linkedin.com/in/shishir-jain-55507324',\
                'http://www.linkedin.com/in/ujval-lakhani-1aa90314',\
                'https://www.linkedin.com/in/suffian-md-isa-92388079',\
                'http://www.linkedin.com/in/pratik-kothari-85407551',\
                'http://www.linkedin.com/in/dinesh-dalamal-7a60a88',\
                'http://www.linkedin.com/in/sandeep-golechha-aa3b1712',\
                'http://www.linkedin.com/in/amit-chordia-b9282214',\
                'http://www.linkedin.com/in/mehul-mehta-b7532224',\

                'http://www.linkedin.com/in/gira-mehta-93954621',\
                'http://www.linkedin.com/in/kalpesh-shah-shah-39b22747',\
                'http://www.linkedin.com/in/debajeet-das-6a408314',\
                'http://www.linkedin.com/in/habib-datoobhoy-8ab32830',\
                'http://www.linkedin.com/in/ashutosh-mishra-32ba825',\
                'http://www.linkedin.com/in/arup-rakshit-985bb66',\
                'http://www.linkedin.com/in/ratna-krishnakumar-ba167b17',\
                'http://www.linkedin.com/in/rakesh-jariwala-6505a69',\
                'http://www.linkedin.com/in/amit-sridharan-aa24495',\
                'http://www.linkedin.com/in/amisha-vora-a1956a16',\
                'http://www.linkedin.com/in/saurabh-jain-597b8b41',\
                'http://www.linkedin.com/in/rajesh-thakur-0a5b876']'''
	

        self.row_count = 1
        self.excel_file_name = 'linkedin_profiles.xls'
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        for i, row in enumerate(header):
            self.todays_excel_sheet1.write(0, i, row)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        
    def spider_closed(self, spider):
        self.cur.execute(self.selectall)
        records = self.cur.fetchall()
        for record in records:
            sk2 , name2,  aux_info2, profile_url2 = record
            try:
                aux_infof = json.loads(aux_info2.replace('\r','').replace('\n','').strip())
                if name2:
                    values = []
                    for kil in self.header2:
                        values.append(self.restore(aux_infof.get(kil,'')))
                    values1 = [self.restore(aux_infof.get('phone','')), self.restore(aux_infof.get('email','')),self.restore(aux_infof.get('skill','')), self.restore(aux_infof.get('group','')),self.restore(aux_infof.get('recom','')), self.restore(aux_infof.get('news','')), self.restore(aux_infof.get('companies','')),self.restore(aux_infof.get('influencers','')),self.restore(aux_infof.get('schools',''))]
                    values.extend(values1)
                    for col_count, value in enumerate(values):
                        self.todays_excel_sheet1.write(self.row_count, col_count, value)
                    self.row_count = self.row_count+1
            except: import pdb;pdb.set_trace()
        self.todays_excel_file.save(self.excel_file_name)

    def parse(self, response):
        sel = Selector(response)
        logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
        csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
        source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())        
        """return [FormRequest.from_response(response, formname = 'login_form',\
                 formdata={'session_key':'rajaqx@gmail.com','session_password':'linkedinpw','isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]"""
        return [FormRequest.from_response(response, formname = 'login_form',\
            formdata={'session_key':'lckiranmayi9@gmail.com','session_password':'ramanaiah','isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]

    def parse_next(self, response):
        sel = Selector(response)
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Headbot; +http://headrun.com) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
	
        for li in self.listprofiles:
            sk = md5.md5(li).hexdigest()
            vals = (sk, li, sk, li)
            self.cur.execute(self.qry, vals)
        for li1 in self.listprofiles[:1]:
            sk1 = md5.md5(li1).hexdigest()
            yield Request('https://www.linkedin.com/vsearch/p?keywords=IBM%20USA', callback=self.parse_again, headers=headers,meta={"sk":sk1})

    def parse_again(self, response):
        sel = Selector(response)
	import pdb;pdb.set_trace()
        sk = response.meta['sk']
        member_id = ''
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Headbot; +http://headrun.com) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
        try: member_id = json.loads(sel.xpath('//button[@data-page-tracking-info][contains(@data-trk,"editing")]/@data-page-tracking-info').extract()[0]).get('vid','')
        except: member_id = ''
        name = ''.join(sel.xpath('//span[@class="full-name"]/text()').extract())
        skilldup = '<>'.join(sel.xpath('//div[@id="profile-skills"]/ul/li/@data-endorsed-item-name').extract())
        additional = ' ,'.join(sel.xpath('//p[@dir="ltr"][contains(.,"Email Id:")][contains(.,"Mobile")]/text()').extract()).replace('\n','')
        email_i = ''.join(re.findall('Email Id:(.*) ,',additional)).strip()
        phonu_i = ''.join(re.findall('Mobile:(.*)',additional)).strip()
        if not additional:
            additional = ' ,'.join(sel.xpath('//p[@dir="ltr"][not(contains(.,"Email Id:"))][contains(.,"Mobile")]/text()').extract()).replace('\n','')
            phonu_i = ''.join(re.findall('Mobile:(.*)',additional)).strip()
        if not additional:
            additional = ' ,'.join(sel.xpath('//p[@dir="ltr"][contains(.,"Email Id:")][not(contains(.,"Mobile"))]/text()').extract()).replace('\n','')
            email_i = ''.join(re.findall('Email Id:(.*) ',additional)).strip()
        if not email_i:
            email_i = ''.join(sel.xpath('//p[@class="description summary-field-show-more"][@dir="ltr"][contains(.,"@gmail.com")]/text()').extract())
        if not email_i:
            email_i = ''.join(sel.xpath('//p[@class="description summary-field-show-more"][@dir="ltr"][contains(.,".com")][contains(.,"@")]/text()').extract())
        email_i = email_i.replace('Please write to','').strip()
        
        if not member_id:
             print '*********************************************'
             print response.url
        auth = ''.join(sel.xpath('//script[@type="text/javascript"]/text()[contains(.,"ProfileEdit.setMapperBaseUrl")]').extract())
        idaut = ''
        if auth:
            idaut = ''.join(re.findall('authToken=(.*)&',auth))

        if member_id:
            aja_url = ''
            if idaut:
                aja_url = "%s%s%s"%(self.ajax_one_url, member_id, self.ajax_third_url%idaut)
            
            else:
                aja_url = "%s%s%s"%(self.ajax_one_url, member_id, self.ajax_second_url)
            if aja_url:
                yield Request(aja_url, callback=self.parse_go, meta={"sk":sk,"name":name,"ref":response.url,'skill_dup':skilldup,'em':email_i, 'ph':phonu_i})
        
        job_title_company = ''.join(sel.xpath('//div[@id="headline"]/p[@class="title"]/text()').extract())
        location = ''.join(sel.xpath('//span[@class="locality"]//text()').extract())
        industry = ''.join(sel.xpath('//dd[@class="industry"]//text()').extract())
        connections = ''.join(sel.xpath('//div[@class="member-connections"]//strong//text()').extract())
        summary = ''.join(sel.xpath('//div[@class="summary"]/p[@class="description"]//p//text()').extract())
       
        name1, mname, lan2, lname, jobtitle, company, location, industry, conn, summary = [''] * 10
        if name:
            name = name.split(' ')
            if len(name) == 2:
                name1, lname = name
            elif len(name) == 3:
                name1, mname, lname = name
            else:
                name1, lname = name[0], name[-1]
                name2 = name[1] + name[2]

        if job_title_company:
            job_title_company = job_title_company.split(' at ')
            jobtitle = job_title_company[0]
            company = job_title_company[-1]  
        experiences = sel.xpath('//div[@id="background-experience"]/h3/parent::div/div[contains(@id, experience)]')
        exp_list = []
        for exp in experiences:
            exp_title = ''.join(exp.xpath('.//h4//text()').extract())
            exp_company = ''.join(exp.xpath('.//h5//text()').extract())
            exp_daterange = exp.xpath('.//span[@class="experience-date-locale"]/time/text()').extract()
            
            if exp_daterange and len(exp_daterange) == 2:
                expstdate = exp_daterange[0]
                expenddate = exp_daterange[-1]
            elif len(exp_daterange) ==1 :
                expstdate = exp_daterange[0]
                try: expenddate =  ''.join(exp.xpath('.//span[@class="experience-date-locale"]/time/following-sibling::text()').extract()[0])
                except: expenddate =  ''
            elif len(exp_daterange) > 2:
                expstdate = exp_daterange[0]
                expenddate = exp_daterange[2]
            else:
                expstdate, expenddate = [''] * 2
            exp_location = ''.join(exp.xpath('.//span[@class="locality"]/text()').extract())
            expcountry, expcity = ['']*2 
            if exp_location:
                try: expcity, expcountry = exp_location.split(', ')
                except:
                    try: expcity, expcountry = exp_location.split('&')
                    except:
                        expcity = exp_location
            else:
                expcity, expcountry = [''] * 2
            expected_string = '<>'.join([exp_title, exp_company, expstdate,\
                     expenddate, expcity, expcountry])
            exp_list.append(expected_string)
        languages = sel.xpath('//div[@id="languages"]//li//text()').extract()
        
        edu_list = []
        educations = sel.xpath('//div[@id="background-education"]/h3/parent::div/div[contains(@id, education)]')
        for edu in educations:
            edu_school = ''.join(edu.xpath('.//h4//text()').extract())
            edu_degree = ','.join(edu.xpath('.//h5//text()').extract())
            edu_daterange = edu.xpath('.//span[@class="education-date"]/time/text()').extract()
            if edu_daterange and len(edu_daterange) == 2:
                edustdate = edu_daterange[0]
                eduenddate = edu_daterange[-1]
            elif len(edu_daterange) == 1:
                edustdate = edu_daterange[0]
                try: eduenddate = ''.join(edu.xpath('.//span[@class="education-date"]/time/following-sibling::text()').extract()[0])
                except: eduenddate = ''
            else:
                edustdate = ''
                eduenddate = ''
            activities = ''.join(edu.xpath('.//p[@class="activities"]//text()').extract()).replace(u'\u2013','').strip()
            edu_string = '<>'.join([edu_school, edu_degree, edustdate, eduenddate, activities])
            edu_list.append(edu_string)

        honors_list = []
        honors_awards = sel.xpath('//div[@id="background-honors"]/h3/parent::div/div[contains(@id, honors)]')
        for hon in honors_awards:
            hon_title = ''.join(hon.xpath('.//h4//text()').extract())
            hon_issuer = ','.join(hon.xpath('.//h5//text()').extract())
            hon_daterange = hon.xpath('.//span[@class="honors-date"]/time/text()').extract()
            hon_descr = ''.join(hon.xpath('.//p[@class="description summary-field-show-more"]/text()').extract())
            honsta = ''
            if hon_daterange and len(hon_daterange) == 2:
                honsta = hon_daterange[0]
                honend = hon_daterange[-1]
            elif len(hon_daterange) == 1:
                honsta = hon_daterange[0]
            hon_string = '<>'.join([hon_title, hon_issuer, honsta, hon_descr])
            honors_list.append(hon_string)
            
            
        lan2, lan3 = [''] * 2
        if len(languages) ==1:
            lan1 = ''.join(languages)
        elif len(languages) ==2:
            lan1, lan2 = languages
        elif len(languages) == 3:
            lan1, lan2, lan3 = languages
        else:
            lan1, lan2, lan3 = [''] * 3

        edu_school1, edustdate1, eduenddate1, edu_degree1,\
         fos1, grade1, activities1, edudesc1 = [''] * 8
        edu_school2, edustdate2, eduenddate2, edu_degree2,\
         fos2, grade2, activities2, edudesc2 = [''] * 8
        edu_school3, edustdate3, eduenddate3, edu_degree3,\
         fos3, grade3, activities3, edudesc3 = [''] * 8

        if len(edu_list) == 1:
            edu_school1, edu_degree1, edustdate1, eduenddate1, activities1 = \
                    ''.join(edu_list).split('<>')
        elif len(edu_list) == 2:
            edu_list1, edu_list2 = edu_list
            edu_school1, edu_degree1, edustdate1, eduenddate1, activities1 = \
                    edu_list1.split('<>')
            edu_school2, edu_degree2, edustdate2, eduenddate2, activities2 = \
                    edu_list2.split('<>')
        elif len(edu_list) == 3:
            edu_list1, edu_list2, edu_list3 = edu_list
            edu_school1, edu_degree1, edustdate1, eduenddate1, activities1 = \
                    edu_list1.split('<>')
            edu_school2, edu_degree2, edustdate2, eduenddate2, activities2 = \
                edu_list2.split('<>')
            edu_school3, edu_degree3, edustdate3, eduenddate3, activities3 = \
                edu_list3.split('<>')
        exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = [''] * 6
        exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2 = [''] * 6
        exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3 = [''] * 6

        if len(exp_list) == 1:
            exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = \
                ''.join(exp_list).split('<>')
        elif len(exp_list) == 2:
            exp_list1, exp_list2 = exp_list
            exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = \
                exp_list1.split('<>')
            exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2 = \
                exp_list2.split('<>')
        elif len(exp_list) == 3:
            exp_list1, exp_list2, exp_list3 = exp_list
            exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = \
                exp_list1.split('<>')
            exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2 = \
                exp_list2.split('<>')
            exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3 = \
                exp_list3.split('<>')

        hontitle1, honocc1, honissuer1, hondate1, hondesc1 = [''] * 5
        hontitle2, honocc2, honissuer2, hondate2, hondesc2 = [''] * 5
        hontitle3, honocc3, honissuer3, hondate3, hondesc3 = [''] * 5
        if len(honors_list) == 1:
            hontitle1,honissuer1, hondate1, hondesc1  = ''.join(honors_list).split('<>')
        elif len(honors_list) == 2:
            honl1, honl2 = honors_list
            hontitle1, honissuer1, hondate1, hondesc1 = honl1.split('<>')
            hontitle2, honissuer2, hondate2, hondesc2 = honl2.split('<>')
        elif len(honors_list) == 3:
            honl1, honl2, honl3 = honors_list
            hontitle1, honissuer1, hondate1, hondesc1 = honl1.split('<>')
            hontitle2, honissuer2, hondate2, hondesc2 = honl2.split('<>')
            hontitle3,  honissuer3, hondate3, hondesc3 = honl3.split('<>')
        
        add_int, maritalstatus, mobile, email = [''] * 4
        maritalstatus = ''.join(sel.xpath('//table[@summary="Personal Details"]//tr[th[contains(text(),"Marital Status")]]/td/text()').extract())
        add_int = ''.join(sel.xpath('//ul[@class="interests-listing"]/li//text()').extract())
        values = [response.url, name1, mname, lname, jobtitle, company, location, industry, connections, summary,\
                exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1,\
                exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2,\
                exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3,\
                hontitle1, honocc1, honissuer1, hondate1, hondesc1, hontitle2, honocc2, \
                honissuer2, hondate2, hondesc2, hontitle3, honocc3, honissuer3, hondate3,\
                hondesc3, edu_school1, edustdate1, eduenddate1, edu_degree1, fos1, grade1,\
                activities1, edudesc1, edu_school2, edustdate2, eduenddate2, edu_degree2,\
                fos2, grade2, activities2, edudesc2, edu_school3, edustdate3, eduenddate3,\
                edu_degree3, fos3, grade3, activities3, edudesc3, lan1, lan2, lan3,\
                add_int, maritalstatus]
        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        for kh, vh in zip(self.header2, values):
            up_aux.update({kh:self.replacefun(vh)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))
            
            
    def parse_go(self,response):
        sel = Selector(response)
        sk = response.meta['sk']
        name = response.meta['name']
        email1, phones1, skil_ulj1, grp1  = ['']*4
        temp = json.loads(response.body)
        all_keys = temp['content']
        #name = all_keys.get('ContactInfo','').get('relationship_info','').get('contactDetails','').get('name','')
        if name:
            name_vals = ('name', name, sk)
            self.cur.execute(self.updateqry% name_vals)
            contact_info = all_keys.get('ContactInfo','')
            skills_info = all_keys.get('Skills','')
            grops = all_keys.get('groupsMpr','')
            following = all_keys.get('Following','')
            list_given = []
            endorsement_given = all_keys.get('Endorsements','')
            if endorsement_given:
                endorse_gv = endorsement_given.get('recosMpr','')
                endorse_re = endorsement_given.get('refsMpr','')
                if endorse_gv:
                    recomme_giv = endorse_gv.get('recommendations','')
                    if recomme_giv:
                        for rg in recomme_giv:
                            li_ins = []
                            title_below = rg.get('title','')
                            text = rg.get('text','')
                            title_name = rg.get('fmt__recommendeeFullName','')
                            if title_name:
                                gn = "%s%s"%('Name',title_name)
				li_ins.append(gn)
                            if title_below:
                                gh = "%s%s"%('Title',title_below)
                                li_ins.append(gh)
                            if text:
                                gt  = "%s%s"%('Text',text)
                                li_ins.append(gt)
                            if li_ins:
                                list_given.append('%s%s'%('Given','_'.join(li_ins)))
                if endorse_re:
                    recomme_rece = endorse_re.get('results','')
                    if recomme_rece:
                        recomme_receo = recomme_rece[0]
                        if recomme_receo:
                            results_rece = recomme_receo.get('references','')
                            for rr in results_rece:
                                li_ins = []
                                if rg.get('referrer',''):
                                    title_below = rg.get('referrer','').get('headline','')
                                    text = rg.get('text','')
                                    title_name = rg.get('referrer','').get('fmt__referrerfullName','')
                                    if title_name:
                                        gn = "%s%s"%('Name',title_name)
                                    if title_below:
                                        gh = "%s%s"%('Title',title_below)
                                        li_ins.append(gh)
                                    if text:
                                        gt  = "%s%s"%('Text',text)
                                        li_ins.append(gt)
                                    if li_ins:
                                        list_given.append('%s%s'%('Received','_'.join(li_ins)))
            fol1, fol2, fol3, fol4 = [], [], [], [] 
            if following:
                chanel_foll = following.get('follow_channels','').get('channels','')
                company_foll = following.get('follow','').get('companyFollowees','')
                influencers = following.get('follow_people','').get('influencers','')
                foll_schools = following.get('follow_school','').get('schoolFollowees','')
                if chanel_foll:
                    for cf in chanel_foll:
                        titcf = cf.get('channel','').get('title','')
                        if titcf: fol1.append(titcf)
                
                if company_foll:
                    for yf in company_foll:
                        tityf = yf.get('canonicalName','')
                        if tityf: fol2.append(tityf)

                if influencers:
                    for inf in influencers:
                        titf = inf.get('_memberFullName','')
                        if titf: fol3.append(titf)

                if foll_schools:
                    for fsc in foll_schools:
                        tsf = fsc.get('canonicalName','')
                        if tsf: fol4.append(tsf)
            if grops:
                grp_list = grops.get('groups','')
                if grp_list:
                    grp1 = self.listtostring(grp_list)
            if skills_info:
                skil = skills_info.get('skillsMpr','')
                if skil:
                    skil_ul = []
                    skil_list = skil.get('skills','') 
                    if skil_list:
                        skil_ulj1 = self.listtostring(skil_list)
            if contact_info:
                contacts = contact_info.get('contact_info','')
                if contacts:
                    emails_list = contacts.get('emails','')
                    phones_list = contacts.get('phones','')
                    for i in emails_list:
                        email = i.get('email','')
                        if email: email1 = email
                    for e in phones_list:
                        phones = e.get('number','')
                        if phones: phones1 = phones
            self.cur.execute(self.selectaux%sk)
            aux_cu = self.cur.fetchall()
            up_aux = json.loads(aux_cu[0][0].replace('\n',''))
            if not email1:
                email1 = response.meta['em']
            if not phones1:
                phones1 = response.meta['ph']
            if email1:
                up_aux.update({'email':self.replacefun(email1)})
            if phones1:
                up_aux.update({'phone':self.replacefun(phones1)})
            if not skil_ulj1:
                skil_ulj1 = response.meta['skill_dup']
            if skil_ulj1:
                up_aux.update({'skill':self.replacefun(skil_ulj1)})
            if grp1:
                up_aux.update({'group':self.replacefun(grp1)})
            if list_given:
                up_aux.update({'recom':self.replacefun('<>'.join(list_given))})
            if fol1:
                up_aux.update({'news':self.replacefun('<>'.join(fol1))})
            if fol2:
                up_aux.update({'companies':self.replacefun('<>'.join(fol2))})
            if fol3:
                up_aux.update({'influencers':self.replacefun('<>'.join(fol3))})
            if fol4:
                up_aux.update({'schools':self.replacefun('<>'.join(fol4))})
            self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))

    def listtostring(self, skil_list):
        skil_ul, skil_ulj1i = [],''
        for s in skil_list:
            skiu = s.get('name','')
            if skiu:
                skil_ul.append(skiu)
        if skil_ul:
            skil_ulj1i = '<>'.join(skil_ul)
            return skil_ulj1i

            
    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###').replace(u'\u2013','').strip()
        return text

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

            
        
        

        
            

    
