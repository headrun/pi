import os, sys, datetime, subprocess, MySQLdb, codecs, json
import optparse, logging, logging.handlers
import xlwt, csv
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import string
import smtplib

class ExcelGenIOC():

    def __init__(self):

        self.header_params = ['movie_id','title','popularity','poster_path','genres_name','vote_average','imdb_id','languages','collection_name','collection_id','coll_poster_path','coll_backdrop_path','production_country','budget','homepage','overview','production_company_name','production_country','production_company_logo','tagline','release_date','adult','spoken_languages','vote_count','runtime','revenue', 'cast_count', 'crew_count', 'reference_url']
        self.header_params1 =  ['Crew_id','movie_id','movie_title','credit_id','name','gender','aka','place_of_birth','death_day','biography','crew_job','cast_character','cast_order', 'Department', 'profile_path','popularity','Adult','Imdb_id','Homepage','reference_url']
        self.excel_file_name1 = 'TMDB_CREW_DATA_Sheet2_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name = 'TMDB_MOVIE_DATA_ON_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'wb+')
        oupf1 = open(self.excel_file_name1, 'wb+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file1  = csv.writer(oupf1)
        self.todays_excel_file1.writerow(self.header_params1)
        self.todays_excel_file.writerow(self.header_params)
       

    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def get_mysql_conn(self):
        self.conn = MySQLdb.connect(db = 'TMDBOBDB', user='root', host = 'localhost', passwd='root', charset   = "utf8", use_unicode=False)
        self.cur = self.conn.cursor()


    def excel_generation(self):
                query = 'select sk,title,popularity,poster_path,genres_name,vote_average,imdb_id,languages,collection_name,collection_id,coll_poster_path,coll_backdrop_path,aux_info,budget,homepage,overview,production_com_name,production_country,production_company_logo,tagline,release_date,adult,spoken_languages,vote_count,runtime,revenue, cast_count, crew_count, reference_url from Movie'
                self.cur.execute(query)
                rows = self.cur.fetchall()
                for row in rows :
                    movie_id,title,popularity,poster_path,genres_name,vote_average,imdb_id,languages,collection_name,collection_id,coll_poster_path,coll_backdrop_path,production_country,budget,homepage,overview,production_company_name,production_country,production_company_logo,tagline,release_date,adult,spoken_languages,vote_count,runtime,revenue, cast_count, crew_count, reference_url = row
                    values = [ movie_id,title,popularity,poster_path,genres_name,vote_average,imdb_id,languages,collection_name,collection_id,coll_poster_path,coll_backdrop_path,production_country,budget,homepage,overview,production_company_name,production_country,production_company_logo,tagline,release_date,adult,spoken_languages,vote_count,runtime,revenue, cast_count, crew_count, reference_url]
                    self.todays_excel_file.writerow(values)
         
                query2 = 'select rank, role, role_title from ProgramCrew  limit 100000,150000'
                import json
                self.cur.execute(query2)
                data = self.cur.fetchall()
                count = 1
                for _row in data:
                    crew_sk, role, meta_data = _row
                    count = count + 1
                    try : meta = json.loads(meta_data.replace("\\", r"\\"))
                    except : print crew_sk
                    cast_id = meta.get('cast_id','')
                    cast_character = meta.get('character','')
                    cast_order = meta.get('order','')
                    crew_job = meta.get('job','')
                    department = meta.get('department','')
                    crew_qry = 'select sk,movie_id,movie_title,credit_id,name,gender,aka,birth_place,death_date,biography,profile_path,popularity,adult,imdb_id,homepage,reference_url from Crew where sk = %s' %crew_sk
                    self.cur.execute(crew_qry)
                    #import pdb;pdb.set_trace()
                    try :crew_data = self.cur.fetchall()[0]
                    except : print "No_data"
                    crew_data = list(crew_data)
                      
                    sk,movie_id,movie_title,credit_id,name,gender,aka,place_of_birth,death_day,biography,profile_path,popularity,adult,imdb_id,homepage,reference_url = crew_data
                    vals = [sk,movie_id,movie_title,credit_id,name,gender,aka,place_of_birth,death_day,biography,crew_job,cast_character,cast_order, department, profile_path,popularity,adult,imdb_id,homepage,reference_url]
                    if sk :
                        self.todays_excel_file1.writerow(vals)
                        print count


                        
                          
            

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


