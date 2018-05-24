import scrapy
import hashlib
import csv
import datetime
from scrapy.selector import Selector
import datetime
from juicer.utils import *

from juicer.items import *


class Baby(JuicerSpider):
    name = 'tmdb_browse'
    start_urls = []
    with open('20180402_movie_list_2014-2017.txt', 'r') as f: rows = f.readlines()
    for row in rows:
        i = row.replace('\r\n','')
        link = "https://api.themoviedb.org/3/search/movie?api_key=ddbd4a97b535574e0c4a405cee1be8d4&query=%s"%i
        #link = "https://api.themoviedb.org/3/search/movie?api_key=ddbd4a97b535574e0c4a405cee1be8d4&query=VELLACHI"
        start_urls.append(link)

    
    def __init__(self, *args, **kwargs):
        super(Baby, self).__init__(*args, **kwargs)
       
 
    def parse(self, response):
        sel = Selector(response)
        data = json.loads(response.body)
        results = data.get('results',[])
        counter = 1
        for result in results :
            vote_count = result.get('vote_count','')
            id_ = result.get('id','')
            vote_average = result.get('vote_average','')
            title = result.get('title','')
            popularity = result.get('popularity','')
            poster_path = result.get('poster_path','')
            lang = result.get('original_language','')
            org_title = result.get('original_title','')
            genre_id = result.get('genre_ids','')
            overview = result.get('overview','')
            release_date = result.get('release_date','')
            adult = result.get('adult','')
            if id_ :
        	credits_link = "https://api.themoviedb.org/3/movie/%s?api_key=ddbd4a97b535574e0c4a405cee1be8d4&append_to_response=credits"%id_
        	self.get_page('tmdb_movie_terminal', credits_link, id_, meta_data={'movie_id':id_,'movie_title':title,'reference_url':response.url})

    def parse_cast(self,response):
        sel = Selector(response)
        result = json.loads(response.body)
        vote_count = result.get('vote_count','')
        id_ = result.get('id','')
        vote_average = result.get('vote_average','')
        title = result.get('title','')
        popularity = result.get('popularity','')
        poster_path = result.get('poster_path','')
        lang = result.get('original_language','')
        org_title = result.get('original_title','')
        genres = result.get('genres',[])
        genre_id = []
        gen_id = [genre_id.get('id','') for genre_id in genres]
        for genr_id in gen_id :
            gen_id = str(genr_id)
            genre_id.append(gen_id)
        genre_id = "<>".join(genre_id)
        gen_name = '<>'.join([genre_name.get('name','') for genre_name in genres])        
        imdb_id = result.get('imdb_id','')
        collection = result.get('belongs_to_collection',{})
        collection_id = collection.get('id','')
        colle_name = collection.get('name','')
        coll_poster_path = collection.get('poster_path','')
        coll_backdrop_path = collection.get('backdrop_path','')
        budget = result.get('budget','')
        homepage = result.get('homepage','')
        original_language = result.get('original_language','')
        overview = result.get('overview','')
        pro_com = result.get('production_companies','')
        pro_com_name = '<>'.join([pro_com_name.get('name','') for pro_com_name in pro_com]) 
        country = '<>'.join([country.get('origin_country','') for country in pro_com]) 
        pro_com_logo = []
        for path in pro_com :
            logo_path = path.get('logo_path','')
      
        
             
            
        overview = result.get('overview','')
        release_date = result.get('release_date','')
        adult = result.get('adult','')

        import pdb;pdb.set_trace()
        credits = data.get('credits',{})
        casts = credits.get('cast',[])
        for cast in casts :
            cast_id = cast.get('cast_id','')
            character = cast.get('character','')
            credit_id = cast.get('credit_id','')
            gender = cast.get('gender','')
            id_ = cast.get('id','')
            name = cast.get('name','')
            order = cast.get('order','')
            profile_path = cast.get('profile_path','')
            if id_ : 
                cast_link = "https://api.themoviedb.org/3/person/%s?api_key=ddbd4a97b535574e0c4a405cee1be8d4"%id_
                yield Request(credits_link,callback=self.parse_castmeta,meta={'movie_id':response.meta.get('movie_id'),'movie_title':response.meta.get('movie_title','')})

    def parse_castmeta(self,response):
        sel = Selector(response)
        data = json.loads(response.body)
        bday = data.get('birthday','')
        death_day = data.get('deathday','')
        id_ = data.get('id','')
        name = data.get('name','')
        aka = data.get('also_known_as','')
        gender = data.get('gender','')
        biography = data.get('biography','')
        popularity = data.get('popularity','')
        place_of_birth = data.get('place_of_birth','')
        profile_path = data.get('profile_path','')
        adult = data.get('adult','')
        imdb_id = data.get('imdb_id','')
        homepage = data.get('homepage','')
        movie_id = response.meta.get('movie_id','')
        movie_title = response.meta.get('movie_title','')

             


            
       
   
            
        #values = [str(time_stamp), conta_num, siz_type, Location, status, date_time, mode]
        #self.todays_excel_file.writerow(values)


                
