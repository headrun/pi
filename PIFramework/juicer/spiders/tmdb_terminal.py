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
    name = 'tmdb_movie_terminal'
    #name = 'tmdb_movie_crawler'
    #start_urls = ['https://api.themoviedb.org/3/movie/314726?api_key=ddbd4a97b535574e0c4a405cee1be8d4&append_to_response=credits']
    
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
        result = json.loads(response.body)
        vote_count = result.get('vote_count','')
        movie_id = result.get('id','')
        vote_average = result.get('vote_average','')
        title = result.get('title','')
        popularity = result.get('popularity','')
        poster_path = result.get('poster_path','')
        if poster_path : poster_path =  "https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + str(poster_path)    
        lang = result.get('original_language','')
        org_title = result.get('original_title','')
        genre_id = ''
        genres = result.get('genres',[])
        genres_id = []
        gen_id = [genre_id.get('id','') for genre_id in genres]
        for genr_id in gen_id :
            gen_id = str(genr_id)
            genres_id.append(gen_id)
        if genre_id :  genre_id = "<>".join(genres_id)
        else : genre_id = ''
        gen_name = '<>'.join([genre_name.get('name','') for genre_name in genres])        
        imdb_id = result.get('imdb_id','')
        collection = result.get('belongs_to_collection',{})
        try : 
            collection_id = collection.get('id','')
            colle_name = collection.get('name','')
            coll_poster_path = collection.get('poster_path','')
            coll_backdrop_path = collection.get('backdrop_path','')
        except : 
            collection_id,colle_name,coll_poster_path,coll_backdrop_path = '','','',''

        budget = result.get('budget','')
        homepage = result.get('homepage','')
        original_language = result.get('original_language','')
        overview = result.get('overview','')
        pro_com = result.get('production_companies','')
        pro_coun = result.get('production_countries','')
        pro_com_name = '<>'.join([pro_com_name.get('name','') for pro_com_name in pro_com]) 
        country = "<>".join([country.get('origin_country','') for country in pro_com if country.get('origin_country')])
        pro_country = "<>".join([p_country.get('name','') for p_country in pro_coun if p_country.get('name')])
        pro_com_logo = []
        for path in pro_com :
            logo_path = path.get('logo_path','')
            if logo_path : logo_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + str(logo_path)
            pro_com_logo.append(logo_path)
        try :  pro_com_logo = "<>".join(pro_com_logo)
        except : pro_com_logo = ''
        release_date = result.get('release_date','')
        revenue = result.get('revenue','')
        runtime = result.get('runtime','')
        spoken_languages = result.get('spoken_languages','')
        if spoken_languages!=None : spoken_languages = '<>'.join([spoken_lang.get('name','') for spoken_lang in spoken_languages])
        else : spoken_languages = ''

        status = result.get('status','')
        tagline = result.get('tagline','')
        overview = result.get('overview','')
        release_date = result.get('release_date','')
        adult = result.get('adult','')
        ref_url = "https://www.themoviedb.org/movie/"+str(movie_id)+'-'+title.lower().replace(' ','-')
        movie_item = MovieItem()
        movie_item['sk'] = str(movie_id)
        movie_item['title'] = normalize(org_title)
        movie_item['popularity'] = str(popularity)
        movie_item['poster_path'] = normalize(poster_path)
        movie_item['genres_id'] = str(genres_id)
        movie_item['genres_name'] = normalize(gen_name)
        movie_item['vote_average'] = str(vote_average)
        movie_item['imdb_id'] = str(imdb_id)
        movie_item['languages'] = normalize(lang)
        movie_item['collection_name'] = normalize(colle_name)
        movie_item['collection_id'] = str(collection_id)
        movie_item['coll_poster_path'] = str(coll_poster_path)
        movie_item['coll_backdrop_path'] = str(coll_backdrop_path)
        movie_item['aux_info'] = str(pro_country)
        movie_item['budget'] = str(budget)
        movie_item['homepage'] = normalize(homepage)
        movie_item['overview'] = normalize(overview)
        movie_item['production_com_name'] = normalize(pro_com_name)
        movie_item['production_country']= normalize(country)
        movie_item['production_company_logo'] = normalize(pro_com_logo)
        movie_item['tagline'] = normalize(tagline)
        movie_item['release_date'] = str(release_date)
        movie_item['adult'] = str(adult)
        movie_item['spoken_languages'] = normalize(spoken_languages)
        movie_item['vote_count'] = str(vote_count)
        movie_item['runtime'] = str(runtime)
        movie_item['revenue'] = str(revenue)
        movie_item['reference_url'] = normalize(ref_url)
        #yield movie_item
        #self.todays_excel_file.writerow(values)
        credits = result.get('credits',{})
        cast_crew_list = []
        casts = credits.get('cast',[])
        cast_count = len(casts)
        movie_item['cast_count'] = str(cast_count)
        cast_rank = 0
        for cast in casts :
            cast_id = cast.get('cast_id','')
            character = cast.get('character','')
            credit_id = cast.get('credit_id','')
            gender = cast.get('gender','')
            id_ = cast.get('id','')
            name = cast.get('name','')
            order = cast.get('order','')
            role_data = ({'cast_id':cast_id,'character':character,'order':order})
            profile_path = cast.get('profile_path','')
            if id_ : 
                rank = cast_rank + 1
                program_crew = ProgramCrewItem()
                program_crew['program_sk'] = str(movie_id)
                program_crew['program_type'] = 'Movie'
                program_crew['crew_sk'] = str(credit_id)
                program_crew['role'] = normalize(character)
                program_crew['role_title']= json.dumps(role_data)
                program_crew['rank'] = str(id_)
                program_crew['aux_info'] = str(id_)
                yield program_crew
                #cast_link = "https://api.themoviedb.org/3/person/%s?api_key=ddbd4a97b535574e0c4a405cee1be8d4"%id_
                #self.get_page("tmdb_crew_terminal", cast_link, id_, meta_data={'movie_id':movie_id,'movie_title':org_title,"type":'cast','cast_character':character,'cast_order':order,'ref_url':response.url,'credit_id':credit_id})
        crews = credits.get('crew',[])
        movie_item['crew_count'] = str(len(crews))
        #yield movie_item
        #import pdb;pdb.set_trace()
        self.got_page(movie_id, 1)
        department,gender,job,name,id_='','','','',''
        crew_rank = 0
        for crew in crews :
            credit_id = crew.get('credit_id','')
            department = crew.get('department','')
            gender = crew.get('gender','')
            id_ = crew.get('id','')
            job = crew.get('job','')
            name = crew.get('name','')
            profile_path = crew.get('profile_path','')
            role_data = ({'department':department,'job':job})
            if id_ :
                rank = crew_rank + 1
                program_crew = ProgramCrewItem()
                program_crew['program_sk'] = str(movie_id)
                program_crew['program_type'] = 'Movie'
                program_crew['crew_sk'] = str(credit_id)
                program_crew['role'] = normalize(job)
                program_crew['role_title'] = json.dumps(role_data)
                program_crew['rank'] = str(id_)
                program_crew['aux_info'] = str(id_)
                yield program_crew
                #crew_link = "https://api.themoviedb.org/3/person/%s?api_key=ddbd4a97b535574e0c4a405cee1be8d4"%id_
                #self.get_page("tmdb_crew_terminal", crew_link, id_, meta_data={'movie_id':movie_id,'movie_title':org_title,'department':department,'credit_id':credit_id,"type":crew,'job':job,'ref_url':response.url,'credit_id':credit_id})
       
      


                
