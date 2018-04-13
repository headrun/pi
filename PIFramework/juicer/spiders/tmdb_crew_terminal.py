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


class BabyTerminal(JuicerSpider):
    name = 'tmdb_crew_terminal'
    
    def __init__(self, *args, **kwargs):
        super(BabyTerminal, self).__init__(*args, **kwargs)
        self.header_params = ['movie_id','title','original_title','popularity','poster_path','genres_id','genres_name','vote_average','imdb_id','languages','collection_name','collection_id','coll_poster_path','coll_backdrop_path','production_country','budget','homepage','overview','production_com_name','production_country','production_company_logo','tagline','release_date','adult','spoken_languages','vote_count','runtime','revenue','reference_url']
        self.header_params1 =  ['Crew_id','movie_id','movie_title','credit_id','name','gender','aka','place_of_birth','death_day','biography','crew_job','cast_character','cast_order','profile_path','popularity','Adult','Imdb_id','Homepage','reference_url']
        self.excel_file_name1 = 'TMDB_CREW_DATA_ON_%s.csv'%str(datetime.datetime.now().date())
        self.excel_file_name = 'TMDB_MOVIE_DATA_ON_%s.csv'%str(datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        oupf1 = open(self.excel_file_name1, 'ab+')
        self.todays_excel_file  = csv.writer(oupf)
        self.todays_excel_file1  = csv.writer(oupf1)
        self.todays_excel_file1.writerow(self.header_params1)
        self.todays_excel_file.writerow(self.header_params)
               
    def parse(self,response):
        sel = Selector(response)
        data = json.loads(response.body)
        department = response.meta.get('data',{}).get('department','')
        bday = data.get('birthday','')
        crew_job = response.meta.get('data',{}).get('job','')
        credit_id = response.meta.get('data',{}).get('credit_id','')
        cast_character = response.meta.get('data',{}).get('cast_character','')
        cast_order = response.meta.get('data',{}).get('cast_order','')
        death_day = data.get('deathday','')
        id_ = data.get('id','')
        name = data.get('name','')
        aka = data.get('also_known_as','')
        if aka : aka = "<>".join(aka)
        else :  aka = ''
        gender = data.get('gender','')
        biography = data.get('biography','')
        popularity = data.get('popularity','')
        place_of_birth = data.get('place_of_birth','')
        profile_path = data.get('profile_path','')
        if profile_path : profile_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + profile_path
        adult = data.get('adult','')
        imdb_id = data.get('imdb_id','')
        homepage = data.get('homepage','')
        movie_id = response.meta.get('data',{}).get('movie_id','')
        movie_title = response.meta.get('data',{}).get('movie_title','')
        ref_url = "https://www.themoviedb.org/person/"+str(id_)+'-'+name.lower().replace(' ','-')
        crew_item = CrewItem()
        crew_item['sk'] = str(id_)
        crew_item['movie_id'] = str(movie_id)
        crew_item['movie_title'] = normalize(movie_title)
        crew_item['credit_id']  = str(credit_id)
        crew_item['name'] = normalize(name)    
        crew_item['gender'] = str(gender)
        crew_item['age'] = ''
        crew_item['aka'] = str(aka)
        crew_item['birth_place'] = normalize(place_of_birth)
        crew_item['death_date'] = str(death_day)
        crew_item['death_place'] = ''
        crew_item['country'] = ''
        crew_item['biography'] = normalize(biography)
        crew_item['crew_job'] = normalize(crew_job)
        crew_item['cast_character'] = normalize(department)
        crew_item['cast_order'] = str(cast_order)
        crew_item['profile_path']= normalize(profile_path)
        crew_item['popularity'] = str(popularity)
        crew_item['adult'] =str(adult)
        crew_item['imdb_id']= str(imdb_id)
        crew_item['homepage']=str(homepage)
        crew_item['reference_url']= normalize(ref_url) 
        yield crew_item
        self.got_page(id_, 1)
        
        #values = [str(id_),str(movie_id),str(department),normalize(movie_title),str(credit_id),normalize(name),str(gender),str(aka),str(place_of_birth),str(death_day),str(biography),str(crew_job),str(cast_character),str(cast_order),str(profile_path),str(popularity),str(adult),str(imdb_id),str(homepage),ref_url.encode('utf-8')]
        
        #self.todays_excel_file1.writerow(values)


                
