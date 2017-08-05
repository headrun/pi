from linkedin_voyage_queries import *
from Linkedin.items import *
from linkedin_voyager_connections_browse import *

class Linkedinconnectn(Lvoyagergetlogin):
    name = "linkedin_voyagerconnections_terminal"
    allowed_domains = ["linkedin.com"]

    def __init__(self, name=None, **kwargs):
        super(Linkedinconnectn, self).__init__(name, **kwargs)
        self.conn_url = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
	cv = requests.get('https://www.linkedin.com/logout/').text
	
    def parse(self, response):
	sel = Selector(response)
	member_xpath = ''.join(sel.xpath('//*[contains(text(),"publicContactInfo")]/text()').extract())
	meb_id, sk = ['']*2
	if member_xpath:
		meb_id = ''.join(re.findall('"objectUrn":"urn:li:member:(.*?)",',member_xpath))
		meb_name = ''.join(re.findall('publicIdentifier":"(.*?)"', member_xpath))
		sk = normalize("%s%s"%(str(meb_id),str(meb_name)))
	cooki_list = response.request.headers.get('Cookie', [])
	li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
	headers = {
		'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
		'x-requested-with': 'XMLHttpRequest',
		'csrf-token': response.meta['csrf_token'],
		'authority': 'www.linkedin.com',
		'referer': 'https://www.linkedin.com/',}
	meb_ver_tag = ''
	member_version_tag = extract_data(sel, '//code[contains(text(),"/identity/profiles/")]/text()')
	if member_version_tag:
		meb_ver_tag = re.findall('/profiles/(.*?)/versionTag', member_version_tag)
		if meb_ver_tag:
			meb_ver_tag = meb_ver_tag[0]
		else:
			meb_ver_tag = ''
	yield Request(self.conn_url, callback=self.parse_connectionscount, meta={'sk':sk, "headers": headers})

    def parse_connectionscount(self, response):
	sk = response.meta['sk']
	sel = Selector(response)
	headers = response.meta.get('headers','')
	num_of_connections = ''
	try:
		num_of_connections = json.loads(sel.xpath('//code[contains(text(),"numConnections")]/text()').extract()[0].strip('\n').strip()).get('data',{}).get('numConnections','')
	except:
		num_of_connections = ''
	list_of_urlsva = []
	if num_of_connections:
		print int(num_of_connections), '>>>>>>>>>>>'
		if int(num_of_connections)<=2000:
			countneed_urls = "https://www.linkedin.com/voyager/api/relationships/connections?count=%s&start=0" % str(num_of_connections)
			list_of_urlsva.append(countneed_urls)
		else:
			set_limit_to = '2000'
			start_limit_to = '0'
			for ic in range(int(num_of_connections)):
				urlsn = "https://www.linkedin.com/voyager/api/relationships/connections?count=%s&start=%s" % (str(set_limit_to), str(start_limit_to))
				list_of_urlsva.append(urlsn)
				if int(set_limit_to)+int(start_limit_to)>int(num_of_connections):
					break
				else:
					start_limit_to = str(int(set_limit_to)+ int(start_limit_to))
	for cuvoyager in list_of_urlsva:
		yield Request(cuvoyager, callback=self.parse_connections, meta={'sk':sk, 'headers':headers}, dont_filter=True, headers=headers)

        status_of_mb = 'crawled'
        if not list_of_urlsva and not int(num_of_connections): status_of_mb = 'not available'
	account_item = Linkedinaccounts()
	account_item['profile_sk'] = sk
	account_item['status'] = normalize(status_of_mb)
	account_item['exact_connections_count'] = normalize(str(num_of_connections))
	account_item['reference_url'] = normalize(self.conn_url)
	if account_item['profile_sk']: yield account_item



    def parse_connections(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
	headers = response.meta.get('headers')
	temp = {}
	try:
		temp = json.loads(response.body)
	except:
		temp = {}
	if temp:
		print len(temp.get('elements',[])), '*********'
		for element in temp.get('elements',[]):
			emt_createdat = element.get('createdAt', '') 
			emt_entityurn = element.get('entityUrn', '')
			emt_miniprofile = element.get('miniProfile',{})
			emt_entityurnmp = emt_miniprofile.get('entityUrn', '')
			emt_firstname = emt_miniprofile.get('firstName', '')
			emt_lastname = emt_miniprofile.get('lastName', '')
			emt_objecturn = emt_miniprofile.get('objectUrn', '')
			headline = emt_miniprofile.get('occupation', '')
			emt_picture = emt_miniprofile.get('picture', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
			emt_background_image = emt_miniprofile.get('backgroundImage', {}).get('com.linkedin.voyager.common.MediaProcessorImage', {}).get('id', '')
			if emt_background_image:
				emt_background_image = "https://media.licdn.com/media%s" % (emt_background_image)
			emt_publicidentifier = emt_miniprofile.get('publicIdentifier', '')
			emt_tracking = emt_miniprofile.get('trackingId', '')
			conne_na = "%s%s%s" % (emt_firstname, ' ', emt_lastname)
			mem_pic, pview  = ['']*2
			if emt_picture:
				mem_pic = "https://media.licdn.com/media%s" % (emt_picture)
			if emt_publicidentifier:
				pview = "https://www.linkedin.com/in/%s/" % emt_publicidentifier
			memberID = ''.join(re.findall('\d+', emt_objecturn))
			sk_connect = md5(sk+conne_na+mem_pic+memberID+pview+headline)
			conne_item = LinkedinItem()
			conne_item['sk'] = normalize(sk_connect)
			conne_item['profile_sk'] = normalize(sk)
			conne_item['connections_profile_url'] = normalize(pview)
			conne_item['headline'] = normalize(headline)
			conne_item['member_id'] = normalize(memberID)
			conne_item['name']  = normalize(conne_na)
			conne_item['image_url'] = normalize(mem_pic)
		   	conne_item['reference_url'] = normalize(response.url)
			conne_item['background_image_url'] = normalize(emt_background_image)
			if mem_pic: 
			    yield ImageItem(image_urls=[mem_pic])
			    hashs = hashlib.sha1((mem_pic).encode('utf-8', 'strict')).hexdigest()
			    conne_item['image_path'] =  "%s%s%s"%(profile_images_path, hashs, '.jpg')
			if conne_item['sk']: yield conne_item

