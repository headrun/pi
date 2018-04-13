from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *

class Login(object):

    def __init__(self, *args, **kwargs):
	self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.select_qry = "select * from Twitter_latest where sk = '%s'"
        self.insert_qry = "insert into pi_automation(sk,s_no,Twt_screen_name,Twt_profile_name,Twt_description,Twt_location,Twt_no_of_tweets,Twt_no_following,Twt_no_of_followers,Twt_no_of_likes,Twt_image,Twt_lists,Twt_timezone,Twt_language,Twt_is_verified,Twt_twitter_url,Twt_email_id,Twt_aux_info,Twt_top_10_hashtags,Twt_top_5_mentioned_users,Twt_retweeted_percentage,Twt_retweeted_users,Twt_Most_referenced_domains,Twt_detected_sources,Twt_detected_languages,Twt_Avg_no_of_tweets_per_day)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE sk=%s,s_no=%s,Twt_screen_name=%s,Twt_profile_name=%s,Twt_description=%s,Twt_location=%s,Twt_no_of_tweets=%s,Twt_no_following=%s,Twt_no_of_followers=%s,Twt_no_of_likes=%s,Twt_image=%s,Twt_lists=%s,Twt_timezone=%s,Twt_language=%s,Twt_is_verified=%s,Twt_twitter_url=%s,Twt_email_id=%s,Twt_aux_info=%s,Twt_top_10_hashtags=%s,Twt_top_5_mentioned_users=%s,Twt_retweeted_percentage=%s,Twt_retweeted_users=%s,Twt_Most_referenced_domains=%s,Twt_detected_sources=%s,Twt_detected_languages=%s,Twt_Avg_no_of_tweets_per_day=%s"
        self.main()
	
    def __del__(self):
	close_mysql_connection(self.con, self.cur)

    def main(self):
        self.cur.execute(self.select_qry % options.sk)
        data = self.cur.fetchall()

        for row in data :
            sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at = row

            s_no = options.k
            values = [sk,s_no,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day]
            values = values  + values
            self.cur.execute(self.insert_qry,values)
            self.con.commit()
            

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-s','--sk',default='', help='sk')
    parser.add_option('-k','--k',default='',help='sno')
    (options, args) = parser.parse_args()
    Login(options)

