import re
import datetime
import requests
import json
import MySQLdb
import xlwt
import os
import md5
import string
import traceback
import logging
import logging.handlers
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from fb_browse_queries import *
from fb_constants import *

class FacebookBrowse(BaseSpider):
    name = "facebook_browse"
    start_urls = ['https://www.facebook.com/login']
    handle_httpstatus_list = [404, 302, 303, 403, 500]

    def __init__(self, *args, **kwargs):
        super(FacebookBrowse, self).__init__(*args, **kwargs)
	#self.login = kwargs.get('login', 'ch')
        #self.login = kwargs.get('login', 'anusha1903')
        self.login = kwargs.get('login','anucherry1903')
	self.domain = "https://mbasic.facebook.com"
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd='root')
        self.cur = self.con.cursor()
        self.about = '/about'
        self.likes = '?v=likes'
        #self.friends = '/friends'
        self.following = '?v=following'
	self.cur.execute(get_qry_params)
	self.profiles_list = [i for i in self.cur.fetchall()]
	self.res_afterlogin = ''
	self.cur_date = str(datetime.datetime.now().date())
        self.myname = os.path.basename(__file__).replace(".py", '')
        self.log_dir = os.path.join(os.getcwd(), 'logs')
        self.init_logger("%s_%s.log" %(self.myname,self.cur_date))
	dispatcher.connect(self.spider_closed, signals.spider_closed)
        
    def spider_closed(self, spider):
	if self.res_afterlogin:
		login_url = self.res_afterlogin.xpath('//a[contains(@href,"/logout.php")]/@href').extract()
		if login_url:
			login_urlf =  "%s%s"%(self.domain,login_url[0])
			cv = requests.get(login_urlf).text
			data = Selector(text=cv)
			login_xpat = data.xpath('//a[contains(@href,"/login.php")]/@href')
			if  login_xpat: self.log.info("Message - %s" %("Logout Successfully"))

    def init_logger(self, filename, level=''):
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        file_name = os.path.join(self.log_dir, filename)
        self.log = logging.getLogger(file_name)
        handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes=524288000, backupCount=5)
        formatter = logging.Formatter(
        '%(asctime)s.%(msecs)d: %(filename)s: %(lineno)d: \
        %(funcName)s: %(levelname)s: %(message)s', "%Y%m%dT%H%M%S")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.setLevel(logging.DEBUG)

    def parse(self, response):
        sel = Selector(response)
        #login = ''
        if self.profiles_list  :
		login  = constants_dict[self.login] 
		lsd = ''.join(sel.xpath('//input[@name="lsd"]/@value').extract())
		lgnrnd = ''.join(sel.xpath('//input[@name="lgnrnd"]/@value').extract())
	      
		return [FormRequest.from_response(response, formname = 'login_form',\
				formdata={'email': login[0],'pass':login[1],'lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_next)]
		#return [FormRequest.from_response(response, formname = 'login_form',\
				#formdata={'email':'anusha1903','pass':'1903@1733','lsd':lsd, 'lgnrnd':lgnrnd},callback=self.parse_next)]

    def parse_close(self, response):
	sel = Selector(response)
	self.res_afterlogin = sel

    def parse_next(self, response):
	yield Request('https://mbasic.facebook.com/', callback=self.parse_close)
        sel = Selector(response)
        for profilei in self.profiles_list:
            sk = profilei[0]
            meta_data = json.loads(profilei[2])
	    profile = meta_data.get('mbasic_url','')
	    email_address = meta_data.get('email_address','')
	    if not profile: continue
	    vals = (sk, profilei[1], sk, profilei[1])
	    self.cur.execute(qry_params, vals)
	    self.cur.execute(update_get_params%(9,sk))
            url_about = "%s%s"%(profile,self.about)
            url_following = "%s%s"%(profile,self.following)
            url1_about = "%s%s"%(profile,self.likes)
            #url_friends = "%s%s"%(profile, self.friends)
            #list_of_pa = [(url_about,'about'), (url_following,''), (url1_about,''), (url_friends,''), (profile,'about')]
            list_of_pa = [(url_about,'about'), (url_following,''), (url1_about,''), (profile,'about')]
            for urls in list_of_pa:
                yield Request(urls[0], callback=self.parse_profile, meta={'sk':sk,"al":'',"see_more":'','profile':profile,"check_list":'','not_found':urls[1], 'email_address':email_address},dont_filter=True)

    def parse_profile(self, response):
        sel = Selector(response)
        #self.res_afterlogin = sel
        sk = response.meta['sk']
	if response.status != 200: self.cur.execute(update_get_params%(2,sk))
        not_found = ''.join(sel.xpath('//title/text()').extract())
        if not response.meta['see_more'] and 'about' in response.meta['not_found']:
            if not  'page not found' in not_found.lower():
                owner_id = ''
                name = ''.join(sel.xpath('//strong[@class="profileName"]//text()').extract())
                if not name: name = ''.join(sel.xpath('//strong[@class="bp"]//text()').extract())
                if not name: name = ''.join(sel.xpath('//title/text()').extract())
		if 'facebook' in name.lower(): name = ''
                owner_href = sel.xpath('//a[@class="btn btnD"][contains(@href,"mbasic")]/@href').extract()
                if not owner_href: owner_href = sel.xpath('//a[contains(@href,"fbid")]/@href').extract()
                if not owner_href: owner_href = sel.xpath('//a[contains(@href,"profile_id")]/@href').extract()
                if not owner_href: owner_href = sel.xpath('//a[contains(@href,"id")][contains(@href,"mbasic")]/@href').extract()
                if owner_href:
                    owner_href = owner_href[0]
                    owner_id = ''.join(re.findall('profile_id=(\d+)',owner_href))
                    if not owner_id:
                        if 'fbid' in owner_href: owner_id = ''.join(re.findall(';id=(\d+)',owner_href))
                        if 'fbid' in owner_href: owner_id = ''.join(re.findall('&id=(\d+)',owner_href))
                    if not owner_id: owner_id = ''.join(re.findall('id=(\d+)',owner_href))
                    if not owner_id: owner_id = ''.join(re.findall('id=(.*)',owner_href))
                current_city =  ''.join(sel.xpath('//div[@title="Current City"]//td[@class]//text()').extract())
                howe_town = ''.join(sel.xpath('//div[@title="Home Town"]//td[@class]//text()').extract())
                if not howe_town:
                    howe_town = ''.join(sel.xpath('//div[@title="Hometown"]//td[@class]//text()').extract())
                facebook_cont = ''.join(sel.xpath('//div[@title="Facebook"]//td[@class]//text()').extract())
                birthday = ''.join(sel.xpath('//div[@title="Birthday"]//td[@class]//text()').extract())
                gender = ''.join(sel.xpath('//div[@title="Gender"]//td[@class]//text()').extract()) 
                professional_skills = ''.join(sel.xpath('//div[@id="skills"]//div[contains(@class,"skills")]/span//text()').extract())
                if not professional_skills: professional_skills = ''.join(sel.xpath('//div[@id="skills"]//div/span//text()').extract())
                mobile = ''.join(sel.xpath('//div[@title="Mobile"]//td[@class]//text()').extract())
                instagram = ''.join(sel.xpath('//div[@title="Instagram"]//td[@class]//text()').extract())
                websites = ''.join(sel.xpath('//div[@title="Websites"]//td[@class]//text()').extract())
                interested_in = ''.join(sel.xpath('//div[contains(@title,"Interested")]//td[@class]//text()').extract())
                languages = ''.join(sel.xpath('//div[contains(@title,"Languages")]//td[@class]//text()').extract())
                religious_views = ''.join(sel.xpath('//div[contains(@title,"Religious")]//td[@class]//text()').extract())
                political_views = ''.join(sel.xpath('//div[contains(@title,"Political")]//td[@class]//text()').extract())
                relationship = ''.join(sel.xpath('//div[@id="relationship"]/div/div[not(table)]//text()').extract())
                address = ''.join(sel.xpath('//div[contains(@title,"Address")]//td[@class]//text()').extract())
                google_talk = ''.join(sel.xpath('//div[contains(@title,"Google Talk")]//td[@class]//text()').extract())
                email = ''.join(sel.xpath('//div[contains(@title,"Email")]//td[@class]//text()').extract())
                nick_name = ''.join(sel.xpath('//div[contains(@title,"Nickname")]//td[@class]//text()').extract())
                other_names = ''.join(sel.xpath('//div[contains(@title,"Other")]//td[@class]//text()').extract())
                messenger = ''.join(sel.xpath('//div[contains(@title,"Messenger")]//td[@class]//text()').extract())
                home_phone = ''.join(sel.xpath('//div[@title="Home"]//td[@class]//text()').extract())
                no_of_friends = ''.join(sel.xpath('//a[contains(text(),"See all friends")]//text()').extract())
                if no_of_friends : no_of_friends = "".join(re.findall('(\d+)',no_of_friends))
                if name:
		    #self.res_afterlogin = sel
                    name_vals = ('name', self.replacefun(name), sk)
                    self.cur.execute(updateqry_params% name_vals)
                    if owner_id:
                        id_vals = ('profile_id', owner_id, sk)
                        self.cur.execute(updateqry_params% id_vals)
			self.cur.execute(update_get_params%(1,sk))	
                    self.cur.execute(selectaux_params%sk)
                    aux_cu1 = self.cur.fetchall()
                    up_aux3 = json.loads(aux_cu1[0][0])
		    up_aux3.update({"email_address":self.replacefun(response.meta.get('email_address',''))})
                    if current_city:
                        up_aux3.update({"current_city":self.replacefun(current_city)})
                    if howe_town:
                        up_aux3.update({"home_town":self.replacefun(howe_town)})

               

                    if no_of_friends :
                        up_aux3.update({"no_of_friends":self.replacefun(no_of_friends)})
                    if facebook_cont:
                        up_aux3.update({"facebook":self.replacefun(facebook_cont)})
                    if birthday:
                        up_aux3.update({"birthday":self.replacefun(birthday)})
                    if gender: up_aux3.update({"gender":self.replacefun(gender)})
                    if professional_skills: up_aux3.update({"professional_skills":self.replacefun(professional_skills)})
                    if no_of_friends : up_aux3.update({"no_of_friends":self.replacefun(no_of_friends)})
                    if mobile: up_aux3.update({"mobile":self.replacefun(mobile)})
                    if instagram: up_aux3.update({"instagram":self.replacefun(instagram)})
                    if websites: up_aux3.update({"websites":self.replacefun(websites)})
                    if interested_in: up_aux3.update({"interested_in":self.replacefun(interested_in)})
                    if languages: up_aux3.update({"languages":self.replacefun(languages)})
                    if religious_views: up_aux3.update({"religious_views":self.replacefun(religious_views)})
                    if political_views: up_aux3.update({"political_views":self.replacefun(political_views)})
                    if relationship: up_aux3.update({"relationship":self.replacefun(relationship)})
                    if address: up_aux3.update({"address":self.replacefun(address)})
                    if google_talk: up_aux3.update({"google_talk":self.replacefun(google_talk)})
                    if email: up_aux3.update({"email":self.replacefun(email)})
                    if nick_name: up_aux3.update({"nick_name":self.replacefun(nick_name)})
                    if messenger: up_aux3.update({"messenger":self.replacefun(messenger)})
                    if home_phone: up_aux3.update({"home_phone":self.replacefun(home_phone)})
                    if other_names: up_aux3.update({"other_names":self.replacefun(other_names)})
                    self.cur.execute(updateqry_params%('aux_info', json.dumps(up_aux3,ensure_ascii=False, encoding="utf-8"),sk))
		else: self.cur.execute(update_get_params%(2,sk))
        profile = response.meta['profile']
        others_list,clothing_list,activities_list, interests_list, music_list, books_list, movies_list, tvshow_list, favteams_list, favathe_list, friends_list, games_list, restaurants_list, websites_list, work_list, education_list, family_list,sports_list, inspirationalpeople_list, following_list = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        ab_list = []
        seetv_likes_list, seetv_watched_list, seemv_likes_list, seemv_watched_list, seebk_likes_list,television_list, reads_list = [],[],[],[],[],[],[]
        dic_keys = {"Other":others_list,"Clothing":clothing_list,"Activities":activities_list,'Interests':interests_list,"Music":music_list, "Books":books_list,"Movies":movies_list,"TV Shows":tvshow_list, "Favorite Teams":favteams_list, "Favorite Athletes":favathe_list,"Games":games_list, "Restaurants":restaurants_list, "Websites":websites_list, "work":work_list, "education":education_list, "family":family_list,"Favorite Sports":sports_list, "Friends":friends_list,"Films":movies_list,"TV Programmes":tvshow_list,"Inspirational People":inspirationalpeople_list,'Television':television_list,"Favourite teams":favteams_list,"Favourite athletes":favathe_list,"following":following_list,"Inspirational people":inspirationalpeople_list}
        dic_keys_movie ={'Likes':seemv_likes_list,'Watched': seemv_watched_list,"Movies":seemv_likes_list,"Films":seemv_likes_list}
        dic_keys_tvshow = {'Likes':seetv_likes_list,'Watched': seetv_watched_list,'Television':television_list,'TV Shows':seetv_likes_list,"TV Programmes":seetv_likes_list}
        dic_keys_books = {'Likes':seebk_likes_list, 'Read': reads_list,'Books':seebk_likes_list}
        check, check_list = '',''
        if not response.meta['see_more']:
            if 'likes' in response.url:
                ab_list = ["Other","Clothing","Activities",'Interests',"Music","Books","Movies","TV Shows","Favorite Teams","Favorite Athletes","Games","Restaurants","Websites","Favorite Sports","Films","TV Programmes","Inspirational People","Favourite teams","Favourite athletes", 'Inspirational people']
            elif 'friends' in response.url:
                ab_list = ["Friends"]
            elif 'followers' in response.url or 'following' in response.url:
                ab_list = ["following"]
            else:
                ab_list = ["work", 'education','family']
        else:
            ab_list = [response.meta['al']]
            check_list = response.meta['al']
            if "Watched" in check_list or "Likes" in check_list or "Book" in check_list or 'Read' in check_list:
                check_list = ''.join(sel.xpath('//h2/text()').extract())
                check = 'yes'
                if 'movie' in response.url:
                    check = 'movie'
                elif 'tvshow' in response.url:
                    check = 'tvshow'
                else:
                    if 'books' in response.url:
                        check = 'read'
                ab_list = [''.join(sel.xpath('//h4/text()').extract()).strip()]
                if not ab_list or ab_list == ['']:
                    ab_list = [response.meta['al']]
                if 'movie' in ab_list[0].lower() or 'film' in ab_list[0].lower():
                    check = 'movie'
                elif 'tv' in ab_list[0].lower():
                    check = 'tvshow'
                else:
                    if 'read' in ab_list[0].lower() or 'book' in ab_list[0].lower():
                        check = 'read'
            if sel.xpath('//h4[contains(text(),"Likes")]/text()').extract():
                text_to = ''.join(sel.xpath('//h2/text()').extract())
                if sel.xpath('//div[contains(text(),"Watched")]/text()').extract():
                    if 'Movies' in check_list or 'Films' in check_list:
                        check = 'movie'
                    if 'tv' in check_list.lower():
                        check = 'tvshow'
                    ab_list = ["Watched","Likes"]
                elif 'movie' in text_to.lower() or 'film' in text_to.lower():
                    check = 'movie'
                    ab_list = ["Watched","Likes"]
                elif 'tv' in text_to.lower():
                    check = 'tvshow'
                    ab_list = ["Watched","Likes"]
                else:
                    if sel.xpath('//div[contains(text(),"Read")]/text()').extract():
                        check = 'read'
                    ab_list = ["Read","Likes"]
        for al in ab_list:
            if al:
                nodes, nodes_xpath = [],''
                if 'Friends' in al:
                    nodes = sel.xpath('//div[@class="timeline"][h3[@class][contains(text(),"%s")]]/div[div[not(contains(@class,"basicNavItems"))]]/div'%al)
                    if not nodes: nodes = sel.xpath('//div[h3[@class][contains(text(),"%s")]]/div[div[not(contains(@class,"basicNavItems"))]]/div'%al)
                elif 'following' in response.url or 'following' in al:
                    nodes = sel.xpath('//div[@id="root"]/div[not(@class)]/div')
                    if not nodes: nodes = sel.xpath('//div[@id="root"]/div/div/div/div[@class]')
                else:
                    nodes = sel.xpath('//div[@id="%s"]/div/div[not(table)]/div'%al)
                    if not nodes:
                        nodes = sel.xpath('//div[h4[contains(text(),"%s")]]/div'%al)
                    if not nodes:
                        nodes = sel.xpath('//div[h3[contains(text(),"%s")]]/following-sibling::div[1]/div/div'%al)
                    if not nodes:
                        nodes_xpath = '//div[div[contains(text(),"%s")]]/table'
                        nodes = sel.xpath('//div[div[contains(text(),"%s")]]/table'%al)
                for node in nodes:
                    inner_node, childs = [], []
                    if 'Friends' in al:
                        inner_node = node.xpath('.//table//td[not(img)]')
                        childs = inner_node.xpath('./child::*')
                    elif  nodes_xpath == '//div[div[contains(text(),"%s")]]/table':
                        inner_node = node.xpath('.//td[not(img)]')
                        childs = inner_node.xpath('./child::*')
                    else:
			allphabets_string =  list(string.ascii_lowercase)
			inner_node = node.xpath('.//div[@class="clear"]/parent::div')
			if not inner_node:
				for alp in allphabets_string:
					inner_node = node.xpath('.//div[@class="b%s"]/parent::div'%alp)
					if inner_node: break
			
			
                        """inner_node = node.xpath('.//div[@class="clear"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="bt"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="bv"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="br"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="bu"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="bw"]/parent::div')
                        if not inner_node: inner_node = node.xpath('.//div[@class="bs"]/parent::div')
			if not inner_node: inner_node = node.xpath('.//div[@class="bj"]/parent::div')
			if not inner_node: inner_node = node.xpath('.//div[@class="bi"]/parent::div')
			if not inner_node: inner_node = node.xpath('.//div[@class="bq"]/parent::div')
			if not inner_node: inner_node = node.xpath('.//div[@class="br"]/parent::div')"""
                        childs = inner_node.xpath('./div/child::*[local-name()!="br"]')
                    above, below = ['']*2
                    if len(childs)>1:
                        above =  childs[0].xpath('.//text()').extract()
                        below =  childs[1].xpath('.//text()').extract()
			if not above and len(below) ==2:
				above = [below[0]]
				below = [below[1]]
                    if len(childs) == 1:
                        above =  childs[0].xpath('.//text()').extract()
                    above = ''.join(above)
                    if 'follow' in al and 'follow' in above: above = ''
                    below = ''.join(below).strip()
                    if below == 'Like' or 'mutual friend' in below.lower() or 'friends' in al.lower():
                        below = ''
                    if 'add friend' in above.lower() or 'message' in above.lower():
                        above = ''
                    if above:
                        tolist = ''
                        if below: tolist = "%s%s%s"%(above,':-',below)
                        else:tolist = above
                        try: 
                            if not check:
                                dic_keys[al].append(tolist)
                            else:
                                if 'Movies' in check_list or 'Films' in check_list or 'movie' in check:
                                    dic_keys_movie[al].append(tolist)
                                elif 'tv' in check_list.lower() or 'tvshow' in check:
                                    dic_keys_tvshow[al].append(tolist)
                                else:
                                    if 'Book' in check_list or 'read' in check:
                                        dic_keys_books[al].append(tolist)
                        except: pass 
                    if 'Friends' not in al:
                        see_more = ''
                        if nodes_xpath == '//div[div[contains(text(),"%s")]]/table':
                            see_more = ''.join(sel.xpath('//div[div[contains(text(),"%s")]]/a[contains(text(),"more")]/@href'%al).extract())
                        elif 'following' in al:
                            see_more =  sel.xpath('//a[span[contains(text(),"See More")]]/@href').extract()
                            if not see_more:
                                see_more = sel.xpath('//a[span[contains(text(),"See more")]]/@href').extract()
                        else:
                            see_more = ''.join(node.xpath('./self::div[contains(@class,"seeMore")]/a/@href').extract())
                            if not see_more: see_more = node.xpath('./self::div/a[span[contains(text(),"See More")]]/@href').extract()
                            if not see_more:
				see_more = ''.join(node.xpath('//a[span[contains(text(),"See more")]]/@href').extract())
				if not see_more: ''.join(node.xpath('//a[span[contains(text(),"see more")]]/@href').extract()) 
			    if not see_more:
                                try: see_more = ''.join(sel.xpath('//div[h3[contains(text(),"%s")]]/following-sibling::div[2]/a[contains(text(),"more")]/@href'%al).extract()[0])
				except: see_more = ''
                                if not see_more:
                                    try: see_more = ''.join(sel.xpath('//div[h3[contains(text(),"%s")]]/following-sibling::div[2]/a[contains(text(),"See more")]/@href'%al).extract()[0])
				    except: see_more = ''
                        if see_more:
                            if 'following' in al:
                                for i_ in see_more:
                                    url_again = "%s%s"%("https://mbasic.facebook.com",i_)
                                    yield Request(url_again, callback= self.parse_profile,meta={'sk':sk,"al":al,"see_more":'yes','profile':profile,"check_list":check_list,'not_found':''})
                            else:
                                if 'mbasic' not in see_more:
                                    url_again = "%s%s"%("https://mbasic.facebook.com",see_more)
                                    yield Request(url_again, callback= self.parse_profile,meta={'sk':sk,"al":al,"see_more":'yes','profile':profile,"check_list":check_list,'not_found':''})
                        if not see_more:
                            try: see_more = ''.join(sel.xpath('//a[span[contains(text(),"See more")]]/@href').extract()[0])
			    except: see_more = ''
                            url_again = "%s%s"%("https://mbasic.facebook.com",see_more)
                            if see_more: yield Request(url_again, callback= self.parse_profile,meta={'sk':sk,"al":al,"see_more":'yes','profile':profile,"check_list":check_list,'not_found':''})
                if 'Friends' in al:
                    see_more = ''.join(sel.xpath('//div[@class="timeline"]/div[contains(@class,"seeMoreFriends")]/a/@href').extract())
                    if not see_more: see_more  = ''.join(sel.xpath('//a[span[contains(text(),"See More Friends")]]/@href').extract())
                    if not see_more: see_more = ''.join(sel.xpath('//a[span[contains(text(),"See more friends")]]/@href').extract())
                    if not see_more: see_more = ''.join(sel.xpath('//a[span[contains(text(),"ee ")]]/@href').extract())
                    if see_more:
                        if 'mbasic' not in see_more:
                            url_again = "%s%s"%("https://mbasic.facebook.com",see_more)
                            yield Request(url_again, callback= self.parse_profile,meta={'sk':sk,"al":al,"see_more":'yes','profile':profile,"check_list":check_list,'not_found':''})
        

        all_lists = [(others_list,'fb_others','others'),(clothing_list,'fb_clothing','clothing'), (activities_list,'fb_activities','activities'), (interests_list,'fb_interests', 'interests'), (music_list,'fb_music','music'), (books_list,'fb_books','book'), (movies_list,'fb_movies','movies'), (tvshow_list, 'fb_tvshows','tvshows'), (favteams_list,'fb_favaourite_athelets','atheletes'), (favathe_list,'fb_favourite_teams','teams'), (games_list,'fb_games','games'), (restaurants_list,'fb_restaurants','restaurants'), (websites_list,'fb_websites','websites'), (work_list,'fb_works','work'), (education_list,'fb_education','education'), (family_list,'fb_family','family'),(sports_list, 'fb_favourite_sports','sports'),(friends_list,'fb_friends','friends'),(inspirationalpeople_list,'fb_inspirational_people','inspirational_people'),(seetv_likes_list,'fb_tvshow_likes','tvshow_likes'), (seetv_watched_list,'fb_tvshows_watched','tvshow_watched'), (seemv_likes_list,'fb_movies_likes','movie_likes'), (seemv_watched_list,'fb_movies_watched','movie_watched'),(seebk_likes_list,'fb_book_likes','books_likes'), (reads_list,'fb_read_books','read_books'),(following_list,'fb_following','read_followers')]
        for alk in all_lists:
            if alk[0]:
                keyf = "%s%s"%('aux_info_',alk[2])
                self.cur.execute(selectauxkeys_params%(keyf,sk))
                aux_cu = self.cur.fetchall()
                try: 
                    up_aux1 = json.loads(aux_cu[0][0].replace('\\',''))
                
                    if up_aux1.get(alk[1],''):
                        fromothe = up_aux1.get(alk[1],'').split('<>')
                        fromothe.extend(set(alk[0]))
                        up_aux1.update({alk[1]:self.replacefun('<>'.join(list(set(fromothe))))})
                    else:
                        up_aux1.update({alk[1]:self.replacefun('<>'.join(set(alk[0])))}) 
                    self.cur.execute(updateqry_params%(keyf, json.dumps(up_aux1,ensure_ascii=False, encoding="utf-8"),sk))
                except Exception,e:
			self.log.error("Error: %s", traceback.format_exc())
			self.log.info("Message - %s" %(response.url))

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text
        
        

        
        
    
