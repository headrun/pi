from scrapy.http import Request, FormRequest
import xlwt
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from linkedin_params import *
from juicer.utils import *
import md5
class linkedinBmerge(JuicerSpider):
    name = "linkedin_browse"
    start_urls = ['https://www.linkedin.com/uas/login?goback=&trk=hb_signin']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999]

    def __init__(self, *args, **kwargs):
        super(linkedinBmerge, self).__init__(*args, **kwargs)
        self.ajax_one_url = ajax_one_url_params
        self.ajax_second_url = ajax_second_url_params
        self.ajax_third_url = ajax_third_url_params
        self.con = MySQLdb.connect(db   = 'FACEBOOK_PROFILES', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd='root')
        self.cur = self.con.cursor()
        self.selectall = selectall_params
        self.qry = qry_params
        self.selectaux = selectaux_params
        self.updateqry = updateqry_params
        header = header2_params+header1
        self.original_url_list = original_url_list_params
        self.listprofiles = ['https://www.linkedin.com/in/aravindrajanm']
        """for profiless_url in open('linke_screennames'):
                if profiless_url != '\n':
                    if '/pub' in profiless_url or "https://www.linkedin.com/in/aajay-girit-b858154b" in profiless_url:
                        profiless_url = self.original_url_list.get(profiless_url.strip('\n'),'')
                        if not profiless_url: profiless_url = profiless_url
                    self.listprofiles.append(profiless_url.strip('\n'))
                    if profiless_url == '': import pdb;pdb.set_trace()"""
        self.row_count = 1
        self.excel_file_name = 'linkedin_profiles.xls'
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        for i, row in enumerate(header):
            self.todays_excel_sheet1.write(0, i, row)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    """def spider_closed(self, spider):
        self.cur.execute(self.selectall)
        records = self.cur.fetchall()
        for record in records:
            sk2 , name2,  aux_info2, profile_url2 = record
            original_url = ''
            if profile_url2 in self.original_url_list.values():
                original_url = (list(self.original_url_list.keys())[list(self.original_url_list.values()).index(profile_url2)])
            else: original_url = profile_url2
            try:
                aux_infof = json.loads(aux_info2.replace('\r','').replace('\n','').replace('\t','').replace('\\','').strip())
                response_flag = ''
                if name2:
                    response_flag = 'Response Available'
                if not name2: response_flag = 'Response Not Available'
                values = []
                for kil in self.header2:
                    values.append(self.restore(aux_infof.get(kil,'')))
                values1 = [self.restore(aux_infof.get('phone','')), self.restore(aux_infof.get('email','')),self.restore(aux_infof.get('skill','')), self.restore(aux_infof.get('group','')),self.restore(aux_infof.get('recom','')), self.restore(aux_infof.get('news','')), self.restore(aux_infof.get('companies','')),self.restore(aux_infof.get('influencers','')),self.restore(aux_infof.get('schools','')),response_flag, original_url]
                values.extend(values1)
                for col_count, value in enumerate(values):
                    self.todays_excel_sheet1.write(self.row_count, col_count, value)
                self.row_count = self.row_count+1
            except: import pdb;pdb.set_trace()
        self.todays_excel_file.save(self.excel_file_name)"""

    def parse(self, response):
        sel = Selector(response)
        logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
        csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
        source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract()) 
	import pdb;pdb.set_trace()
        return [FormRequest.from_response(response, formname = 'login_form',\
            formdata={'session_key':'lckiranmayi9@gmail.com','session_password':'dotoday1#','isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]

    def parse_next(self, response):
        sel = Selector(response)
	import pdb;pdb.set_trace()
        """from scrapy.http.cookies import CookieJar
        cookieJar = response.meta.setdefault('cookie_jar', CookieJar())
        cookieJar.extract_cookies(response, response.request)
        cookies_test = cookieJar._cookies"""
        for li in self.listprofiles:
            sk = md5.md5(li).hexdigest()
            vals = (sk, li, sk, li)
            self.cur.execute(self.qry, vals)
        for li1 in self.listprofiles:
            sk1 = md5.md5(li1).hexdigest()
            try: yield Request(li1, callback=self.parse_again, headers=headers,meta={"sk":sk1})
            except: import pdb;pdb.set_trace()

    def parse_again(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        member_id = ''
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
        name1, mname, lan2, lname, jobtitle, company, location, industry, conn, summary = [''] * 10
        job_title_company = ''.join(sel.xpath('//div[@id="headline"]/p[@class="title"]/text()').extract())
        location = ''.join(sel.xpath('//span[@class="locality"]//text()').extract())
        industry = ''.join(sel.xpath('//dd[@class="industry"]//text()').extract())
        connections = ''.join(sel.xpath('//div[@class="member-connections"]//strong//text()').extract())
        summary = ''.join(sel.xpath('//div[@class="summary"]//p[@class="description"]//text()').extract())
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
            if not hon_descr and 'Honors & Awards' in hon_title:
                hon_descr = ''.join(hon.xpath('.//p//text()').extract())
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
        elif len(languages)>3:
            lan1, lan2, lan3 = languages[0:3]
        else:
            lan1, lan2, lan3 = [''] * 3

        edu_school1, edustdate1, eduenddate1, edu_degree1,\
         fos1, grade1, activities1, edudesc1 = [''] * 8
        edu_school2, edustdate2, eduenddate2, edu_degree2,\
         fos2, grade2, activities2, edudesc2 = [''] * 8
        edu_school3, edustdate3, eduenddate3, edu_degree3,\
         fos3, grade3, activities3, edudesc3 = [''] * 8
        edu_school4, edustdate4, eduenddate4, edu_degree4,\
         fos4, grade4, activities4, edudesc4 = [''] * 8

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
        elif len(edu_list) == 4:
            edu_list1, edu_list2, edu_list3, edu_list4 = edu_list
            edu_school1, edu_degree1, edustdate1, eduenddate1, activities1 = \
                edu_list1.split('<>')
            edu_school2, edu_degree2, edustdate2, eduenddate2, activities2 = \
                 edu_list2.split('<>')
            edu_school3, edu_degree3, edustdate3, eduenddate3, activities3 = \
                edu_list3.split('<>')
            edu_school4, edu_degree4, edustdate4, eduenddate4, activities4 = \
                edu_list4.split('<>')
        exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = [''] * 6
        exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2 = [''] * 6
        exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3 = [''] * 6
        exp_title4, exp_company4, expstdate4, expenddate4, exp_city4, exp_count4 = [''] * 6

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
        elif len(exp_list) > 3:
            exp_list1, exp_list2, exp_list3, exp_list4 = exp_list[0:4]
            exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1 = \
                exp_list1.split('<>')
            exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2 = \
                exp_list2.split('<>')
            exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3 = \
                exp_list3.split('<>')
            exp_title4, exp_company4, expstdate4, expenddate4, exp_city4, exp_count4 = \
                exp_list4.split('<>')

        hontitle1, honocc1, honissuer1, hondate1, hondesc1 = [''] * 5
        hontitle2, honocc2, honissuer2, hondate2, hondesc2 = [''] * 5
        hontitle3, honocc3, honissuer3, hondate3, hondesc3 = [''] * 5
        hontitle4, honocc4, honissuer4, hondate4, hondesc4 = [''] * 5
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
        elif len(honors_list) > 3:
            honl1, honl2, honl3, honl4 = honors_list[0:4]
            hontitle1, honissuer1, hondate1, hondesc1 = honl1.split('<>')
            hontitle2, honissuer2, hondate2, hondesc2 = honl2.split('<>')
            hontitle3,  honissuer3, hondate3, hondesc3 = honl3.split('<>')
            hontitle4,  honissuer4, hondate4, hondesc4 = honl4.split('<>')
        add_int, maritalstatus, mobile, email = [''] * 4
        maritalstatus = ''.join(sel.xpath('//table[@summary="Personal Details"]//tr[th[contains(text(),"Marital Status")]]/td/text()').extract())
        add_int = ''.join(sel.xpath('//ul[@class="interests-listing"]/li//text()').extract())
        values = [response.url, name1, mname, lname, jobtitle, company, location, industry, connections, summary,\
                exp_title1, exp_company1, expstdate1, expenddate1, exp_city1, exp_count1,\
                exp_title2, exp_company2, expstdate2, expenddate2, exp_city2, exp_count2,\
                exp_title3, exp_company3, expstdate3, expenddate3, exp_city3, exp_count3,\
                exp_title4, exp_company4, expstdate4, expenddate4, exp_city4, exp_count4,\
                hontitle1, honocc1, honissuer1, hondate1, hondesc1, hontitle2, honocc2, \
                honissuer2, hondate2, hondesc2, hontitle3, honocc3, honissuer3, hondate3,\
                hondesc4, hontitle4, honocc4, honissuer4, hondate4,\
                hondesc4, edu_school1, edustdate1, eduenddate1, edu_degree1, fos1, grade1,\
                activities1, edudesc1, edu_school2, edustdate2, eduenddate2, edu_degree2,\
                fos2, grade2, activities2, edudesc2, edu_school3, edustdate3, eduenddate3,\
                edu_degree3, fos3, grade3, activities3, edudesc3,\
                edu_school4, edustdate4, eduenddate4, edu_degree4, fos4, grade4,\
                activities4, edudesc4, lan1, lan2, lan3,\
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
            import pdb;pdb.set_trace()
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
                                if rr.get('referrer',''):
                                    title_below = rr.get('referrer','').get('headline','')
                                    text = rr.get('text','')
                                    title_name = rr.get('referrer','').get('fmt__referrerfullName','')
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
            try: up_aux = json.loads(aux_cu[0][0].replace('\n','').replace('\t','').replace('\r',''))
            except: import pdb;pdb.set_trace()
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

            
        
        

        
            

    
