import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
import datetime
from juicer.utils import *
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from juicer.items import *
from datetime import timedelta

class PaytmBrowse(JuicerSpider):
    name = 'paytm_browse'
    start_urls = ['https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&channel=web&version=2&child_site_id=1&site_id=1']
    
    def __init__(self, *args, **kwargs):
        super(PaytmBrowse, self).__init__(*args, **kwargs)
        #self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        #self.cur = self.conn.cursor()
        self.header_params = ['movie_code','Movie_title','image_url','censor','genre','content','duration','trailor_url','language','opening_date']
        self.header_params1 = ['session_id','Movie_code','theater_name','provider_name','address','latitude','longitude','multiple_ticket','audi','real_show_time','free_seating','token_fee_only','token_fee_pickup_time','grouped_seats','max_tickets','seats_avail','seats_total','ticket_type','ticket_price','reference_url'] 
        self.query = 'insert into Movie(Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,aux_info,reference_url,created_at, modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.meta_query = 'insert into Movie_sessions(session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_total,ticket_type,ticket_price,aux_info,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        self.excel_file_name1 = 'paytm_session_data_ON_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name = 'paytm_movie_data_ON_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        oupf1 = open(self.excel_file_name1, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file1  = csv.writer(oupf1)
        #self.todays_excel_file1.writerow(self.header_params1)
        #self.todays_excel_file.writerow(self.header_params)
               
    def parse(self,response):
        sel = Selector(response)
        result = json.loads(response.body)
        count = 0
        movie_list = movie_list = ['O9IW2O','O9IX6F']
        date = str(datetime.datetime.now().date())
        for movie in movie_list :
            movie_link = 'https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&moviecode=%s&fromdate=%s'%(movie,date)
            main_url = 'https://paytm.com/movies/chennai'
            yield Request(movie_link,callback=self.parse_availability, meta={'movie_id':movie,'ref_url':main_url,'date':date,'count':count},dont_filter=True)

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
        #vals = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
        #self.todays_excel_file.writerow(vals)
        #vals = (movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,'',reference_url)
        #self.cur.execute(self.query,vals)
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
                scree_on_top = session.get('screenOnTop','')
                provider_id = session.get('providerId','')
                free_seating = session.get('freeSeating','')
                if session_id and cinema_id :
                    referrer = reference_url + '&cinemaId=' + str(cinema_id) + '&sessionId=' + str(session_id)
                    headers = {
    'Host': 'apiproxy-moviesv2.paytm.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-type': 'application/json; charset=utf-8',
    'Referer': referrer,
    'Origin': 'https://paytm.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
                data = '{"cinemaId":"%s","sessionId":"%s","providerId":%s,"screenOnTop":%s,"freeSeating":false}'%(cinema_id,session_id,provider_id,scree_on_top)
                import requests 
                seat_avail,seat_unavail = [],[]
                import pdb;pdb.set_trace()
                response = requests.post('https://apiproxy-moviesv2.paytm.com//v1/movies/select-seat', headers=headers, data=data).text
                data = json.loads(response)
                obj_area = data.get('seatLayout',{}).get('colAreas',{}).get('objArea',[])
                for node in obj_area :
                    rows = node.get('objRow',[])
                    area = node.get('AreaDesc','').upper()
                    if  area =='PR' : area = 'PREMIERE'
                    elif area == 'CL' : area = 'CLUB'
                    elif area == 'SL' : area = 'SILVER'
                    elif area == 'EX' : area = 'EXECUTIVE'

                    #ticket_ = response.meta.get('ticket_info','')

                    #ticket_price = json.loads(ticket_).get(area,'')
                    seat_avail,seat_unavail = [],[]
                    for row in rows:
                        total_seats = row.get('objSeat',[])
                        for seat_status_ in total_seats:
                            seat_status = int(seat_status_.get('SeatStatus',''))
                            if seat_status == 0 : seat_avail.append(seat_status)
                            elif seat_status == 1 : seat_unavail.append(seat_status)
                            elif seat_status == 3 : 
                                seat_unavail.append(seat_status)
                                print seat_status,seat_status_
                            elif seat_status == 4 : 
                                seat_unavail.append(seat_status)
                                print seat_status_
                            else :
                                print seat_status
                                seat_unavail.append(seat_status) 
                
        dates_list = data_.get('movie_list','')[0].get('session_dates',[])
        for date in dates_list :
                        today_date = str(datetime.datetime.now().date())
                        if today_date in date : continue
                        count = count + 1
                        if count >= 6 : break
                        movie_link = 'https://apiproxy-moviesv2.paytm.com//v2/movies/search?city=chennai&moviecode=%s&fromdate=%s'%(movie_id,date)
                        yield Request(movie_link,callback=self.parse_availability, meta={'movie_id':movie_id,'ref_url':response.url,'date':date,'count':count},dont_filter=True)

