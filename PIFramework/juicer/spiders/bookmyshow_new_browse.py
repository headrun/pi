import scrapy
import requests
import csv
from juicer.utils import *
from datetime import timedelta
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from to_udrive import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib,ssl
import shutil

class Bookmyshow(JuicerSpider):
    name = "bookmyshow_new_browse"
    allowed_domains = ['bookmyshow.com']
    start_urls = ['https://in.bookmyshow.com/chennai/movies']
    
    def __init__(self, *args,  **kwargs):
        super(Bookmyshow, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.header_params = ['Session_id', 'Movie_name','Movie_code','Theatre_name','Release_date','Movie duration','Genre','showtime','Available_seats','Not_Available','Total_seats','Ticket_type','Price','Availability_status','Crawler start time','Crawler_end_time','Reference_url'] 
        self.meta_query = 'insert into bookmyshow_sessions(sk,movie_title,Movie_code,session_id,theater_name,release_date,duration,genre,real_show_time,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,status,crawler_starttime,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.select_qry = 'select session_id,movie_title,Movie_code,theater_name,release_date,duration,genre,real_show_time,seats_avail, seats_unavail, seats_total,ticket_type,ticket_price,status,crawler_starttime,reference_url from bookmyshow_sessions where crawler_starttime = "%s"'
        self.crawler_start_time = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.excel_file_name = 'Bookmyshow_session_data_ON_%s.csv'% self.crawler_start_time
        self.oupf = open(self.excel_file_name, 'wb+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.header_params)
        self.processed_path = '/root/PIFramework/juicer/spiders/paytm_csv_files'
        self.del_qry = 'delete from bookmyshow_sessions'
        self.cur.execute(self.del_qry)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        sel = Selector(response)
	movies = sel.xpath('//div[@class="mv-row"]/div[@class="card-container wow fadeIn movie-card-container"]')
        for movie in movies:
	    url = ''.join(movie.xpath('./a/@href').extract()) 
	    if url:
                normal_url = 'https://in.bookmyshow.com' + url
                yield Request(normal_url, callback = self.parse_book,dont_filter=True)

    def parse_book(self, response):
	sel = Selector(response)
	booking_link = extract_list_data(sel, '//div[@class="more-showtimes"]/a/@href')
	if booking_link:
		booking_link = 'https://in.bookmyshow.com' + booking_link[0]
		yield Request(booking_link, callback = self.parse_new, dont_filter=True)

    def parse_new(self, response):
        format_ = response.meta.get('format_','')
        sel = Selector(response)
        day = sel.xpath('//div[@class="date-container "]/ul/li/a/@href').extract()
        for i in day:
	    day_navigation_url = 'https://in.bookmyshow.com' + i
            yield Request(day_navigation_url,callback=self.parse_meta,meta={'main_url':format_},dont_filter=True)
	
    def parse_meta(self,response):
        sel = Selector(response)        
        movie_code = response.url.split('/')[-2]
        main_url = response.meta.get('main_url','')
        date_ = response.url.split('/')[-1]
        date = str(datetime.datetime.strptime(str(date_),'%Y%m%d').date())
        movie_name = ''.join(sel.xpath('//div[@class="cinema-name-wrapper"]/a//text()').extract()).strip()
        genre = "<>".join(sel.xpath('//span[@class="__genre-tag"]//text()').extract())
        percent = "".join(sel.xpath('//span[@class="__percent"]//text()').extract())
        no_of_votes = "".join(sel.xpath('//span[@class="__votes"]//text()').extract())
        try : rel_date = normalize("".join(sel.xpath('//span[@class="__release-date"]//text()').extract()[0]))
        except : rel_date = ''
        movie_duration = "".join(sel.xpath('//span[@itemprop="duration"]//text()').extract())
        nodes = sel.xpath('//ul[@id="venuelist"]/li[@class="list "]')
        for node in nodes:
                    theatre_name = ''.join(node.xpath('.//a[@class="__venue-name"]//text()').extract()).strip()
                    all_shows =  node.xpath('.//a[contains(@class, "__showtime-link")]')
                    for each_show in all_shows:
                        session_id = ''.join(each_show.xpath('./@data-session-id').extract())
                        venue_code = ''.join(each_show.xpath('./@data-venue-code').extract())
                        availability = each_show.xpath('./@data-cat-popup').extract()
                        url = ''.join(each_show.xpath('./@href').extract())
                        show_time = date +' '+ ''.join(each_show.xpath('./@data-display-showtime').extract())
                        prices = ''.join(each_show.xpath('./@data-cat-popup').extract())
                        avail = ''.join(each_show.xpath('./@data-availability').extract())
                        show_info_link = "https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFO&vid="+str(venue_code)+"&ssid="+str(session_id)
                        if show_info_link :
                            yield Request(show_info_link, callback = self.parse_next, meta= {'url':response.url, 'date':date, 'movie_name':movie_name, 'theatre_name':theatre_name, 'time':show_time, 'main_url':main_url,'avail':avail,'ref_url':response.url,'genre':genre,'rel_date':rel_date,'vote_percent':percent,'no_of_votes':no_of_votes,'movie_dur':movie_duration,'movie_code':movie_code,'session_id':session_id},dont_filter=True)
            
    def parse_next(self, response):
            sel = Selector(response)
            data = json.loads(response.body.replace('arrShowInfo=','').strip(';'))
            session_id = response.meta.get('session_id','')
            movie_title = response.meta.get('movie_name', '')
            movie_code = response.meta.get('movie_code', '')
            theatre_name = response.meta.get('theatre_name','')
            movie_duration = response.meta.get('movie_dur','')
            genre = response.meta.get('genre','')
            rel_date = response.meta.get('rel_date','')
            show_time = response.meta.get('time','')
            availability = response.meta.get('avail','') 
            ref_url = response.meta.get('ref_url','')
            for node in data :
                ticket_type = node[25]
                cost = node[4]
                available_seats = node[38]
                total  = node[37]
                unavail = int(total) - int(available_seats)
                sk = md5(str(session_id)+str(movie_code)+str(theatre_name)+str(show_time)+str(ticket_type))
                values = (sk,movie_title,movie_code,session_id,theatre_name,rel_date,movie_duration,genre,show_time,available_seats,unavail,total,ticket_type,cost,availability,self.crawler_start_time,ref_url)
                self.cur.execute(self.meta_query,values)

    def spider_closed(self, spider):
        crawler_end_time = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.cur.execute(self.select_qry % self.crawler_start_time)
        data = self.cur.fetchall()
        for row in data :
            session_id,movie_title,movie_code,theatre_name,rel_date,movie_duration,genre,show_time,available_seats,unavail,total,ticket_type,cost,availability,self.crawler_starttime,ref_url = row
            vals = [session_id,movie_title,movie_code,theatre_name,rel_date,movie_duration,genre,show_time,available_seats,unavail,total,ticket_type,cost,availability,self.crawler_starttime,crawler_end_time,ref_url]
            self.todays_excel_file.writerow(vals)
        statinfo = os.stat(self.excel_file_name)
        size = statinfo.st_size
        if size > 0  :
            self.oupf.close()
            email_from_list = ['anusha.boyina19@gmail.com']
            file_id = Googleupload().main('Bookmyshow_Availability', email_from_list, self.excel_file_name)
	    move_file('/root/PIFramework/juicer/spiders/"%s"'%self.excel_file_name, '/root/PIFramework/juicer/spiders/paytm_csv_files')
        self.cur.close()
        self.conn.close()

    def alert_mail(self, email_from_list, file_id, paytm_file_name):
        sender_mail = 'positiveintegersproject@gmail.com'
        receivers_mail_list = email_from_list
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Bookmyshow session data on %s' % self.crawler_start_time
        mas = '<p>File name : %s</p>'% str(paytm_file_name)
        mas += '<p>File is uploaded in paytm [sub-folder] of paytm_session_data [folder] in google drive of %s</p>' % sender_mail
        mas += '<p>Doc Link : "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
        msg['From'] = sender
        msg['To'] = receivers
        tem = MIMEText(''.join(mas), 'html')
        msg.attach(tem)
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        s.login(sender_mail, 'integers')
        s.sendmail(sender, receivers_mail_list, msg.as_string())
        s.quit()

                
