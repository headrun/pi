import csv
import datetime
import datetime
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import MySQLdb
from datetime import timedelta

class  ExcelGenIOC():
    
    def __init__(self):

        self.conn = MySQLdb.connect(db = 'paytm_movie', user='root', host = 'localhost', passwd='', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.header_params = ['movie_code','Movie_title','image_url','censor','genre','content','duration','trailor_url','language','opening_date','reference_url']
        self.header_params1 = ['session_id','Movie_code','theater_name','provider_name','address','latitude','longitude','multiple_ticket','audi','real_show_time','free_seating','token_fee_only','token_fee_pickup_time','grouped_seats','max_tickets','seats_avail','seats_total','ticket_type','ticket_price','reference_url'] 
        self.query = 'select Movie_code,Movie_title,image_url,censor,genres,content,duration,trailor_url,language,opening_date,reference_url from Movie'
        self.meta_query = 'insert into Movie_sessions(session_id,Movie_code,theater_name,provider_name,address,latitude,longitude,multiple_ticket,audi,real_show_time,free_seating,token_fee_only,token_fee_pickup_time,grouped_seats,max_tickets,seats_avail,seats_total,ticket_type,ticket_price,aux_info,reference_url,created_at,modified_at)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()'
        #self.excel_file_name1 = 'paytm_session_data_ON_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name = 'paytm_movie_data_ON_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        #oupf1 = open(self.excel_file_name1, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        #self.todays_excel_file1  = csv.writer(oupf1)
        #self.todays_excel_file1.writerow(self.header_params1)
        self.todays_excel_file.writerow(self.header_params)
        self.main()

    def main(self):
        self.cur.execute(self.query)       
        data = self.cur.fetchall()
        for row in data :
            movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url = row
            vals = [movie_id,movie_title,image_url,censor,genre,content,duration,trailor_url,language,opening_date,reference_url]
            self.todays_excel_file.writerow(vals)
                       
if __name__ == '__main__':
    OBJ = ExcelGenIOC()
     
