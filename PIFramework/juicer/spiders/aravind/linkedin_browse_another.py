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
class linkedinB(BaseSpider):
    name = "linkedin"
    start_urls = ['https://www.linkedin.com/uas/login?goback=&trk=hb_signin']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999]
    
    def __init__(self, *args, **kwargs):
        super(linkedinB, self).__init__(*args, **kwargs)
        self.ajax_one_url = "https://www.linkedin.com/profile/mappers?x-a=%2Cprofile_v2_contact_info%2Cprofile_v2_groups%2Cprofile_v2_skills%2Cprofile_v2_connections%2Cprofile_v2_follow%2Cprofile_v2_course_recommendations%2Cprofile_v2_endorsements&x-p=profile_v2_connections%2Edistance%3A1%2Ctop_card%2EprofileContactsIntegrationStatus%3A0%2Cprofile_v2_right_fixed_discovery%2Erecords%3A12%2Cprofile_v2_right_fixed_discovery%2Eoffset%3A0%2Cprofile_v2_browse_map%2EpageKey%3Anprofile_view_nonself%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_discovery%2Erecords%3A12%2Cprofile_v2_discovery%2Erecords%3A12%2Ctop_card%2Etc%3Atrue%2Cprofile_v2_discovery%2Eoffset%3A0%2Cprofile_v2_summary_upsell%2EsummaryUpsell%3Atrue&x-oa=bottomAliases&id="
        self.ajax_second_url = "&locale=en_US&snapshotID=&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"
        self.ajax_third_url = "&locale=en_US&snapshotID=&authToken=%s&authType=name&invAcpt=&promoId=&notContactable=&primaryAction=&isPublic=false&sfd=true"

        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd='root')
        self.cur = self.con.cursor()
        self.selectall = 'select sk , name, aux_info, profile_url from linkedin_profiles'
        self.qry = 'insert into linkedin_profiles(sk, profile_url, aux_info, created_at, modified_at) values (%s, %s, "{}", now(), now())  on duplicate key update modified_at = now(), sk =%s, profile_url = %s, aux_info = "{}"'
        self.selectaux = 'select aux_info from linkedin_profiles where sk = "%s"'
        self.updateqry = "update linkedin_profiles set %s = '%s' where sk = '%s'"
        header = ['Name', 'Profile_url', 'Phone Number', 'Email','Skills', 'Groups', 'Recommendations' , 'Following News', 'Following Companies', 'Following Influencers', 'Following Schools']
        #self.listprofiles = ['http://www.linkedin.com/in/sanjay-gupta-7a7aa929','https://www.linkedin.com/in/aravindrajanm']
        #self.listprofiles = ['https://www.linkedin.com/in/phanipriya','https://www.linkedin.com/in/prrashi','https://www.linkedin.com/in/yatishteddla']
        #self.listprofiles = ['https://www.linkedin.com/in/saurabh-jain-597b8b41','https://www.linkedin.com/in/rajesh-thakur-0a5b876']
        #self.listprofiles = ['https://www.linkedin.com/in/rakesh-jariwala-6505a69']
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
                    values = [name2, profile_url2, self.restore(aux_infof.get('phone','')), self.restore(aux_infof.get('email','')),self.restore(aux_infof.get('skill','')), self.restore(aux_infof.get('group','')),self.restore(aux_infof.get('recom','')), self.restore(aux_infof.get('news','')), self.restore(aux_infof.get('companies','')),self.restore(aux_infof.get('influencers','')),self.restore(aux_infof.get('schools',''))]
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
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Veveobot; +http://corporate.veveo.net/contact/) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
        for li in self.listprofiles:
            sk = md5.md5(li).hexdigest()
            vals = (sk, li, sk, li)
            self.cur.execute(self.qry, vals)
        for li1 in self.listprofiles:
            sk1 = md5.md5(li1).hexdigest()
            yield Request(li1, callback=self.parse_again, headers=headers,meta={"sk":sk1})

    def parse_again(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        member_id = ''
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Veveobot; +http://corporate.veveo.net/contact/) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
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
        if job_title_company:
            job_title_company = job_title_company.split(' at ')
            jobtitle = job_title_company[0]
            company = job_title_company[-1]  

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
            up_aux = json.loads(aux_cu[0][0])
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
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

            
        
        

        
            

    
