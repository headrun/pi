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
    name = 'paytm_new_browse'
    start_urls = ['https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&channel=web&version=2&child_site_id=1&site_id=1']
    
    def __init__(self, *args, **kwargs):
        super(PaytmBrowse, self).__init__(*args, **kwargs)
        self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.header_params = ['movie_code','Movie_title','image_url','censor','genre','content','duration','trailor_url','language','opening_date','Reference_url']
        self.header_params1 = ['session_id','Movie_code','theater_name','provider_name','address','latitude','longitude','multiple_ticket','real_show_time','free_seating','token_fee_only','token_fee_pickup_time','grouped_seats','max_tickets','seats_avail','seats_unavail','seats_total','ticket_type','ticket_price', 'crawler_start_time','crawler_end_time','reference_url'] 
        self.query = 'insert into Movie(Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,crawler_starttime,reference_url,created_at, modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.meta_query = 'insert into Movie_sessions(sk,session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_starttime,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.select_qry = 'select session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_starttime,reference_url from Movie_sessions where crawler_starttime="%s"'
        self.movie_query = 'select Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,reference_url from Movie where crawler_starttime = "%s"'
        self.crawler_start_time  = str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.excel_file_name1 = 'paytm_session_data_ON_%s.csv'% self.crawler_start_time
        self.excel_file_name = 'paytm_Movie_data_ON_%s.csv'% self.crawler_start_time
        self.excel_file_name2 = 'Paytm_Session_Data_On_%s.csv'% self.crawler_start_time
        self.excel_file_name3 = 'Paytm_Movie_Data_ON_%s.csv'% self.crawler_start_time
        self.oupf = open(self.excel_file_name, 'ab+')
        self.oupf1 = open(self.excel_file_name1, 'ab+')
        self.oup2 = open(self.excel_file_name2, 'ab+')
        self.oupf3 = open(self.excel_file_name3, 'ab+')
        self.todays_movieef  = csv.writer(self.oupf)
        self.todays_excel_file1  = csv.writer(self.oupf1)
        self.todays_movie  = csv.writer(self.oupf3)
        self.todays_session  = csv.writer(self.oup2)
        self.todays_excel_file1.writerow(self.header_params1)
        self.todays_movieef.writerow(self.header_params)
        self.todays_movie.writerow(self.header_params) 
        self.todays_session.writerow(self.header_params1)
        self.processed_path = '/root/PIFramework/juicer/spiders/paytm_csv_files'
        self.session_id = []
        self.url = []
        self.del_qry = 'delete from Movie_sessions'
        self.del_qry2 = 'delete from Movie'
        dispatcher.connect(self.spider_closed, signals.spider_closed)
               
    def parse(self,response):
        sel = Selector(response)
        self.cur.execute(self.del_qry)
        self.cur.execute(self.del_qry2)
        self.conn.commit()
        result = json.loads(response.body)
        count = 0
        movie_list = result.get('movies',{}).keys()
        date_list = []
        date = datetime.datetime.now().date()
        for i in range(1,7):
            date_list.append(date+datetime.timedelta(days=i))
        for date in date_list :        
            for movie in movie_list :
                movie_link = 'https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&moviecode=%s&fromdate=%s'%(movie,str(date))
                main_url = 'https://paytm.com/movies/chennai'
                yield Request(movie_link,callback=self.parse_availability, meta={'movie_id':movie,'ref_url':main_url,'date':str(date),'count':count},dont_filter=True)

    def spider_closed(self, spider):
        crawler_end_time =  str(datetime.datetime.now() + timedelta(hours=9,minutes=34)).split('.')[0]
        self.cur.execute(self.movie_query % self.crawler_start_time)
        data_ = self.cur.fetchall()
        for row_ in data_ :
            movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url = row_
            vals_data = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
            self.todays_movieef.writerow(vals_data)
            if 'O9IW2O' in movie_id or 'O9IX6F' in movie_id : self.todays_movie.writerow(vals_data) 
        self.cur.execute(self.select_qry % self.crawler_start_time)
        data = self.cur.fetchall()
        for row in data :
                session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_start_time,reference_url = row
                values = [session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,ticket_type,ticket_price,crawler_start_time,crawler_end_time,reference_url]
                self.todays_excel_file1.writerow(values)
                
                if 'O9IW2O' in Movie_code or 'O9IX6F' in Movie_code :self.todays_session.writerow(values)
        statinfo = os.stat(self.excel_file_name1)
        size = statinfo.st_size 
        self.oupf.close()
        self.oupf1.close()
        self.oupf3.close()
        self.oup2.close()
        if size > 0  :
            email_from_list = ['anusha.boyina19@gmail.com']
            files = [self.excel_file_name1,self.excel_file_name]
            for file_ in files :
                file_id = Googleupload().main('Paytm_Availability', email_from_list, file_)
            other = [self.excel_file_name2,self.excel_file_name3]
            for oth in other :
                file_id = Googleupload().main('paytm', email_from_list, oth)     
                #self.alert_mail(email_from_list,file_id, file_)
        self.cur.close()
        self.conn.close()

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
        reference_url = "https://paytm.com/movies/chennai/" + movie_title_ + '/'+movie_id+'?' +'fromdate='+ date
        aux_info = ''
        vals = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
        #self.todays_excel_file.writerow(vals)
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
                free_seating = session.get('freeSeating','')
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
                    try : ticket_info.update({ticket_type:ticket_price})
                    except : import pdb;pdb.set_trace()
                if session_id and cinema_id :
                        referrer = reference_url + '&movieCode='+ movie_id + '&cinemaId=' + str(cinema_id) + '&sessionId=' + str(session_id)
                        headers = {
                    'Host': 'apiproxy-moviesv2.paytm.com',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:56.0) Gecko/20100101 Firefox/56.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-type': 'application/json; charset=utf-8',
                    'Referer': referrer,
                    'Origin': 'https://paytm.com',
                   }
                        headers1 = {
                    'Pragma': 'no-cache',
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

                        yield Request(link, callback = self.parse_again, headers=headers1, method='OPTIONS',meta = {'referer':referrer, "headers":headers, "data":data, "provider_name":provider_name, "headers1":headers1, "link":link,'ticket_info': json.dumps(ticket_info),'session_id':session_id,'movie_id':movie_id,'theater_name':theater_name,'provider_name':provider_name,'address':address,'latitude':latitude,'longitude':longitude,'multiple_ticket':multiple_ticket,'audi':audi,'real_show_time':real_show_time,'free_seating':free_seating,'token_fee_only':token_fee_only,'token_fee_pickup_time':token_fee_pickup_time,'grouped_seats':grouped_seats,'max_tickets':max_tickets,'is_disable':is_disable,'reference_url':reference_url}, dont_filter=True)


    def parse_again(self, response):
        if response.status != 204 and response.status != 200:
                import pdb;pdb.set_trace()
        headers = response.meta.get('headers', '')
        referrer = response.meta.get('referer', '')
        data = response.meta.get('data', '')
        provider_name = response.meta.get('provider_name', '')
        headers1 = response.meta.get('headers1', '')
        link = response.meta.get('link', '')
        movie_dict = response.meta.get('movie_dict',{})
        ticket_info = response.meta.get('ticket_info',{})
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

        yield Request(link, callback = self.parse_next, headers=headers, body=json.dumps(data), method='POST',meta = {'referer':referrer, "headers":headers, "data":data, "provider_name":provider_name, "headers1":headers1, "link":link,'ticket_info':ticket_info,'session_id':session_id,'movie_id':movie_id,'theater_name':theater_name,'provider_name':provider_name,'address':address,'latitude':latitude,'longitude':longitude,'multiple_ticket':multiple_ticket,'audi':audi,'real_show_time':real_show_time,'free_seating':free_seating,'token_fee_only':token_fee_only,'token_fee_pickup_time':token_fee_pickup_time,'grouped_seats':grouped_seats,'max_tickets':max_tickets,'is_disable':is_disable,'reference_url':reference_url},dont_filter=True)

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
			    else : 
				#print seat_status , seat_status_, response.meta.get('real_show_time','')
				seat_unavail.append(seat_status)
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

                        aux_info = ''
                        is_disable = response.meta.get('movie_dict',{}).get('is_disable','')
                        audi =  response.meta.get('movie_dict',{}).get('audi','')  
                        sk = md5(str(session_id)+str(movie_id)+str(real_show_time)+str(area))
                    self.session_id.append(session_id)
                    vals1 = (sk,session_id,movie_id,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,area,ticket_price,self.crawler_start_time,reference_url)
                    vals1_ = [session_id,movie_id,theater_name,provider_name,address,latitude,longitude,multiple_ticket,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_unavail,seats_total,area,ticket_price,is_disable,reference_url]
                    self.cur.execute(self.meta_query,vals1)
                    seat_avail,seat_unavail,total_seats_ = [],[],[]

    def send_mail(self):
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            import smtplib,ssl
            sender_mail = 'positiveintegersproject@gmail.com'
            sender_pass = 'integers'
            #receivers = 'anushab@headrun.com'
            #receivers = 'chetan.m@positiveintegers.com'
	    receivers = 'chlskiranmayi@gmail.com'
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "paytm Movie session data on %s" % str(datetime.datetime.now().date())
            msg['From'] = sender_mail
            msg['To'] = ''.join(receivers)
            msg['Cc'] = 'kiranmayi@headrun.com'
            mas = 'Hi,  please find the data for paytm sessions'
            files = [self.excel_file_name1,self.excel_file_name]
            for file_ in files :
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(file_ , "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename = file_)
                msg.attach(part)
                #cmd = "mv '%s' '%s'" % (file_, self.processed_path)
                #os.system(cmd)
            tem = MIMEText(''.join(mas), 'html')
            msg.attach(tem)
            s = smtplib.SMTP('smtp.gmail.com:587')
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender_mail,sender_pass)
            s.sendmail(sender_mail, receivers, msg.as_string())
            s.quit()

    def alert_mail(self, email_from_list, file_id, paytm_file_name):
        sender_mail = 'positiveintegersproject@gmail.com'
        receivers_mail_list = email_from_list
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'paytm session data on %s' % self.crawler_start_time
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
	
