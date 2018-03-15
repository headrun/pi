import sys
sys.path.append('/root/pi_automation/table_schemas')
from to_udrive import *
from generic_functions import *
from pi_db_operations import *

class Login(object):

    def __init__(self):
        
	self.con, self.cur = get_mysql_connection(DB_HOST,REQ_DB_NAME, '')
        self.select_qry = "select * from facebook_profiles where sk='7658d1d09d5458c9fe6243e2994e9c9a'"
        self.insert_qry = "insert into pi_automation(sk,Fb_name,Fb_profile_id,Fb_aux_info,Fb_aux_info_read_followers,Fb_aux_info_books_likes,Fb_aux_info_read_books,Fb_aux_info_movie_watched,Fb_aux_info_movie_likes,Fb_aux_info_tvshow_watched,Fb_aux_info_tvshow_likes,Fb_aux_info_inspirational_people,Fb_aux_info_sports,Fb_aux_info_family,Fb_aux_info_education,Fb_aux_info_work,Fb_aux_info_clothing,Fb_aux_info_friends,Fb_aux_info_atheletes,Fb_aux_info_teams,Fb_aux_info_book,Fb_aux_info_music,Fb_aux_info_games,Fb_aux_info_websites,Fb_aux_info_restaurants,Fb_aux_info_activities,Fb_aux_info_interests,Fb_aux_info_tvshows,Fb_aux_info_movies,Fb_aux_info_life_events,Fb_aux_info_quotes,Fb_aux_info_about,Fb_aux_info_lived_places,Fb_aux_info_others,Fb_profile_url)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update sk=%s,Fb_name=%s,Fb_profile_id=%s,Fb_aux_info=%s,Fb_aux_info_read_followers=%s,Fb_aux_info_books_likes=%s,Fb_aux_info_read_books=%s,Fb_aux_info_movie_watched=%s,Fb_aux_info_movie_likes=%s,Fb_aux_info_tvshow_watched=%s,Fb_aux_info_tvshow_likes=%s,Fb_aux_info_inspirational_people=%s,Fb_aux_info_sports=%s,Fb_aux_info_family=%s,Fb_aux_info_education=%s,Fb_aux_info_work=%s,Fb_aux_info_clothing=%s,Fb_aux_info_friends=%s,Fb_aux_info_atheletes=%s,Fb_aux_info_teams=%s,Fb_aux_info_book=%s,Fb_aux_info_music=%s,Fb_aux_info_games=%s,Fb_aux_info_websites=%s,Fb_aux_info_restaurants=%s,Fb_aux_info_activities=%s,Fb_aux_info_interests=%s,Fb_aux_info_tvshows=%s,Fb_aux_info_movies=%s,Fb_aux_info_life_events=%s,Fb_aux_info_quotes=%s,Fb_aux_info_about=%s,Fb_aux_info_lived_places=%s,Fb_aux_info_others=%s,Fb_profile_url=%s"
	
    def __del__(self):
	close_mysql_connection(self.con, self.cur)

    def main(self):
        self.cur.execute(self.select_qry)
        data = self.cur.fetchall()
        for row in data :
            sk,Fb_name,Fb_profile_id,Fb_aux_info,Fb_aux_info_read_followers,Fb_aux_info_books_likes,Fb_aux_info_read_books,Fb_aux_info_movie_watched,Fb_aux_info_movie_likes,Fb_aux_info_tvshow_watched,Fb_aux_info_tvshow_likes,Fb_aux_info_inspirational_people,Fb_aux_info_sports,Fb_aux_info_family,Fb_aux_info_education,Fb_aux_info_work,Fb_aux_info_clothing,Fb_aux_info_friends,Fb_aux_info_atheletes,Fb_aux_info_teams,Fb_aux_info_book,Fb_aux_info_music,Fb_aux_info_games,Fb_aux_info_websites,Fb_aux_info_restaurants,Fb_aux_info_activities,Fb_aux_info_interests,Fb_aux_info_tvshows,Fb_aux_info_movies,Fb_aux_info_life_events,Fb_aux_info_quotes,Fb_aux_info_about,Fb_aux_info_lived_places,Fb_aux_info_others,Fb_profile_url,created_at,modified_at = row
            values = [sk,Fb_name,Fb_profile_id,Fb_aux_info,Fb_aux_info_read_followers,Fb_aux_info_books_likes,Fb_aux_info_read_books,Fb_aux_info_movie_watched,Fb_aux_info_movie_likes,Fb_aux_info_tvshow_watched,Fb_aux_info_tvshow_likes,Fb_aux_info_inspirational_people,Fb_aux_info_sports,Fb_aux_info_family,Fb_aux_info_education,Fb_aux_info_work,Fb_aux_info_clothing,Fb_aux_info_friends,Fb_aux_info_atheletes,Fb_aux_info_teams,Fb_aux_info_book,Fb_aux_info_music,Fb_aux_info_games,Fb_aux_info_websites,Fb_aux_info_restaurants,Fb_aux_info_activities,Fb_aux_info_interests,Fb_aux_info_tvshows,Fb_aux_info_movies,Fb_aux_info_life_events,Fb_aux_info_quotes,Fb_aux_info_about,Fb_aux_info_lived_places,Fb_aux_info_others,Fb_profile_url]
            values = values + values
            import pdb;pdb.set_trace()
            self.cur.execute(self.insert_qry,values)
            self.con.commit()
            

if __name__ == '__main__':
    Login().main()

