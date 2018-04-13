import pymysql

#db details

"""db_user   = 'root'
db_passwd = 'hdrn59!'
db_host   = 'localhost'
db_name   = 'TWITTER'"""

db_user   = 'root'
db_passwd = 'root'
db_host   = '176.9.181.34'
db_name = 'FACEBOOK'
#Access and Consumer Tokens
#Aruna
access_token="2826154500-Kt43ZckLttYHvip2wlvhTTyK6AScEsSxEpxHzPG"
access_token_secret="UoDlnNmGlTM2HH2Vw2dFF18K5oYAUVxulmAqMs4UfUMb4"
consumer_key="KUFycnEBUXtEzem3Pk3omGdZJ"
consumer_secret="8wW82SXdRi6aWpgKV7fjTPYrvFxoRQencwWng1y3oeli2ZljFD"


con = pymysql.connect(db=db_name,
user=db_user,
password=db_passwd,
charset="utf8mb4",
host=db_host)

cur = con.cursor()

#query operations

#qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now()'

twitter_qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now(),sk=%s,screen_name=%s,name=%s,description=%s,location=%s,tweets=%s,following=%s,followers=%s,likes=%s,image=%s,lists=%s,timezone=%s,language=%s,is_verified=%s,twitter_url=%s,email_id=%s,aux_info=%s,top_10_hashtags=%s,top_5_mentioned_users=%s,retweeted_percentage=%s,retweeted_users=%s,Most_referenced_domains=%s,detected_sources=%s,detected_languages=%s,Avg_no_of_tweets_per_day=%s'

#twitter_qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now(),sk=%s,screen_name=%s,name=%s,description=%s,location=%s,tweets=%s,following=%s,followers=%s,likes=%s,image=%s,lists=%s,timezone=%s,language=%s,is_verified=%s,twitter_url=%s,email_id=%s,aux_info=%s,top_10_hashtags=%s,top_5_mentioned_users=%s,retweeted_percentage=%s,retweeted_users=%s,Most_referenced_domains=%s,detected_sources=%s,detected_languages=%s,Avg_no_of_tweets_per_day=%s'

insert_query = 'insert into twitter_crawl(sk, url, crawl_type, content_type,related_type,crawl_status,meta_data,created_at,modified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'

update_qry = 'update twitter_crawl set crawl_status=1 where sk="%s" and crawl_status =9 and date(created_at) = curdate()'

select_qry = 'select  sk,url,meta_data from twitter_crawl where date(modified_at)>="2018-04-10" and crawl_status!=100 and crawl_status=0'

upd_qry = 'update twitter_crawl set crawl_status=9 where sk= "%s" and crawl_status=0 and date(created_at)=curdate()'
