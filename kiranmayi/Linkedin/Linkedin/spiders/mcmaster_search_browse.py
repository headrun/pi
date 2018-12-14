import json
import scrapy
import MySQLdb
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import re

class McmasterSearchBrowse(BaseSpider):
    name = 'mcmaster_search_browse'
    handle_httpstatus_list = [403, 500, 502, 400]

    def __init__(self, *args, **kwargs):
        super(McmasterSearchBrowse, self).__init__(*args, **kwargs)
	self.mvcode = 'mv1543321786'
	self.conn = MySQLdb.connect(db='MCMASTER',user='root',passwd='root', host='localhost', use_unicode=True)
        self.cur = self.conn.cursor()
	self.query = 'insert into mcmaster_headers_crawl(sk, url, crawl_status, meta_data, created_at, modified_at) values(%s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now()'
	dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def start_requests(self):
	link = 'https://www.mcmaster.com/%s/WebParts/SrchRsltWebPart/WebSrchEng.aspx?inpArgTxt=%s'
	word = 'Phillips screws'
	search_link = link%(self.mvcode, word.lower().replace(' ','-'))
	yield Request(search_link, self.parse, meta={'word':word})

    def parse(self, response):
        body = json.loads(response.body)
	word = response.meta['word']
	l_word = word.lower()
	if body:
	    body = body[0]
	    id_ = str(body['WebSrchEngMetaDat']['FastTrackSrchRsltId']).split('.')[0]
	    link = 'https://www.mcmaster.com/%s/webparts/content/ProdPageWebPart/ProdPageWebPart.aspx?cntnridtxt=MainContent&srchidtxt=%s&cntnrwdth=1531&srchrsltdisplovrdind=false&specsrchhexnutsovrdind=false&landingpagesuppressedind=false&srchrslttxt=%s&expandedprsnttns=&viewporthgt=289&envrmgrcharsetind=3'%(self.mvcode, id_, l_word)
	    yield Request(link, self.parse_search, meta={'word':word, 'sk':id_, 'l_word':l_word, 'link':link})

    def parse_search(self, response):
	sel = Selector(response)
	nodes = sel.xpath('//div[contains(@class, "AbbrPrsnttn floated PrsnttnStructure")]')
	sk = response.meta['sk']
	word = response.meta['word']
	l_word = response.meta['l_word']
	link = response.meta['link']
	strings = link.split(l_word)
	anchorprodsetid = ''.join(re.findall('AnchorProdSetId":(.*),"AnchorStateIsSet', response.body)).split('.')[0]
	for node in nodes:
	    type_id = ''.join(node.xpath('./@prodsetid').extract())
	    type_ = ' '.join(node.xpath('.//h3[@class="AbbrPrsnttn_PrsnttnNm"]//text()').extract())
	    type_desc = ' '.join(node.xpath('.//p[@class="PrsnttnCpy"]//text()').extract())
	    type_link = '%s%s&GrpUsrInps=[{"AnchorProdSetId":"%s","AnchorStateIsSet":false,"GrpEID":"","ProdSetId":"%s"}]%s'%(strings[0], l_word, anchorprodsetid, type_id, strings[1])
	    if 'Tapping' in type_:
	    	yield Request(type_link, self.parse_type, meta={'word':word, 'sk':sk, 'l_word':l_word, 'link':link, 'type_id':type_id, 'type':type_, 'type_desc':type_desc})

    def parse_type(self, response):
	sel = Selector(response)
	#nodes = sel.xpath('//table[@class="ItmTbl"]')
	nodes = sel.xpath('//table[contains(@class, "ItmTbl")]')
	if not nodes:
	    yield Request(response.url, self.parse_subtype, meta=response.meta, dont_filter=True)
	desc1 = response.meta.get('type_desc', '')
	desc2 = response.meta.get('sub_inner_desc', '')
	desc3 = response.meta.get('sub_inner_inner_desc', '')
        for node in nodes :
            headers = node.xpath('.//td[contains(@class,"Price")]//span//text()').extract()
            product_link  = node.xpath('.//td[contains(@class,"ItmTblCellPartNbr")]')
	    '''if response.meta.get('sub_inner_type', '') == 'Drilling Screws for Joining Insulation to Metal':
		import pdb;pdb.set_trace()'''
            for inner_node in product_link :
            	product_id = "".join(inner_node.xpath(".//text()").extract())
		main_cat = response.meta.get('type', '')+'<>'+response.meta.get('sub_type', '')+'<>'+response.meta.get('sub_inner_type', '')+'<>'+response.meta.get('sub_inner_inner_type', '')
		main_cat = main_cat.strip('<>')
                id_ = "".join(inner_node.xpath("./@data-mcm-prodgrps").extract())
                price = inner_node.xpath('./following-sibling::td[contains(@class,"ItmTblCellPrce") and contains(@data-mcm-prodgrps, "%s")]/text()'%id_).extract()
                if len(price)>1 :
                        price1 = headers[0] + ':' + price[0]
                        price2 = headers[1] + ':' + price[1]
                        price = price1+"<>"+price2
                else : price = "".join(price)
                ref_url = "https://www.mcmaster.com/#"+ product_id
                meta_data = {"constructed_url":response.url,'price':price,'product_id':product_id,'main_cat':main_cat,'ref_url':ref_url, 'type_desc1':desc1, 'type_desc2':desc2, 'type_desc3':desc3}
		url = 'https://www.mcmaster.com/%s/WebParts/Content/ItmPrsnttnWebPart.aspx?partnbrtxt=%s'%(self.mvcode, product_id)
		#import pdb;pdb.set_trace()
		#values = (product_id.encode('utf8'), url.encode('utf8'), '0', MySQLdb.escape_string(json.dumps(meta_data)))
		values = (product_id.encode('utf8'), url.encode('utf8'), '0', json.dumps(meta_data))
		self.cur.execute(self.query, values)
		self.conn.commit()

    def parse_subtype(self, response):
	sel = Selector(response)	
	sk = response.meta['sk']
	type_id = response.meta['type_id']
	l_word = response.meta['l_word']
	type_ = response.meta['type']
	type_desc = response.meta['type_desc']
	nodes = sel.xpath('//div[@id="ProdPrsnttnGrpCntnr"][@prodsetid]')
	for node in nodes:
	    sub_type = ' '.join(node.xpath('.//h3[@class="GroupPrsnttn_PrsnttnNm"]//text()').extract())
	    inner_nodes = node.xpath('.//div[contains(@class, "AbbrPrsnttn floated PrsnttnStructure")]')
	    for i_node in inner_nodes:
		sub_inner_type = ' '.join(i_node.xpath('.//h3[@class="AbbrPrsnttn_PrsnttnNm"]//text()').extract())
		sub_inner_id = ''.join(i_node.xpath('.//@prodsetid').extract())
		sub_inner_desc = ' '.join(i_node.xpath('.//p[@class="PrsnttnCpy"]//text()').extract())
		sub_inner_url = 'https://www.mcmaster.com/%s/WebParts/Content/ContentWebPart/ContentWebPart.aspx?cntnrIDtxt=ProdPageContent&srchidtxt=%s&cntnrwdth=1046&srchrslttxt=%s&GrpUsrInps=[{"AnchorProdSetId":"%s","AnchorStateIsSet":true,"GrpEID":"","ProdSetId":"%s"}]&viewporthgt=295&envrmgrcharsetind=3'%(self.mvcode, sk, l_word, sub_inner_id, type_id)
		yield Request(sub_inner_url, self.parse_innersubtype, meta={ 'sk':sk, 'l_word':l_word, 'type_id':type_id, 'type':type_, 'type_desc':type_desc, 'sub_type':sub_type, 'sub_inner_type':sub_inner_type, 'sub_inner_desc':sub_inner_desc})

    def parse_innersubtype(self, response):
	sel = Selector(response)
	sk = response.meta['sk']  
        type_id = response.meta['type_id']
        l_word = response.meta['l_word']
	type_ = response.meta['type']
	type_desc = response.meta['type_desc']
	sub_type = response.meta['sub_type']
	sub_inner_type = response.meta['sub_inner_type']
	sub_inner_desc = response.meta['sub_inner_desc']
	nodes = sel.xpath('//div[contains(@class, "AbbrPrsnttn floated PrsnttnStructure")]')
	if not nodes:
	    yield Request(response.url, self.parse_type, meta=response.meta, dont_filter=True)
	for node in nodes:
	    sub_inner_inner_type = ' '.join(node.xpath('.//h3//text()').extract())
	    sub_inner_inner_id = ''.join(node.xpath('./@prodsetid').extract())
	    sub_inner_inner_desc = ' '.join(node.xpath('.//p[@class="PrsnttnCpy"]//text()').extract())
	    sub_inner_inner_link = 'https://www.mcmaster.com/%s/WebParts/Content/ContentWebPart/ContentWebPart.aspx?cntnrIDtxt=ProdPageContent&srchidtxt=%s&cntnrwdth=1046&srchrslttxt=%s&GrpUsrInps=[{"AnchorProdSetId":"%s","AnchorStateIsSet":true,"GrpEID":"","ProdSetId":"%s"}]&viewporthgt=295&envrmgrcharsetind=3'%(self.mvcode, sk, l_word, type_id, sub_inner_inner_id)
	    yield Request(sub_inner_inner_link, self.parse_type, meta={ 'sk':sk, 'l_word':l_word, 'type_id':type_id, 'type':type_, 'type_desc':type_desc, 'sub_type':sub_type, 'sub_inner_type':sub_inner_type, 'sub_inner_desc':sub_inner_desc, 'sub_inner_inner_type':sub_inner_inner_type, 'sub_inner_inner_desc':sub_inner_inner_desc})
