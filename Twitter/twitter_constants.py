import MySQLdb

#db details

db_user   = 'root'
db_passwd = 'hdrn59!'
db_host   = 'localhost'
db_name   = 'TWITTER'

#Access and Consumer Tokens
#Aruna
access_token="2826154500-Kt43ZckLttYHvip2wlvhTTyK6AScEsSxEpxHzPG"
access_token_secret="UoDlnNmGlTM2HH2Vw2dFF18K5oYAUVxulmAqMs4UfUMb4"
consumer_key="KUFycnEBUXtEzem3Pk3omGdZJ"
consumer_secret="8wW82SXdRi6aWpgKV7fjTPYrvFxoRQencwWng1y3oeli2ZljFD" 

#db_connection

con = MySQLdb.connect(db=db_name,
                      user=db_user,
                      passwd=db_passwd,
                      charset="utf8",
                      host=db_host,
                      use_unicode=True)
cur = con.cursor()

#query operations

qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now()'

insert_query = 'insert into twitter_crawl(sk, url, crawl_type, content_type,related_type,crawl_status,meta_data,created_at,mod    ified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'

update_qry = 'update twitter_crawl set crawl_status=1 where sk=%s'

select_qry = 'select  sk,url,meta_data from twitter_crawl where crawl_status = 0'

upd_qry = 'update twitter_crawl set crawl_status=9 where sk= "%s"'
