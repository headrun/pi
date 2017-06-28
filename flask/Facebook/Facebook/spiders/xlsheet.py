import xlwt
import MySQLdb
import json
from fb_browse_queries import *
import datetime

class xlsfile(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
	self.cur = self.con.cursor()
        self.row_count = 1
        self.excel_file_name = 'Ash_enrichment_facebook.xlsx'
	#self.excel_file_name = 'fullcontact_facebook.xlsx'
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)

    def restore(self, text):
        text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
        if '<>' in text:
            text = set(text.split('<>'))
            text = '<>'.join(text)
        return text

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def send_xls(self):
        self.cur.execute(selectall_params)
        records = self.cur.fetchall()
        print len(records)
        for record in records:
            sk1 , name1, profile_id1, aux_info1, aux_info_read_followers,aux_info_books_likes,aux_info_read_books,aux_info_movie_watched,aux_info_movie_likes,aux_info_tvshow_watched, aux_info_tvshow_likes, aux_info_inspirational_people, aux_info_sports, aux_info_family, aux_info_education, aux_info_work, aux_info_clothing, aux_info_friends, aux_info_atheletes, aux_info_teams, aux_info_book, aux_info_music, aux_info_games, aux_info_websites, aux_info_restaurants, aux_info_activities, aux_info_interests, aux_info_tvshows, aux_info_movies, aux_info_others, profile_url1 = record

            #import pdb;pdb.set_trace()
	    try: self.cur.execute(update_getc_params%('updatedrecord',sk1))
	    except: pass
            if 'Facebook' in name1: 
                name1=''
                import pdb;pdb.set_trace()
            if 'Add Mobile Number' in name1: 
                name1=''
                import pdb;pdb.set_trace()
            
            aux_infof = json.loads(aux_info1.replace('\\','').replace('\r\n',''))
            aux_info_read_followers = json.loads(aux_info_read_followers.replace('\\',''))
            aux_info_books_likes = json.loads(aux_info_books_likes.replace('\\',''))
            aux_info_read_books = json.loads(aux_info_read_books.replace('\\',''))
            aux_info_movie_watched = json.loads(aux_info_movie_watched.replace('\\',''))
            aux_info_movie_likes = json.loads(aux_info_movie_likes.replace('\\',''))
            aux_info_tvshow_watched = json.loads(aux_info_tvshow_watched.replace('\\',''))
            aux_info_tvshow_likes = json.loads(aux_info_tvshow_likes.replace('\\',''))
            aux_info_inspirational_people = json.loads(aux_info_inspirational_people.replace('\\',''))
            aux_info_sports = json.loads(aux_info_sports.replace('\\',''))
            aux_info_family = json.loads(aux_info_family.replace('\\',''))
            aux_info_education = json.loads(aux_info_education.replace('\\',''))
            aux_info_work = json.loads(aux_info_work.replace('\\',''))
	    try:
		aux_info_clothing = json.loads(aux_info_clothing.replace('\\',''))
	    except:
		aux_info_clothing = {"fb_clothing":'<>'.join(aux_info_friends.replace(' "',"").replace('{"fb_clothing":','').split('<>'))}

            try:aux_info_friends = json.loads(aux_info_friends.replace('\\',''))
            except:
                aux_info_friends = {"fb_friends":'<>'.join(aux_info_friends.replace(' "',"").replace('{"fb_friends":','').split('<>'))}
            aux_info_atheletes = json.loads(aux_info_atheletes.replace('\\',''))
            aux_info_teams = json.loads(aux_info_teams.replace('\\',''))
            aux_info_book = json.loads(aux_info_book.replace('\\',''))
            aux_info_music = json.loads(aux_info_music.replace('\\',''))
            aux_info_games = json.loads(aux_info_games.replace('\\',''))
            aux_info_websites = json.loads(aux_info_websites.replace('\\',''))
            aux_info_restaurants = json.loads(aux_info_restaurants.replace('\\',''))
            aux_info_activities = json.loads(aux_info_activities.replace('\\',''))
            aux_info_interests = json.loads(aux_info_interests.replace('\\',''))
            aux_info_tvshows = json.loads(aux_info_tvshows.replace('\\',''))
            aux_info_movies = json.loads(aux_info_movies.replace('\\',''))
            try: aux_info_others = json.loads(aux_info_others.replace('\\',''))
            except:
                aux_info_others = {"fb_others":'<>'.join(aux_info_others.replace(' "',"").replace('{"fb_others":','').split('<>'))} 
            response_flag = ''
            if name1:
                response_flag = 'Response Available'
            if not name1: response_flag = 'Response Not Available'
            values = [self.restore(name1), profile_id1, profile_url1, profile_url1.replace('mbasic','www'),self.restore(aux_infof.get('current_city','')), self.restore(aux_infof.get('home_town','')),self.restore(aux_infof.get('birthday','')),self.restore(aux_infof.get('gender','')),self.restore(aux_infof.get('professional_skills','')),self.restore(aux_infof.get('no_of_friends','')),self.restore(aux_infof.get('mobile','')), self.restore(aux_infof.get('instagram','')),self.restore(aux_infof.get('websites','')),self.restore(aux_infof.get('interested_in','')),self.restore(aux_infof.get('languages','')),self.restore(aux_infof.get('religious_views','')),self.restore(aux_infof.get('political_views','')),self.restore(aux_infof.get('relationship','')),self.restore(aux_infof.get('address','')),self.restore(aux_infof.get('google_talk','')),self.restore(aux_infof.get('email','')),self.restore(aux_infof.get('other_names','')),self.restore(aux_infof.get('nick_name','')),self.restore(aux_infof.get('messenger','')),self.restore(aux_infof.get('home_phone','')),self.restore(aux_infof.get('facebook','')),self.restore(aux_info_others.get('fb_others','')),self.restore(aux_info_clothing.get('fb_clothing','')),self.restore(aux_info_activities.get('fb_activities','')),self.restore(aux_info_interests.get('fb_interests','')),self.restore(aux_info_music.get('fb_music','')),self.restore(aux_info_book.get('fb_books','')),self.restore(aux_info_movies.get('fb_movies','')),self.restore(aux_info_tvshows.get('fb_tvshows','')),self.restore(aux_info_atheletes.get('fb_favaourite_athelets','')),self.restore(aux_info_teams.get('fb_favourite_teams','')),self.restore(aux_info_games.get('fb_games','')),self.restore(aux_info_restaurants.get('fb_restaurants','')),self.restore(aux_info_websites.get('fb_websites','')),self.restore(aux_info_work.get('fb_works','')),self.restore(aux_info_education.get('fb_education','')),self.restore(aux_info_sports.get('fb_favourite_sports','')),self.restore(aux_info_friends.get('fb_friends','')),self.restore(aux_info_inspirational_people.get('fb_inspirational_people','')),self.restore(aux_info_tvshow_likes.get('fb_tvshow_likes','')),self.restore(aux_info_tvshow_watched.get('fb_tvshows_watched','')),self.restore(aux_info_movie_likes.get('fb_movies_likes','')),self.restore(aux_info_movie_watched.get('fb_movies_watched','')),self.restore(aux_info_books_likes.get('fb_book_likes','')),self.restore(aux_info_read_books.get('fb_read_books','')),self.restore(aux_info_read_followers.get('fb_following','')),self.restore(aux_info_family.get('fb_family','')),response_flag, self.restore(aux_infof.get('email_address',''))]
	    if 'Response Not Available' in response_flag:
		self.cur.execute('select meta_data from facebook_crawl where sk = "%s"'%sk1)
		records_email = self.cur.fetchall()
		values [-1] = json.loads(records_email[0][0]).get('email_address','')
		#print values
            for col_count, value in enumerate(values):
                if len(value) > 32767: 
                    continue
                self.todays_excel_sheet1.write(self.row_count, col_count, value)
            self.row_count = self.row_count+1
	self.todays_excel_file.save(self.excel_file_name)

def main():
        obj = xlsfile()
        obj.send_xls()
if __name__ == '__main__':
        main()


