con = MySQLdb.connect(db='TWITTER',
                      user='root',
                      passwd='hdrn59!',
                      charset="utf8",
                      host='localhost',
                      use_unicode=True)
cur = con.cursor()
qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now()'
update_qry = 'update twitter_crawl set crawl_status=1 where sk=%s'
