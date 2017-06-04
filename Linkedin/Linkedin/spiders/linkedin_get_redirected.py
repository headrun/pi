##from linkedin_queries import *
from linkedin_functions import *
from random_mails import mails_dict
class Linkedinpremiumprofilesbrowsered(scrapy.Spider):
    name = "linkedinredirected_browse"
    allowed_domains = ["linkedin.com"]
    start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)
    #custom_settings = { 'REDIRECT_MAX_TIMES': 333 }

    def __init__(self, *args, **kwargs):
	super(Linkedinpremiumprofilesbrowsered, self).__init__(*args, **kwargs)
        self.login = kwargs.get('login', 'ramanujan')
	self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
	#get_query_param = "select sk, url, meta_data from linkedin_crawl where crawl_status=0 limit 15"
	get_query_param = 'select sk, original_url from linkedin_connectionprofiles where profile_url like "%name&authToken%" order by rand() limit 500'
        self.query2 = 'update linkedin_connectionprofiles set profile_url= "%s" where sk = "%s"'

	self.cur.execute(get_query_param)
	self.profiles_list = [i for i in self.cur.fetchall()]
	dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
	sel = Selector(response)
	logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
	csrf_token = ''.join(sel.xpath('//input[@name="csrfToken"]/@value').extract())
	source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
	account_mail, account_password = random.choice(list(mails_dict.items()))[1]
	print account_mail, account_password
	if account_mail:	
	        print {'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias}
	        return [FormRequest.from_response(response, formname = 'login_form',\
                    formdata={'session_key':account_mail,'session_password':account_password,'isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next)]
		    

    def spider_closed(self, spider):
	cv = requests.get('https://www.linkedin.com/logout/').text

	
    def parse_next(self, response):
	sel = Selector(response)
	for li in self.profiles_list:
	    sk = li[0]
	    yield Request(li[1], callback=self.parse_correct, meta={"sk":sk})


    def parse_correct(self, response):
        sel = Selector(response)
	sk = response.meta.get('sk','')
	meb = sel.xpath('//code[contains(text(),"PatentView")][contains(text(),"objectUrn")][contains(text(),"urn:li:member:")]').extract() 
	linkedin_auth, memb_id = '',''
	linke_a, linkd_javatex = {},''
	try: linke_a = json.loads(sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').strip()).get('included','')
	except:
		try:
			cv = (sel.xpath('//code[contains(text(),"authToken")]/text()').extract()[0].replace('\\','').replace('\n','').replace(' "','').strip())
			linke_a = re.findall('included":(\[.*\])',cv)
			linke_a = json.loads(re.sub('pdfFileName=.*(").*&authType=name','',linke_a[0]))
		except:
			linke_a = {}
	if linke_a:
		enum_l = [i for i,j in enumerate(linke_a) if 'authToken' in j.get('requestUrl','')]
		if enum_l:
			enumd = enum_l[0]
			linkd_javatex = linke_a[enumd].get('requestUrl','')
			linkedin_auth = ''.join(re.findall('authToken=(.*?)&',linke_a[enumd].get('requestUrl','')))
	if meb:
	    cvv = re.findall('\?id=(.*?)&',linkd_javatex)
	    if cvv:
		vb= ',"entityUrn":"urn:li:fs_miniProfile:%s","publicIdentifier":"(.*?)"'%cvv[0]
		urlr =  ''.join(re.findall(vb,meb[0]))
		if not urlr:
			vb= '"urn:li:fs_miniProfile:%s,backgroundImage,com.linkedin.voyager.common.MediaProcessorImage"},"publicIdentifier":"(.*?)"'%cvv[0]
		urlr =  ''.join(re.findall(vb,meb[0]))
		if not urlr:
			urlr = ''.join(re.findall('/voyager/api/identity/profiles/(.*?)/privacySettings', response.body)[-1])
			file("anotherpatter","ab+").write("%s\n" %urlr)
		if urlr:
			urlr = "https://www.linkedin.com/in/%s/"%urlr
			print sk
			execute_query(self.cur, self.query2%(urlr, sk))
	


	

