import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
import datetime
from juicer.utils import *
from scrapy.http import Request, FormRequest
import time
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from juicer.items import *
from datetime import timedelta
import openpyxl as px
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from to_udrive import *
import shutil

class TicketNewBrowse(JuicerSpider):
    name = 'ticketnew_browse'
    start_urls = ['http://www.ticketnew.com/online-advance-booking/Movies/C/Chennai']
    
    def __init__(self, *args, **kwargs):
        super(TicketNewBrowse, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.header_params = ['Movie_title','Movie_code','session_id','theater_name','address','published_date','duration','language','genre','actors','director','music','description','real_show_time','max_tickets','seats_avail','seats_unavail','seats_total','ticket_type','ticket_price', 'status','crawler_start_time','crawler_end_time','reference_url']
        self.meta_query = 'insert into Ticketnew_sessions(sk,movie_title,Movie_code,session_id,theater_name,address,published_date,duration,language,genre,actors,director,music,description,real_show_time,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,status,crawler_starttime,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.select_qry = 'select movie_title,Movie_code,session_id,theater_name,address,published_date,duration,language,genre,actors,director,music,description,real_show_time,max_tickets,seats_avail, seats_unavail, seats_total,ticket_type,ticket_price,status,crawler_starttime,reference_url from Ticketnew_sessions where crawler_starttime = "%s"'
        self.crawler_start_time = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.excel_file_name = 'ticketnew_session_data_ON_%s.csv'% self.crawler_start_time
        self.oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.header_params)
        self.processed_path = '/root/PIFramework/juicer/spiders/Paytm_csv_files'
        self.del_qry = 'delete from Ticketnew_sessions'
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        crawler_end_time = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.cur.execute(self.select_qry % self.crawler_start_time)
        data = self.cur.fetchall()
        for row in data :
            movie_title,Movie_code,session_id,theater_name,address,published_date,duration,language,genre,actors,director,music,desc,real_show_time,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,status,crawler_start_time,reference_url = row
            vals = [movie_title,Movie_code,session_id,theater_name,address,published_date,duration,language,genre,actors,director,music,desc,real_show_time,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,status,crawler_start_time,crawler_end_time,reference_url]
            self.todays_excel_file.writerow(vals)
        statinfo = os.stat(self.excel_file_name)
        size = statinfo.st_size
        if size > 0  :
            self.oupf.close()
            email_from_list = ['anusha.boyina19@gmail.com']
            file_id = Googleupload().main('Ticketnew_Availability', email_from_list, self.excel_file_name)
	    move_file('/root/PIFramework/juicer/spiders/"%s"'%self.excel_file_name, '/root/PIFramework/juicer/spiders/Paytm_csv_files')
        self.cur.close()
        self.conn.close()
        
               
    def parse(self,response):
        sel = Selector(response)
        self.cur.execute(self.del_qry)
        self.conn.commit()
        movie_links = sel.xpath('//div[@class="tn-movie tn-section-tile"]//a[contains(@href,"Online-Advance-Booking")]//@href').extract() 
        for movie in movie_links :
            yield Request(movie,callback=self.parse_availability)


    def parse_availability(self,response):
	sel = Selector(response)
        movie_code = response.url.split('/')[-2]
        date_links = sel.xpath('//ul[@id="ulShowDate"]//li//a//@href').extract()
        for link in date_links :
            yield Request(link,callback=self.parse_movie_meta)
        
    def parse_movie_meta(self,response):
        sel = Selector(response)
        movie_title = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//h2//text()').extract())
        lang = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//span[@itemprop="inLanguage"]//text()').extract())
        genre = "<>".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//span[@itemprop="genre"]//text()').extract())
        published_date = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//span[@itemprop="datePublished"]//text()').extract())
        try : duration = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//h6//text()').extract()[-1]).replace('|','')
        except : duration = ''
        actors = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//p[@itemprop="actor"]//text()').extract())
        director = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//p[@itemprop="director"]//text()').extract())
        music = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//p[@itemprop="musicBy"]//text()').extract())
        desc = "".join(sel.xpath('//div[@class="movie-details tn-entity-details"]//p[@itemprop="description"]//text()').extract())
        theatre_nodes = sel.xpath('//div[@class="tn-entity tn-block tn-entity-and-timing-details"]')
        for node in theatre_nodes :
            name = "".join(node.xpath('.//div[@class="tn-entity-details"]//h5//text()').extract())
            address = "".join(node.xpath('.//div[@class="tn-entity-details"]//p//text()').extract())
            timing_nodes = node.xpath('.//div[@class="tn-timing-details"]//ul//li')
            for time_node in timing_nodes :
                time_link = "".join(time_node.xpath('.//a//@data-tkts').extract())
                time = "".join(time_node.xpath('.//a//text()').extract())
                date_ = "".join(time_node.xpath('.//a//@data-date').extract())
                data_event = "".join(time_node.xpath('.//a//@data-event').extract())
                data_venue = "".join(time_node.xpath('.//a//@data-venue').extract())
                real_show_time = date_ + ' ' + time 
                data_ = json.loads(time_link)
                for data in data_ :
                    ticket_type = data.get('Name','')
                    id_ = data.get('Id','')
                    rate = data.get('Rate','')
                    mode = data.get('Mode','')
                    seat_avail = data.get('Avail','')
                    total = data.get('Total','')
                    max_ = data.get('Max','') 
                    color = data.get('Color','')
                    status = data.get('Text','')
                    movie_code = response.url.split('/')[-4]
                 
                    if total==0 and status == 'Available':
                        data = '{"Venue_ID":%s,"Event_Id":"%s","Event_Date":"%s","Level_Id":"%s","Req_Seats":"10","Sel_Mode":"%s","Cancel_Url":"%s"}'%(data_venue,data_event,date_,id_,mode,response.url)
                        headers = {'Accept-Language': 'en-US,en;q=0.9,fil;q=0.8', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'http://www.ticketnew.com', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Referer': response.url, 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Content-Type': 'application/json; charset=UTF-8'}
                        import requests
                        response_text = requests.post('http://www.ticketnew.com/moviepage/EncodeUrl', headers=headers, data=data).text
                        link = 'http://www.ticketnew.com/onlinetheatre/Theatre/' + json.loads(response_text.replace('\\\\','&').replace('u0026','')).get('d').strip('"')
                        yield Request(link,callback=self.parse_meta,meta={'ticket_type':ticket_type,'id_':id_,'rate':rate,'mode':mode,'max_':max_,'status':status,'date_':'date_','reference_url':response.url,'name':name,'real_show_time':real_show_time,'address':address,'movie_title':movie_title,'movie_code':movie_code,'published_date':published_date,'duration':duration,'lang':lang,'genre':genre,'actors':actors,'director':'director','music':music,'desc':desc},dont_filter=True)
                    else :

                        sk = md5(str(ticket_type)+str(id_)+str(rate)+str(mode)+str(seat_avail)+str(status)+str(response.url)+str(time)+str(name))
                        seat_unavail = total - seat_avail
                        vals = (sk,movie_title,movie_code,id_,name,address,published_date,duration,lang,genre,actors,director,music,desc,real_show_time,max_,seat_avail,seat_unavail,total,ticket_type,rate,status,self.crawler_start_time,response.url)
                        self.cur.execute(self.meta_query,vals)

    def parse_meta(self,response):
        sel = Selector(response)
        seat_avail = len(sel.xpath('//table//tr//td[contains(@class,"tn-seat tn-seat-available")]'))
        seat_unavail = len(sel.xpath('//table//tr//td[contains(@class,"tn-seat tn-seat-taken")]'))
        total = seat_avail + seat_unavail
        movie_title = response.meta.get('movie_title','')
        movie_code = response.meta.get('movie_code','')
        id_ = response.meta.get('id_','')
        name = response.meta.get('name','')
        address = response.meta.get('address','')
        published_date = response.meta.get('published_date','')
        duration = response.meta.get('duration','')
        lang = response.meta.get('lang','')
        genre = response.meta.get('genre','')
        actors = response.meta.get('actors','')
        director = response.meta.get('director','')
        music = response.meta.get('music','')
        desc = response.meta.get('desc','')
        real_show_time = response.meta.get('real_show_time','')
        max_ = response.meta.get('max_','')
        ticket_type = response.meta.get('ticket_type','')
        rate = response.meta.get('rate','')
        status = response.meta.get('status','')
        reference_url = response.meta.get('reference_url','')
        mode = response.meta.get('mode')
        sk = md5(str(ticket_type)+str(id_)+str(rate)+str(mode)+str(seat_avail)+str(status)+str(response.url)+str(real_show_time)+str(name))
        vals = (sk,movie_title,movie_code,id_,name,address,published_date,duration,lang,genre,actors,director,music,desc,real_show_time,max_,seat_avail,seat_unavail,total,ticket_type,rate,status,self.crawler_start_time,reference_url)
        self.cur.execute(self.meta_query,vals)

    def send_mail(self):
	    from email.mime.multipart import MIMEMultipart
	    from email.mime.text import MIMEText
	    from email.mime.base import MIMEBase
	    from email import encoders
	    import smtplib,ssl
	    sender_mail = 'positiveintegersproject@gmail.com'
            sender_pass = 'integers'
            receivers = 'chlskiranmayi@gmail.com'
	    msg = MIMEMultipart('alternative')
	    msg['Subject'] = "Ticketnew Movie session data on %s" % str(datetime.datetime.now().date())
	    msg['From'] = sender_mail
	    msg['To'] = ''.join(receivers)
            msg['Cc'] = 'kiranmayi@headrun.com'
            mas = 'Hi,  please find the sample data for ticket new' 
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.excel_file_name , "rb").read())
            encoders.encode_base64(part)
	    part.add_header('Content-Disposition', 'attachment', filename = self.excel_file_name)
            msg.attach(part)
	    tem = MIMEText(''.join(mas), 'html')
 	    msg.attach(tem)
            s = smtplib.SMTP('smtp.gmail.com:587')
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender_mail,sender_pass)
            s.sendmail(sender_mail, receivers, msg.as_string())
            s.quit()
			    

