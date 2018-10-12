import json
import md5
import scrapy
import MySQLdb
import csv
from mcmaster_config import *
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import datetime
from juicer.utils import *

class McmasterTerminal(JuicerSpider):
    name = 'mcmaster_data_terminal'
    handle_httpstatus_list = [403, 500]


    def __init__(self, *args, **kwargs):
        super(McmasterTerminal, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db='MCMASTER',user='root',passwd='root', host='localhost', use_unicode=True)
        self.cur = self.conn.cursor()
        self.header_params = ['id','title','Image','Description','Price','Item_data','Reference_url','Main_link']
	self.excel_file_name = 'Mcmaster_sample_data_on_%s.csv'%str(datetime.datetime.now().date())
        self.inser_qry = 'insert into mcmaster(sk,title,category,description,image_url,price,item_data,reference_url,main_link,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())on duplicate key update title=%s, description=%s, image_url=%s, item_data=%s,reference_url=%s,modified_at = now()'
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        

    def spider_closed(self, spider):
	print "spider closed"
        self.cur.close()
        self.conn.close()

    '''def parse(self, response):
	url = response.url.replace('%E2%80%A1', '').replace('%E2%80%A2', '').encode('ascii','ignore').decode()
	#import pdb;pdb.set_trace()
	yield Request(url, self.parse_next, meta=response.meta, dont_filter=True)'''

    def parse(self, response):
	sel = Selector(response)
        print response.meta
        if response.status==403 :
            proxy = response.meta.get('proxy','')
            #self.send_mail(proxy)
	print response
	try:
            price = response.meta.get('data','').get('price','')
            product_id = response.meta.get('data','').get('product_id','').replace(u'\u2022', '')
            price_link = response.meta.get('data','').get('constructed_url','')
            category = normalize(response.meta.get('data','').get('category',''))
	except:
	    price = json.loads(response.meta.get('data','')).get('price','')
            product_id = json.loads(response.meta.get('data','')).get('product_id','').replace(u'\u2022', '')
            price_link = json.loads(response.meta.get('data','')).get('constructed_url','')
            category = normalize(json.loads(response.meta.get('data','')).get('category',''))
        aux_info = {}
        image = "".join(sel.xpath('//div[contains(@id,"ImgCaptionCntnr")]//img//@src').extract())
        title = normalize("".join(sel.xpath('//h3[contains(@class,"header")]//text()').extract()))
        desc = normalize("".join(sel.xpath('//div[@class="CpyCntnr"]//text()').extract()))
        nodes = sel.xpath('//div[@class="cntnr--product-info"]//table[@class="spec-table--pd"]//tr')
        for node in nodes :
		header = normalize("".join(node.xpath('.//td[1]//text()').extract()))
                value =  normalize("".join(node.xpath('.//td[2]//text()').extract()))
                aux_info.update({header:value})

        aux_info = json.dumps(aux_info)
        values = (product_id,title,category,desc,image,price,aux_info,response.url,price_link, title, desc,image, aux_info,response.url)
 
        if title: 
            self.cur = self.conn.cursor()
            self.cur.execute(self.inser_qry,values)
	    self.conn.commit()
            self.got_page(product_id,1)
       

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
           #part = MIMEBase('application', "octet-stream")
           #part.set_payload(open(self.excel_file_name , "rb").read())
           #encoders.encode_base64(part)
           #part.add_header('Content-Disposition', 'attachment', filename = self.excel_file_name)
           #msg.attach(part)
           tem = MIMEText(''.join(mas), 'html')
           msg.attach(tem)
           s = smtplib.SMTP('smtp.gmail.com:587')
           s.ehlo()
           s.starttls()
           s.ehlo()
           s.login(sender_mail,sender_pass)
           s.sendmail(sender_mail, receivers, msg.as_string())
           s.quit()
       
