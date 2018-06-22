import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
from juicer.utils import *
from scrapy.http import Request, FormRequest
import time
import sys
from scrapy.mail import MailSender
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from juicer.items import *
from datetime import timedelta
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from to_udrive import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib,ssl

class PaytmBrowse(JuicerSpider):
    name = 'paytm_browse'
    start_urls = ['https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&channel=web&version=2&child_site_id=1&site_id=1']
    
    def __init__(self, *args, **kwargs):
        super(PaytmBrowse, self).__init__(*args, **kwargs)
	self.conn = MySQLdb.connect(db='paytm_movie', user='root', host='localhost', passwd='root', charset="utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.query = 'insert into Movie(Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,crawler_starttime,reference_url,created_at, modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.meta_query = 'insert into Movie_sessions(sk,session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_starttime,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.select_qry = 'select session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_starttime,reference_url from Movie_sessions where crawler_starttime="%s"'
        self.movie_query = 'select Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,reference_url from Movie where crawler_starttime = "%s"' 
        self.crawler_start_time  = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.session_id = []
        self.url = []
	self.old_records_time = str(datetime.datetime.strptime(self.crawler_start_time, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H'))
	self.del_qry = 'delete from Movie_sessions where crawler_starttime not like "%{0}%"'
        self.del_qry2 = 'delete from Movie where crawler_starttime not like "%{0}%"'
               
    def parse(self,response):
        sel = Selector(response)
        self.cur.execute(self.del_qry.format(self.old_records_time))
        self.cur.execute(self.del_qry2.format(self.old_records_time))
        self.conn.commit()
        result = json.loads(response.body)
        count = 0
        movie_list = result.get('movies',{})
        date_list = []
        date = datetime.datetime.now().date()
	for len_ in range(int(self.min_), int(self.max_)):
		movie_id = movie_list.keys()[len_]
		movie = movie_list[movie_id]
		m_title = movie['title'].replace('(', '').replace(')', '').replace(' ', '-').replace('--', '')
                main_url = 'https://paytm.com/movies/chennai'
		movie_link = 'https://paytm.com/movies/chennai/%s-m/%s?fromdate=%s'%(m_title, movie_id, str(date))
                yield Request(movie_link,callback=self.parse_date, meta={'movie_id':movie_id,'ref_url':main_url,'count':count},dont_filter=True)

    def parse_date(self, response):
	sel = Selector(response)
	day_data = extract_list_data(sel, '//div[@class="ElCQ"]/text()')
	check_date = datetime.datetime.now().date()
	check_day = str(check_date).split('-')[-1]
	movie_id = response.meta['movie_id']
	main_url = response.meta['ref_url']
	count = response.meta['count']
	for day in day_data:
	    date_ = int(day) - int(check_day)
	    fromdate = datetime.datetime.now().date()+datetime.timedelta(days=date_)
	    movie_link = 'https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&moviecode=%s&fromdate=%s'%(movie_id,str(fromdate))
 	    yield Request(movie_link,callback=self.parse_availability, meta={'movie_id':movie_id,'ref_url':main_url,'date':str(fromdate),'count':count},dont_filter=True)

    def parse_availability(self,response):
	sel = Selector(response)
        data_ = json.loads(response.body)
        date = response.meta.get('date','')
        count = response.meta.get('count',0)
        movie_id = response.meta.get('movie_id','')
        movies = data_.get('movies',{}).get(movie_id,'')
        movie_title = movies.get('title','')
        movie_title_ = movie_title.replace(' ','-').lower().replace('(','').replace(')','')
        image_url = movies.get('image_url','')
        censor = movies.get('censor','')
        genre = movies.get('genre','')
        content = movies.get('content','')
        duration = movies.get('duration','')
        trailor_url = movies.get('urlForTrailer','')
        language = movies.get('language','')
        opening_date = movies.get('openingDate','')
        reference_url = "https://paytm.com/movies/chennai/" + movie_title_ + '-m/'+movie_id+'?' +'fromdate='+ date
        aux_info = ''
        vals = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
        vals = (movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,self.crawler_start_time,reference_url)
        self.cur.execute(self.query,vals)
        movie_dict = {}
        if movies :
            sessions = movies.get('sessions',[])        
            for session in sessions :
                theater_name = session.get('cinemaName','')
                provider_name = session.get('providerName','')
                address = session.get('address','')
                latitude = session.get('latitude','')
                longitude = session.get('longitude','')
                multiple_ticket = session.get('multipleEticket','')
                session_id = session.get('sessionId','')
                cinema_id = session.get('cinemaId','')
                scree_on_top = str(session.get('screenOnTop',''))
                provider_id = str(session.get('providerId',''))
                free_seating = session.get('freeSeating','')
                audi = session.get('audi','')
                token_fee_only = session.get('tokenFeeOnly','')
                token_fee_pickup_time = session.get('tokenFeePickupTime','')
                grouped_seats = session.get('groupedSeats','')
                max_tickets = session.get('maxTickets','')
                real_show_time = session.get('realShow')
                is_disable = session.get('is_disable','')
                if real_show_time :
                    time = real_show_time.replace('T',' ').replace('.000Z','')
                    try : 
                        datetime_format = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
                        real_show_time =  str(datetime_format + timedelta(hours=5, minutes=30))
                    except : real_show_time = ''
                session_details = session.get('sessionDetails',[]) 
                ticket_info =  {}
                for i in session_details :
                    seats_total = i.get('seatsTotal','')
                    price = i.get('priceDetails',{})
                    ticket_type = str(price.get('tTypeDescription','')).upper().replace('3D','').strip()
                    ticket_price = price.get('price','')
                    ticket_info.update({ticket_type:ticket_price})
                if session_id and cinema_id :
			referrer = reference_url + '&movieCode='+ movie_id + '&cinemaId=' + str(cinema_id) + '&sessionId=' + str(session_id)
                        headers = {'Host': 'apiproxy-moviesv2.paytm.com',
                    		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:56.0) Gecko/20100101 Firefox/56.0',
                    		'Accept': '*/*',
                    		'Accept-Language': 'en-US,en;q=0.5',
                    		'Content-type': 'application/json; charset=utf-8',
                    		'Referer': referrer,
                    		'Origin': 'https://paytm.com',
                   		}
                        headers1 = {'Pragma': 'no-cache',
                    		'Access-Control-Request-Method': 'POST',
                    		'Origin': 'https://paytm.com',
                    		'Accept-Encoding': 'gzip, deflate, br',
                    		'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
                    		'Accept': '*/*',
                    		'Cache-Control': 'no-cache',
                    		'Connection': 'keep-alive',
                    		'Access-Control-Request-Headers': 'content-type',
                        	}
                        data = {"cinemaId":"%s" % cinema_id,"sessionId":"%s" % session_id,"providerId":int(provider_id),"screenOnTop":int(scree_on_top)}
                        link = 'https://apiproxy-moviesv2.paytm.com//v1/movies/select-seat?channel=WEB&child_site_id=1&site_id=1&version=2'

                        yield Request(link, callback = self.parse_again, headers=headers1, method='OPTIONS', meta = {'referer':referrer, "headers":headers, "data":data, "provider_name":provider_name, "headers1":headers1, "link":link,'ticket_info': json.dumps(ticket_info),'session_id':session_id,'movie_id':movie_id,'theater_name':theater_name,'provider_name':provider_name,'address':address,'latitude':latitude,'longitude':longitude,'multiple_ticket':multiple_ticket,'audi':audi,'real_show_time':real_show_time,'free_seating':free_seating,'token_fee_only':token_fee_only,'token_fee_pickup_time':token_fee_pickup_time,'grouped_seats':grouped_seats,'max_tickets':max_tickets,'is_disable':is_disable,'reference_url':reference_url}, dont_filter=True)


    def parse_again(self, response):
        headers = response.meta.get('headers', '')
        referrer = response.meta.get('referer', '')
        data = response.meta.get('data', '')
	link = response.meta.get('link', '')
	yield Request(link, callback = self.parse_next, headers=headers, body=json.dumps(data), method='POST',meta =response.meta)

    def parse_next(self,response):
        	sel = Selector(response)
		data = json.loads(response.body)
                self.url.append(response.url)
		obj_area = data.get('seatLayout',{}).get('colAreas',{}).get('objArea',[])
		for node in obj_area :
		    rows = node.get('objRow',[])
		    area = node.get('AreaDesc','').upper()
                    if  area =='PR' : area = 'PREMIERE'
                    elif area == 'CL' : area = 'CLUB'
                    elif area == 'SL' : area = 'SILVER'
                    elif area == 'EX' : area = 'EXECUTIVE'
		    ticket_ = response.meta.get('ticket_info','')
                    ticket_price = json.loads(ticket_).get(area,'')
                    seat_avail,seat_unavail = [],[]
		    for row in rows:
			total_seats = row.get('objSeat',[])
			for seat_status_ in total_seats:
			    seat_status = int(seat_status_.get('SeatStatus',''))
			    if seat_status == 0 : seat_avail.append(seat_status)
			    elif seat_status == 1 : seat_unavail.append(seat_status)
			    elif seat_status == 3 : seat_unavail.append(seat_status)
			    elif seat_status == 4 : seat_unavail.append(seat_status)
			    else : seat_unavail.append(seat_status)
		        seats_total =  len(seat_avail) + len(seat_unavail)
                        seats_avail = len(seat_avail)
                        seats_unavail = len(seat_unavail)
                        session_id = response.meta.get('session_id','')
			movie_id = response.meta.get('movie_id','')
			theater_name = response.meta.get('theater_name','')
			provider_name = response.meta.get('provider_name','')
			address = response.meta.get('address','')
			latitude =  response.meta.get('latitude','')
			longitude = response.meta.get('longitude','')
			multiple_ticket = response.meta.get('multiple_ticket','')
			real_show_time = response.meta.get('real_show_time','')
			free_seating = response.meta.get('free_seating','')
			token_fee_only = response.meta.get('token_fee_only','')
			token_fee_pickup_time = response.meta.get('token_fee_pickup_time','')
			grouped_seats = response.meta.get('grouped_seats','')
			max_tickets = response.meta.get('max_tickets','')
			reference_url =  response.meta.get('reference_url','')
			aux_info = ''
			is_disable = response.meta.get('is_disable','')
			audi =  response.meta.get('audi','')
                        is_disable = response.meta.get('movie_dict',{}).get('is_disable','')
                        audi =  response.meta.get('movie_dict',{}).get('audi','')  
                        sk = md5(str(session_id)+str(movie_id)+str(real_show_time)+str(area))
                    self.session_id.append(session_id)
                    vals1 = (sk,session_id,movie_id,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,area,ticket_price,self.crawler_start_time,reference_url)
                    vals1_ = [session_id,movie_id,theater_name,provider_name,address,latitude,longitude,multiple_ticket,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,area,ticket_price,is_disable,reference_url]
                    self.cur.execute(self.meta_query,vals1)
                    seat_avail,seat_unavail,total_seats_ = [],[],[]

