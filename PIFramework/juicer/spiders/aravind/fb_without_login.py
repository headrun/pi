import re
import datetime
import requests
from bs4 import BeautifulSoup
import json
import MySQLdb
import xlwt

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import md5

class Fbnew(BaseSpider):
    name = "fb_without_login"
    handle_httpstatus_list = [404, 302, 303, 403, 500]

    def __init__(self, *args, **kwargs):
        super(Fbnew, self).__init__(*args, **kwargs)
	mail =  kwargs.get('mail', '')
	if mail:
		self.start_urls = ['https://www.facebook.com/search/top/?q=%s' % mail]
        '''self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd='root')
        self.cur = self.con.cursor()
	self.profiles_list = ['https://www.facebook.com/AravindRajanM']'''
        '''self.profiles_list = ['https://www.facebook.com/nikhil.chandwani','https://www.facebook.com/nsagar1990','https://www.facebook.com/karthikbalait/',
        'https://www.facebook.com/kuttanda.umesh', 'https://www.facebook.com/kkunal.bothra',\
        'https://www.facebook.com/lotus.mistry', 'http://www.facebook.com/amit.mehra.3998', \
        'http://www.facebook.com/ashraf.qureshi', 'http://www.facebook.com/kunaljiv', \
        'http://www.facebook.com/yogesh.agrawal.96592', 'http://www.facebook.com/ashit.shah.359', \
        'http://www.facebook.com/vivek.kakkad', 'http://www.facebook.com/people/_/100001022865533',\
        'http://www.facebook.com/renny.thomas.737', 'http://www.facebook.com/manan.lahoty', \
        'http://www.facebook.com/people/_/1639436935', 'http://www.facebook.com/eksureshkumar', \
        'http://www.facebook.com/people/_/100001040714960', 'http://www.facebook.com/bimal.mody', \
        'https://www.facebook.com/ramautar.jhawar', 'http://www.facebook.com/pratikj2', \
        'http://www.facebook.com/mayur.jain.581', 'http://www.facebook.com/sunil.jalan.775',\
        'http://www.facebook.com/people/_/100001582371079', 'http://www.facebook.com/pratik.kothari.3954',\
        'http://www.facebook.com/jainrakeshg', 'http://www.facebook.com/shanti856', \
        'http://www.facebook.com/people/_/100000690702184', 'http://www.facebook.com/amit.chordia.96', \
        'http://www.facebook.com/gira.mehta.3', 'http://www.facebook.com/people/_/100000479853734', \
        'http://www.facebook.com/debajeet.das','http://www.facebook.com/ashutosh.mishra.52056', \
        'http://www.facebook.com/arup.rakshit.7','http://www.facebook.com/ratna.krishnakumar', \
        'https://www.facebook.com/anthony.joseph.98837','http://www.facebook.com/people/_/711137216', \
        'http://www.facebook.com/people/_/100000642671604'] '''
        '''self.about = '/about'
        self.basic_info = '/about?section=contact-info' 
        self.relationshipurl = '/about?section=relationship'
        self.section_living = '/about?section=living'
        #self.list_tobeall = [('/movies','moives'), ('/tv','tvshow'), ('/books','books'), ('/likes','likes'), ('/music','music'), ('/friends','friends'), ('/games','games'), ('/likes_restaurants','restaurants'), ('/likes_section_sports_athletes','athelets'),('/about?section=education', 'education'),('/likes_section_sports_teams','sport teams')]
        self.list_tobeall = [('/likes_section_movies','moives'), ('/likes_section_tv_shows','tvshow'), ('/likes_section_books','books'), ('/likes','likes'), ('/likes_section_music','music'), ('/friends','friends'), ('/games','games'), ('/likes_restaurants','restaurants'), ('/likes_section_sports_athletes','athelets'),('/about?section=education', 'education'),('/likes_section_sports_teams','sport teams'),('/likes_people','People'),('/video_movies_watch','Watched Movies'),('/video_tv_shows_watch','Watched Tvshows'),('/books_read','Read Books'),('/map','checkins'),('/reviews','reviews'),('/groups','groups')]

        self.qry = 'insert into facebook_profiles(sk, profile_url, aux_info, created_at, modified_at) values (%s, %s, "{}", now(), now())  on duplicate key update modified_at = now(), sk =%s, profile_url = %s, aux_info = "{}"'
        self.updateqry = "update facebook_profiles set %s = '%s' where sk = '%s'"
        self.selectaux = 'select aux_info from facebook_profiles where sk = "%s"'
        self.selectall = 'select sk , name, profile_id, aux_info, profile_url from facebook_profiles'

        self.selectall = 'select sk , name, profile_id, aux_info, profile_url from facebook_profiles'
        header = ['Name', 'Profile_url', 'Tvshow', 'Movies', 'ID','Music','Birthday','Address Locality','Mobile_number', 'Gender','Interested In','Languages','Religious views','Political Views','Websites','Social Links','Facebook','Address','Other Phones','Relation','Family Members','Hometown','Work', 'Education','Friends','Books', 'Likes','Athelets', 'Sport teams','People', 'Watched Movies','Watched Tvshows','Read Books','Restaurants','Games','Email', 'Checkins', 'Reviews', 'Groups']
        self.row_count = 1 
        self.excel_file_name = 'facebook_profiles.xls'
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        for i, row in enumerate(header):
            self.todays_excel_sheet1.write(0, i, row)'''
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',')
        return text

    def spider_closed(self, spider):
        #elf.cur.execute(self.selectall)
        records = []#lf.cur.fetchall()
        for record in records:
            sk1 , name1, profile_id1, aux_info1, profile_url1 = record
            try:
                aux_infof = json.loads(aux_info1)
                if name1:
                    values = [name1, profile_url1, self.restore(aux_infof.get('tvshow','')), self.restore(aux_infof.get('movie','')),profile_id1, self.restore(aux_infof.get('music','')), self.restore(aux_infof.get('birthday','')), self.restore(aux_infof.get('address_locality','')), self.restore(aux_infof.get('mobile_number','')), self.restore(aux_infof.get('gender','')), self.restore(aux_infof.get('interested in','')), self.restore(aux_infof.get('languages','')),self.restore(aux_infof.get('religious views','')), self.restore(aux_infof.get('political views','')), self.restore(aux_infof.get('websites','')), self.restore(aux_infof.get('social_links1','')), self.restore(aux_infof.get('facebook','')), self.restore(aux_infof.get('address','')), self.restore(aux_infof.get('other phones','')),self.restore(aux_infof.get('relation','')),self.restore(aux_infof.get('family members','')), self.restore(aux_infof.get('hometown','')), self.restore(aux_infof.get('work','')), self.restore(aux_infof.get('education','')),self.restore(aux_infof.get('friends','')),self.restore(aux_infof.get('books','')),self.restore(aux_infof.get('likes','')),self.restore(aux_infof.get('athelets','')),self.restore(aux_infof.get('sport teams','')),self.restore(aux_infof.get('People','')),self.restore(aux_infof.get('Watched Movies','')),self.restore(aux_infof.get('Watched Tvshows','')),self.restore(aux_infof.get('Read Books','')),self.restore(aux_infof.get('restaurants','')),self.restore(aux_infof.get('games','')),self.restore(aux_infof.get('email','')), self.restore(aux_infof.get('checkins','')), self.restore(aux_infof.get('reviews','')), self.restore(aux_infof.get('groups',''))]
                    for col_count, value in enumerate(values):
                        print self.row_count, col_count, value
                        self.todays_excel_sheet1.write(self.row_count, col_count, value)
                    self.row_count = self.row_count+1
            except: import pdb;pdb.set_trace()
        #elf.todays_excel_file.save(self.excel_file_name)


    def parse(self, response):
        sel = Selector(response)
	texts = sel.xpath('//div[@class="hidden_elem"]').extract()[-1].replace('<!--', '').replace('-->', '')
	hxs = Selector(text=texts)
	users = ''.join(hxs.xpath('//div[@class="clearfix"]/a/@href').extract())
	import pdb;pdb.set_trace()
	with open('users.txt', 'a') as f:
		f.write('%s\n' % users)
	print users
        '''lsd = ''.join(sel.xpath('//input[@name="lsd"]/@value').extract())
        lgnrnd = ''.join(sel.xpath('//input[@name="lgnrnd"]/@value').extract())
        return [FormRequest.from_response(response, formname = 'login_form',\
                 formdata={'email':'sindhu4a1@gmail.com','pass':'9989365570','lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_next)]'''
  
    def parse_next(self, response):
        sel = Selector(response)
        for profile in self.profiles_list:
            sk = md5.md5(profile).hexdigest()
            vals = (sk, profile, sk, profile)
            self.cur.execute(self.qry, vals)
        for profile in self.profiles_list:
            sk = md5.md5(profile).hexdigest()
            yield Request(profile, callback=self.parse_profile, meta={'sk':sk})

    def parse_profile(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        fb_name = ''
        try: fb_name = json.loads(''.join(sel.xpath(\
        '//script[@type="application/ld+json"]/text()').extract())).get('name','')
        except: fb_name = ''.join(sel.xpath('//title[@id="pageTitle"]/text()').extract())
        #id_pf = ''.join(sel.xpath('//a[contains(@href,"profile_id")]/@href').extract())
        #fb_id = ''.join(re.findall('profile_id=(.*?)&',id_pf))
        id_pf = ''.join(sel.xpath('//meta[@property="al:android:url"]/@content').extract())
        fb_id = ''.join(re.findall('profile/(.*)',id_pf))
        if fb_name:
            name_vals = ('name', fb_name, sk)
            self.cur.execute(self.updateqry% name_vals)

        if fb_id:
            id_vals = ('profile_id', fb_id, sk)
            self.cur.execute(self.updateqry% id_vals)

        living_url = "%s%s"%(response.url,self.section_living)
        yield Request(living_url, callback=self.living_info,meta={'sk':sk})
        relatio_url = "%s%s"%(response.url,self.relationshipurl)
        yield Request(relatio_url, callback=self.relatio_info,meta={'sk':sk})
        about_basic_url = "%s%s"%(response.url,self.basic_info)
        yield Request(about_basic_url, callback = self.parse_basic_info,meta={'sk':sk})
        about_url = "%s%s"%(response.url,self.about)
        yield Request(about_url, callback = self.parse_about,meta={'sk':sk})
        list_tobe = self.list_tobeall
        for ki in self.list_tobeall:
            urlpar = "%s%s"%(response.url, ki[0])
            yield Request(urlpar, callback = self.parse_movies,meta={'type':ki[1],'sk':sk})

    def education1(self, soup,text):
        final_list, check = [],''
        if text == "work":
            check = soup.find('div',text="Work")
        else:
            check = soup.find('div',text="Education")
        if check:
            li_tags = check.findParent('div').find("ul").findAll('li')
            for lit in li_tags:
                lkit = lit.findAll('a')
                for lk in lkit:
                    if lk.attrs.get('href',''):
                        lkit = lk.text
                        if lkit and 'None' not in lkit:
                            variable = lkit
                            if variable:
                                final_list.append(variable)
        if final_list:
            return '<>'.join(final_list)
        else:
            final_list = ''
            return final_list
    def parse_movies(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        type_ = response.meta['type']
    
        final_list = []
        work1, educatio = '', ''
        comment_code = ''
        if type_ == "friends":
            comment_code = ''.join(sel.xpath('//div[@class="hidden_elem"]/code/comment()[contains(.,"friends")][contains(.,"data-pnref")]').extract())
            
        elif type_ == "education":
            comment_work =  ''.join(sel.xpath('//div[@class="hidden_elem"]/code/comment()[contains(.,"Work")][contains(.,"data-pnref")]').extract())
            if comment_work:
                comment_work = comment_work.replace(' -->','').replace('<!--','').strip()
                soup_work = BeautifulSoup(comment_work, 'lxml')
                if soup_work: 
                    work1 = self.education1(soup_work,'work')

            comment_education = ''.join(sel.xpath('//div[@class="hidden_elem"]/code/comment()[contains(.,"Education")][contains(.,"data-pnref")]').extract())
            if comment_education:
                comment_education = comment_education.replace(' -->','').replace('<!--','').strip()
                soup_education = self.get_beautifulsoup(comment_education)
                if soup_education: 
                    educatio = self.education1(soup_education,'educate')
            
        else:
            comment_code = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"uiList")]').extract()) 
        liksp_ = ''
        if type_ != 'education':
            comment_code = comment_code.replace(' -->','').replace('<!--','').strip()
            soup = BeautifulSoup(comment_code, 'lxml')
            check_code = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"aria-selected")]').extract())
            if 'likes' in response.url and type_ != 'likes':
                check_code = check_code.replace(' -->','').replace('<!--','').strip()
                liksp = BeautifulSoup(check_code, 'lxml')
                try:
                    liksp1_  = liksp.findAll('a',role=True)[0].get('aria-selected','')
                    if liksp1_:
                        liksp_ = liksp.findAll('a',role=True)[0].get('name','') 
                except: liksp_ = ''
                 
            if type_ == 'friends':
                li_tags = soup.find("ul")
                if li_tags:
                    li_tags = li_tags.findAll('li')
                    for lit in li_tags:
                        lkit = lit.findAll('a')
                        for lk in lkit:
                            if lk.attrs.get('data-gt',''):
                                lkit = lk.text
                                if lkit and 'None' not in lkit:
                                    variable = lkit
                                    if variable:
                                        final_list.append(variable)
            else:
                a_tags = soup.select("li > div > div > a")
                for ia in a_tags:
                    movis = ia.attrs.get('title')
                    if movis and 'None' not in movis:
                        variable = movis
                        if variable:
                            final_list.append(variable)
                if not final_list:
                    a_tags = soup.findAll('div',attrs={'class':"fsl fwb fcb"})
                    for ia in a_tags:
                        movis = ia.text
                        if movis and 'None' not in movis:
                            variable = movis
                            if variable: 
                                final_list.append(variable)
                if not final_list:
                    a_tags = soup.findAll('a',{'class':''}, href=re.compile(type_))
                    a_tag2 = ''
                    if not a_tags:
                        a_tag2 = soup.findAll('a', href=True)
                        a_tags = soup.findAll('a', href=True)
                    for ia in a_tags:
                        movis = ''
                        if a_tags == a_tag2:
                            if ia.get('data-hovercard',''):
                                movis = ia.text
                        else:
                            movis = ia.text
                        if movis and 'None' not in movis:
                            variable = movis
                            if variable: final_list.append(variable)
        if 'all likes' in liksp_.lower():
            final_list = ''
        print final_list
        print response.url
        print '**********'
        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        if final_list:
            final_lt = ','.join(set(final_list))
            if type_ and final_list:
                up_aux.update({type_: self.replacefun(final_lt)})
        if work1:
            up_aux.update({'work':self.replacefun(work1)})
        if educatio:
            up_aux.update({'education':self.replacefun(educatio)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))



    def parse_about (self,response):
        sel = Selector(response)
        sk = response.meta['sk']
        address_locality = ''
        try: address_locality = json.loads(''.join(sel.xpath('//script[@type="application/ld+json"]/text()').extract())).get('address','').get('addressLocality','') #lives in
        except:
            address_locality = ''
        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        if address_locality:
            up_aux.update({'address_locality': self.replacefun(address_locality)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk)) 

    def living_info(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        towns_meml1 = ''
        comment_living =  ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Hometown")]').extract())
        if comment_living:
            soup_living  = self.get_beautifulsoup(comment_living)
            if soup_living:
                towns_meml1 = self.findlr(soup_living,'')
        
        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        if towns_meml1:
            up_aux.update({'hometown':self.replacefun(towns_meml1)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))

    def relatio_info(self, response):
        sk = response.meta['sk']
        sel = Selector(response)
        relation1, family_meml1,  = '',''
        comment_relation = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Relationship")]').extract())
        
        if comment_relation:
            soup_relation = self.get_beautifulsoup(comment_relation)
            if soup_relation:
                try: relation1 = soup_relation.findAll('ul')[0].findNext('li').findNext('div').findNext('div').findNext('div').text
                except: relation1 = ''
        if 'No relationship info to show' in relation1:
            relation1  = ''
        comment_family = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Family Members")]').extract())
        if comment_family:
            soup_family  = self.get_beautifulsoup(comment_family)
            if soup_family:
                family_meml1 = self.findlr(soup_family,'family')
        if 'no relationship info to show' in family_meml1.lower():
            family_meml1 = ''

        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        if relation1:
            up_aux.update({'relation':self.replacefun(relation1)})
        if family_meml1:
            up_aux.update({'family members':self.replacefun(family_meml1)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))

    def findlr (self, soup_family,text1):
        family_meml, family_meml1 = [], ''
        soup_family = soup_family.find('ul')
        if soup_family:
            li_l  = soup_family.findAll('li')
            if li_l:
                for lt in li_l:
                    ones = ''
                    try: 
                        ones = lt.findAll('span')[0].text
                        if ones and text1:
                            relation = lt.findAll('span')[0].findNext('div').text
                            if relation:
                                ones = "%s%s%s"%(relation,':- ',ones)
                    except: ones = ''
                    if 'Add a family member' in ones: ones = ''
                    if 'No places to show' in ones: ones = ''
                    if ones: family_meml.append(ones)
        if family_meml:
            family_meml1 = '<>'.join(family_meml)
        return family_meml1
                            
                    
    def get_beautifulsoup (self, souptext):
        souptext = souptext.replace(' -->','').replace('<!--','').strip()
        soup = BeautifulSoup(souptext, 'lxml')
        return soup

    def get_listvalues(self, textlt, keyv):
        first_value = textlt
        values_list = []
        textlt = textlt.findParent('li')
        if textlt:
            if keyv == 'websites' or keyv == "social links" or keyv == "facebook":
                befre = textlt
                textlt = textlt.findAll('a')
                checksocial = textlt 
                if not textlt:
                    textlt = befre.findAll('span')
            else:
                textlt = textlt.findAll('span')
            if textlt:
                for tt in textlt:
                    if (keyv == 'websites' or keyv == "social links" or keyv == "facebook") and checksocial:
                        varb = tt.attrs.get('onmouseover','')
                        if 'this' in varb:
                            varb_ = re.findall('this, "(.*)"',varb)
                            if varb_:
                                varb = ''.join(varb_).replace('\\','')
                            else:
                                varb = ''
                        else:
                            varb = ''
                    else:
                        varb = tt.text
                    if varb in first_value: continue
                    varb = varb.replace(u' \xb7 ','').strip()
                    if varb:values_list.append(varb)
        if values_list:
            return '<>'.join(set(values_list))

    def parse_basic_info (self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        gender1, birthday1, interested_in1, languages1, religious_views1, political_views1, websites1, social_links1, fb_mobile_number1, facebook_f1, address_f1, other_phones_f1, fb_email1  = ['']*13
        basic_info = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Basic Information")]').extract())
        
        soup_basic = self.get_beautifulsoup(basic_info)
        gender = soup_basic.find('span',text=re.compile(u'Gender', re.IGNORECASE))
        if gender:
            gender1 = self.get_listvalues(gender,'gender')
        
        birthday = soup_basic.find('span',text=re.compile(u'Birthday', re.IGNORECASE))
        if birthday:
            birthday1 = self.get_listvalues(birthday,'birthday')

        interested_in = soup_basic.find('span',text=re.compile(u'Interested in', re.IGNORECASE))
        if interested_in:
            interested_in1 = self.get_listvalues(interested_in,'interested in') 
        languages = soup_basic.find('span',text=re.compile(u'Languages', re.IGNORECASE))
        if languages:
            languages1 = self.get_listvalues(languages,'languages')
        religious_views = soup_basic.find('span',text=re.compile(u'Religious views', re.IGNORECASE))
        if religious_views:
            religious_views1 = self.get_listvalues(religious_views,'religious views')
        political_views = soup_basic.find('span',text=re.compile(u'Political Views', re.IGNORECASE))
        if political_views:
            political_views1 = self.get_listvalues(political_views,'political views')
        
        Website_social_links = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Websites and social links")]').extract())
        if not Website_social_links:
            Website_social_links = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Websites and Social Links")]').extract())
        soup_web = self.get_beautifulsoup(Website_social_links)
        websites = soup_web.find('span',text='Websites')
        if websites:
            websites1 = self.get_listvalues(websites,'websites')
        social_links = soup_web.find('span',text='Social links')
        if not social_links: social_links = soup_web.find('span',text='Social Links')
        if social_links:
            social_links1 = self.get_listvalues(social_links,'social links')
        
        contact_informat = ''.join(sel.xpath('//div[@class="hidden_elem"]/code[@id]/comment()[contains(.,"Contact Information")]').extract())
        soup_conta = self.get_beautifulsoup(contact_informat)
        #fb_mobile_number = soup_conta.find('span',text='Mobile Phones')
        fb_mobile_number = soup_conta.find('span',text=re.compile(u'Mobile phones', re.IGNORECASE))
        if fb_mobile_number:
            fb_mobile_number1 = self.get_listvalues(fb_mobile_number,'mobile number')
        fb_email = soup_conta.find('span',text=re.compile(u'Email'))
        if fb_email:
            fb_email1 =  self.get_listvalues(fb_email,'email')
        
        facebook_f = soup_conta.find('span',text='Facebook')
        if facebook_f:
            facebook_f1 = self.get_listvalues(facebook_f, 'facebook')
        address_f = soup_conta.find('span',text='Address')
        if address_f:
            address_f1 = self.get_listvalues(address_f, 'address') 
        other_phones_f = soup_conta.find('span',text='Other Phones')
        if other_phones_f:
            other_phones_f1 = self.get_listvalues(other_phones_f,'Other Phones')
        
        
        self.cur.execute(self.selectaux%sk)
        aux_cu = self.cur.fetchall()
        up_aux = json.loads(aux_cu[0][0])
        if fb_mobile_number1:
            #up_aux.update({'mobile_number':fb_mobile_number.replace('"','').replace("'",'')})
            up_aux.update({'mobile_number':self.replacefun(fb_mobile_number1)})
        if gender1:
            up_aux.update({'gender':self.replacefun(gender1)})
        if birthday1:
            up_aux.update({'birthday':self.replacefun(birthday1)})
        if interested_in1:
            up_aux.update({'interested in':self.replacefun(interested_in1)})
        if languages1:
            up_aux.update({'languages':self.replacefun(languages1)})
        if religious_views1:
            up_aux.update({'religious views':self.replacefun(religious_views1)})
        if political_views1:
            up_aux.update({'political views':self.replacefun(political_views1)})
        if websites1:
            up_aux.update({'websites':self.replacefun(websites1)})
        if social_links1:
             up_aux.update({'social_links1':self.replacefun(social_links1)})
        if facebook_f1:
            up_aux.update({'facebook':self.replacefun(facebook_f1)})
        if address_f1:
            up_aux.update({'address':self.replacefun(address_f1)})
        if other_phones_f1:
            up_aux.update({'other phones':self.replacefun(other_phones_f1)})
        if fb_email1:
            up_aux.update({'email':self.replacefun(fb_email1)})
        self.cur.execute(self.updateqry%('aux_info', json.dumps(up_aux,ensure_ascii=False, encoding="utf-8"),sk))

    def replacefun(self, text):
        ###replace('"','').replace("'",'')
        #text = text.replace('<>#<>','"').replace("<>##<>","'").replace(',','###')
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text
        
        

        
        
    
