import json
import scrapy
import MySQLdb
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import ast

class McmasterBrowse(BaseSpider):
    name = 'mcmaster_browse'
    handle_httpstatus_list = [403, 500, 502]

    def __init__(self, *args, **kwargs):
        super(McmasterBrowse, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db='MCMASTER',user='root',passwd='root', host='localhost', use_unicode=True)
        self.cur = self.conn.cursor()	
        #self.conn1 = MySQLdb.connect(db='urlqueue_dev',user='root',passwd='root', host='localhost', use_unicode=True)
        #self.cur1 = self.conn1.cursor()
        self.inser_qry = 'insert into mcmaster(sk,title,category,description,image_url,price,item_data, aux_info, reference_url,main_link,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())on duplicate key update title=%s, description=%s, image_url=%s, item_data=%s,reference_url=%s,category=%s,modified_at = now()'
	self.query1 = 'update ignore mcmaster_headers_crawl set crawl_status=%s, modified_at=now() where sk=%s'
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def start_requests(self):
	query = "select sk,url,meta_data from mcmaster_headers_crawl where crawl_status=0 order by rand() limit 2"
	self.cur.execute(query)
	rows = self.cur.fetchall()
	for row in rows:
	    sk , url, meta_data = row
	    '''import pdb;pdb.set_trace()
	    try:
		meta_data = json.loads(str(meta_data).replace('\\',""))
	    except:
	    	meta_data = json.loads(ast.literal_eval(meta_data))'''
	    meta_data = json.loads(meta_data)
	    yield Request(url.replace('*',''), self.parse, meta=meta_data)
	#url = 'https://www.mcmaster.com/mv1542631522/WebParts/Content/ItmPrsnttnWebPart.aspx?partnbrtxt=93175A212'
	#yield Request(url, self.parse)

    def spider_closed(self, spider):
	print "spider closed"
        self.cur.close()
        self.conn.close()
	#self.cur1.close()
        #self.conn1.close()

    def parse(self, response):
	sel = Selector(response)
	price = response.meta.get('price','')
        product_id = response.meta.get('product_id','').replace(u'\u2022', '')
        price_link = response.meta.get('constructed_url','')
        category = response.meta.get('main_cat','').encode('utf8')
	desc1 = response.meta.get('type_desc1','')
	desc2 = response.meta.get('type_desc2','')
	desc3 = response.meta.get('type_desc3','')
	if response.status != 200:
	    q_values = ('2', product_id)
	    self.cur.execute(self.query1,q_values)
            self.conn.commit()
	else:	
	    aux_info = {}
	    image = "".join(sel.xpath('//div[contains(@id,"ImgCaptionCntnr")]//img//@src').extract())
	    title = " ".join(sel.xpath('//h3[contains(@class,"header")]//text()').extract()).encode('utf8', '')
	    desc = " ".join(sel.xpath('//div[@class="CpyCntnr"]//text()').extract()).encode('utf8', '')
	    nodes = sel.xpath('//div[@class="cntnr--product-info"]//table[@class="spec-table--pd"]//tr')
	    item_data = {}
	    for node in nodes :
	        header = "".join(node.xpath('.//td[1]//text()').extract()).encode('utf8')
	        value =  "".join(node.xpath('.//td[2]//text()').extract()).encode('utf8')
	       	item_data.update({header:value})
	    if image and 'http' not in image:
	        image = 'https://images1.mcmaster.com%s'%image
	    if desc1:
		aux_info.update({'type_desc1':desc1})
	    if desc2:
                aux_info.update({'type_desc2':desc2})
	    if desc3:
                aux_info.update({'type_desc3':desc3})
	    aux_info = json.dumps(aux_info)
	    values = (product_id,title,category,desc,image,price,json.dumps(item_data),aux_info,response.url,price_link, title, desc,image, aux_info,response.url, category)
	    #print str(values)
            self.cur.execute(self.inser_qry,values)
	    self.conn.commit()
	    q_values = ('1', product_id)
	    self.cur.execute(self.query1,q_values)
	    self.conn.commit()

    def send_mail(self,proxy):
           from email.mime.multipart import MIMEMultipart
           from email.mime.text import MIMEText
           from email.mime.base import MIMEBase
           from email import encoders
           import smtplib,ssl
           sender_mail = 'positiveintegersproject@gmail.com'
           sender_pass = 'integers'
           receivers = ['jaideep@headrun.com']
           msg = MIMEMultipart('alternative')
           msg['Subject'] = "%s is blocked %s" % (proxy,str(datetime.datetime.now().date()))
           msg['From'] = sender_mail
           msg['To'] = ''.join(receivers)
           msg['Cc'] = 'anushab@headrun.com'
           mas = 'Hi'
           tem = MIMEText(''.join(mas), 'html')
           msg.attach(tem)
           s = smtplib.SMTP('smtp.gmail.com:587')
           s.ehlo()
           s.starttls()
           s.ehlo()
           s.login(sender_mail,sender_pass)
           s.sendmail(sender_mail, receivers, msg.as_string())
           s.quit()
       
