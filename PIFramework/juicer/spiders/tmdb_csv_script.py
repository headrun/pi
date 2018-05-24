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
import re

class ExcelGenIOC():

    def __init__(self):

        self.header_params = ['movie_id','title','popularity','poster_path','genres_name','vote_average','imdb_id','languages','collection_name','collection_id','coll_poster_path','coll_backdrop_path','production_country','budget','homepage','overview','production_company_name','production_country','production_company_logo','tagline','release_date','adult','spoken_languages','vote_count','runtime','revenue', 'cast_count', 'crew_count', 'reference_url']
        self.header_params1 =  ['Crew_id','movie_id','movie_title','credit_id','name','gender','aka','place_of_birth','death_day','biography','crew_job','cast_character','cast_order', 'Department', 'profile_path','popularity','Adult','Imdb_id','Homepage','reference_url']
        #self.excel_file_name1 = 'TMDB_CREW_latest_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name = 'TMDB_MOVIEON_all_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        #oupf1 = open(self.excel_file_name1, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        #self.todays_excel_file1  = csv.writer(oupf1)
        #self.todays_excel_file1.writerow(self.header_params1)
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
                    """query2 = 'select rank, role, role_title, program_sk from ProgramCrew where program_sk=%s'%movie_id
                    import json
                    self.cur.execute(query2)
                    data = self.cur.fetchall()
                    for _row in data:
                        crew_sk, role, meta_data, movie_id = _row
                        try : meta = json.loads(meta_data)
                        except : 
                            print meta_data
                            continue
                        cast_id = meta.get('cast_id','')
                        cast_character = meta.get('character','')
                        cast_order = meta.get('order','')
                        crew_job = meta.get('job','')
                        department = meta.get('department','')
                        crew_qry = 'select sk,credit_id,name,gender,aka,birth_place,death_date,biography,profile_path,popularity,adult,imdb_id,homepage,reference_url from Crew where sk = %s' %crew_sk
                        self.cur.execute(crew_qry)
                        try :crew_data = self.cur.fetchall()[0]
                        except :continue
                        crew_data = list(crew_data)
                       
                        sk,credit_id,name,gender,aka,place_of_birth,death_day,biography,profile_path,popularity,adult,imdb_id,homepage,reference_url = crew_data
                        try : vals = [sk,movie_id,self.normalize(title),credit_id,self.normalize(name),gender,self.normalize(aka),place_of_birth.encode('utf-8'),death_day,biography.encode('utf-8'),crew_job.encode('utf-8'),self.normalize(cast_character),cast_order, department.encode('utf-8'), profile_path,popularity,adult,imdb_id,homepage,reference_url]
                        except :
                             print movie_id,'*****',sk
                             continue
                        if sk :
                            try : self.todays_excel_file1.writerow(vals)
                            except : 
                                print movie_id,'*****',sk
                                continue"""


                        
                          
    def normalize(self,text):
        return self.clean(self.compact(self.xcode(text)))

    def xcode(self,text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode) if isinstance(text, unicode) else text

    def compact(self,text, level=0):
        if text is None: return ''
        if level == 0:
            text = text.replace("\r", " ")
        compacted = re.sub("\s\s(?m)", " ", text)
        if compacted != text:
            compacted = compact(compacted, level+1)

        return compacted.strip()

    def clean(self,text):
        if not text: return text

        value = text
        value = re.sub("&amp;", "&", value)
        value = re.sub("&lt;", "<", value)
        value = re.sub("&gt;", ">", value)
        value = re.sub("&quot;", '"', value)
        value = re.sub("&apos;", "'", value)

        return value



    def un(self,text):
        text = text.replace('\t','').replace('\r','').strip()
        return text        

    def main(self):
        self.get_mysql_conn()
        self.excel_generation()


if __name__ == '__main__':
    OBJ = ExcelGenIOC()
    OBJ.main()


