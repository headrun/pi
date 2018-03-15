"""from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *

class Login(object):

    def __init__(self):
	self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.select_qry = "select * from Twitter_latest limit 1"
        self.insert_qry = "insert into pm_csv1_pi_output(sk,Twt_screen_name,Twt_profile_name,Twt_description,Twt_location,Twt_no_of_tweets,Twt_no_following,Twt_no_of_followers,Twt_no_of_likes,Twt_image,Twt_lists,Twt_timezone,Twt_language,Twt_is_verified,Twt_twitter_url,Twt_email_id,Twt_aux_info,Twt_top_10_hashtags,Twt_top_5_mentioned_users,Twt_retweeted_percentage,Twt_retweeted_users,Twt_Most_referenced_domains,Twt_detected_sources,Twt_detected_languages,Twt_Avg_no_of_tweets_per_day)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	
    def __del__(self):
	close_mysql_connection(self.con, self.cur)

    def main(self):
        self.cur.execute(self.select_qry)
        data = self.cur.fetchall()
        for row in data :
            sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at = row
            values = [sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day]
            import pdb;pdb.set_trace()
            self.cur.execute(self.insert_qry,values)
            self.con.commit()
            

if __name__ == '__main__':
    Login().main()"""

