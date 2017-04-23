from linkedin_queries import *
from Linkedin.items import *
from linkedin_utils import *

class Linkedinconnectn(Lgetlogin):
    name = "linkedinconnectionsnew_terminal"
    allowed_domains = ["linkedin.com"]

    def __init__(self, name=None, **kwargs):
        super(Linkedinconnectn, self).__init__(name, **kwargs)
        self.conn_url = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'
	self.conn_ajax = 'https://www.linkedin.com/profile/profile-v2-connections?id='
	self.conn_ajax2 = '&offset=10&count=10&distance=1&type=INITIAL'
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
		if meb_id:
			url_con = "{}{}{}".format(self.conn_ajax, meb_id, self.conn_ajax2)
		yield Request(url_con, callback=self.parse_connectionscount, meta={'sk':sk,"meb_id":meb_id})
	status_of_mb = 'crawled'
        if not meb_id: status_of_mb = 'no member id'
	if meb_id:
		account_item = Linkedinaccounts()
		account_item['profile_sk'] = sk
		account_item['status'] = normalize(status_of_mb)
		account_item['reference_url'] = normalize(self.conn_url)
		if account_item['profile_sk']: yield account_item

    def parse_connectionscount(self, response):
	sel = json.loads(response.body)
	sk = response.meta['sk']
	meb_id = response.meta.get('meb_id','')
	all_keys = sel.get('content','')
	if all_keys:
		count_co = all_keys.get('connections','').get('i18n__All_numAll','')
		count_co1 = all_keys.get('connections','').get('i18n__Shared_numShared','')
		if count_co:
			countc = int(''.join(re.findall('\((.*?)\)',count_co)).replace(',','').replace('.','').strip())
			if countc == 0: countc = int(''.join(re.findall('\((.*?)\)',count_co1)).replace(',','').replace('.','').strip())
			if countc:
				for imi in range(0,countc,10):
				    if imi>countc:
					break
				    url_con = "{}{}{}{}{}".format("https://www.linkedin.com/profile/profile-v2-connections?id=",meb_id,"&offset=",str(imi),"&count=10&distance=1&type=INITIAL")
				    yield Request(url_con, callback=self.parse_connections, meta={'sk':sk}, dont_filter=True)

    def parse_connections(self, response):
        sel = Selector(response)
        sk = response.meta['sk']
        temp = json.loads(response.body)
        all_keys = temp['content']
        connections_ = all_keys.get('connections','')
        conneimalist, total_connections = [], ''
        if connections_:
            name_connec = connections_.get('connections','')
            for nac in name_connec:
                conne_na = nac.get('fmt__full_name','').replace(u'\U0001f680','').strip().replace(u'\U0001f60e','').strip()
                mem_pic = nac.get('mem_pic','')
		pview = nac.get('pview','')
		headline = nac.get('headline','')
		memberID = str(nac.get('memberID',''))
                conne_naim = ''
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
		if mem_pic: 
		    yield ImageItem(image_urls=[mem_pic])
		    hashs = hashlib.sha1((mem_pic).encode('utf-8', 'strict')).hexdigest()
		    conne_item['image_path'] =  "%s%s%s"%("/root/Linkedin/Linkedin/spiders/images/full/",hashs,'.jpg')
		if conne_item['sk']: yield conne_item

