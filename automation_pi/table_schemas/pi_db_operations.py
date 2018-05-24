insert_script_query = 'insert into %s(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values("%s", "%s", "%s", "%s", "%s", now(), now()) on duplicate key update modified_at=now(), meta_data="%s"'
insert_pi_crawl_query = 'insert into pi_crawl (sk, profiles_start_modified_at, profiles_end_modified_at, profiles_sheet_status, profiles_run_status, social_media_type, created_at, modified_at) values("%s", "%s", "%s", "%s", "%s", "%s", now(), now()) on duplicate key update modified_at=now()'
email_dev_list = ['kiranmayi@headrun.com', 'anushab@headrun.com']
email_prod_list = ['kiranmayi@headrun.com', 'anushab@headrun.com']
sender_mail_pi = 'positiveintegersproject@gmail.com'
sender_pwd_pi = 'integers'
mailids_from_list = ['anushab@headrun.com']
zero_quer = "select count(*) from %s where modified_at >= '%s' and crawl_status=0"

#Access and Consumer Tokens
access_token="2826154500-Kt43ZckLttYHvip2wlvhTTyK6AScEsSxEpxHzPG"
access_token_secret="UoDlnNmGlTM2HH2Vw2dFF18K5oYAUVxulmAqMs4UfUMb4"
consumer_key="KUFycnEBUXtEzem3Pk3omGdZJ"
consumer_secret="8wW82SXdRi6aWpgKV7fjTPYrvFxoRQencwWng1y3oeli2ZljFD"

#twitter
twitter_qry = 'insert into Twitter_latest(sk,screen_name,name,description,location,tweets,following,followers,likes,image,lists,timezone,language,is_verified,twitter_url,email_id,aux_info,top_10_hashtags,top_5_mentioned_users,retweeted_percentage,retweeted_users,Most_referenced_domains,detected_sources,detected_languages,Avg_no_of_tweets_per_day,created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now(),sk=%s,screen_name=%s,name=%s,description=%s,location=%s,tweets=%s,following=%s,followers=%s,likes=%s,image=%s,lists=%s,timezone=%s,language=%s,is_verified=%s,twitter_url=%s,email_id=%s,aux_info=%s,top_10_hashtags=%s,top_5_mentioned_users=%s,retweeted_percentage=%s,retweeted_users=%s,Most_referenced_domains=%s,detected_sources=%s,detected_languages=%s,Avg_no_of_tweets_per_day=%s'

twitter_update_qry = 'update twitter_crawl set crawl_status=1 where sk="%s" and crawl_status =9'

twitter_select_qry = 'select  sk, url, meta_data from twitter_crawl where crawl_status = 0 and (created_at between "%s" and "%s") limit 80'

twitter_upd_qry = 'update twitter_crawl set crawl_status=9 where sk= "%s" and crawl_status=0'

twitter_taken_qry = "select profiles_start_modified_at, profiles_end_modified_at, sk from pi_crawl where social_media_type = 'twitter' and profiles_run_status = 'not_taken'"
update_twitter_pi_crawl = "update pi_crawl set profiles_run_status = 'taken' where sk = '%s'"
update_twitter_sheet_pi_crawl = "update pi_crawl set profiles_sheet_status = 'taken' where sk = '%s'"

#Facebook_get_crawl
fb_facebook_taken_qry = "select profiles_start_modified_at, profiles_end_modified_at, sk from pi_crawl where social_media_type = 'facebook' and profiles_run_status = 'not_taken'"
fb_zero_queryi = 'select  sk, url from facebook_crawl where crawl_status = 0 and modified_at >= "%s"'
fb_update_pi_crawl = "update pi_crawl set profiles_run_status = 'taken' where sk = '%s'"
fb_grp_tt_qury = "select count(*) from facebook_profiles where modified_at >= '%s' and profile_id != '' and name != '' and aux_info != '{}'"
fb_grp_tt_qury1 = "select count(*) from facebook_profiles where modified_at >= '%s'"

#Linkedin_get_crawl
ln_linkedin_taken_qry = "select profiles_start_modified_at, profiles_end_modified_at, sk from pi_crawl where social_media_type = 'linkedin' and profiles_run_status = 'not_taken'"
ln_zero_queryi = 'select  sk, url from linkedin_crawl where crawl_status = 0 and modified_at >= "%s"'
ln_grp_tt_qury = "select count(*), crawl_status  from linkedin_crawl where  modified_at >= '%s' group by crawl_status"

constants_dict_fb = {'email':['yagnasree@headrun.com','yagna^123']}

scrapy_run_cmd_fb = '/usr/local/bin/scrapy crawl facebook_crawler -a login="%s" --set  ROBOTSTXT_OBEY=0 -a mpi="%s" --set HTTPCACHE_ENABLED=0'

#linkedin_constants
#'ramanujan':['srinivasaramanujan427@gmail.com','dotoday1#']
#'meatproject':['meatproject05@gmail.com','ram123123']
mails_dict_ln = {'ccv':['ccvy1.pavani1886@gmail.com','ccvy1.pavani@1886'],'smiley':['smileykutie@gmail.com','smileykutie$'],'ramanujan':['srinivasaramanujan427@gmail.com','dotoday1#'],'meatproject':['meatproject05@gmail.com','ram123123']}

ips_list_ln = ['144.76.48.143', '144.76.48.144',
                '144.76.48.145', '144.76.48.146',
                '144.76.48.147', '144.76.48.148',
                '144.76.48.149', '144.76.48.150',
                '176.9.181.37', '176.9.181.40',
                '176.9.181.41']
#ips_list_block=['176.9.181.34']

login_cmds_ip_ln = ['/usr/local/bin/scrapy crawl linkedinapivoyager_browse -a login="ccv" --set ROBOTSTXT_OBEY=0 --set HTTPCACHE_ENABLED=0  --set HTTP_PROXY="http://176.9.181.37:3279" -a mpi="%s"', 'scrapy crawl linkedinapivoyager_browse -a login="smiley" --set ROBOTSTXT_OBEY=0 --set HTTPCACHE_ENABLED=0  --set HTTP_PROXY="http://176.9.181.40:3279" -a mpi="%s"','scrapy crawl linkedinapivoyager_browse -a login="meatproject" --set ROBOTSTXT_OBEY=0 --set HTTPCACHE_ENABLED=0  --set HTTP_PROXY="http://176.9.181.41:3279" -a mpi="%s"']

dic_ln = {"linkedin_profilesskira2.log":["kira2headrun@gmail.com",'kira^123'],"linkedin_profilessmile.log":["smileykutie@gmail.com","smileykutie$"], "linkedin_profilesccv.log":["ccvy1.pavani1886@gmail.com",'ccvy1.pavani@1886'],"linkedin_profilesmeat.log":["meatproject05@gmail.com","ram123123"],"linkedin_profiles.log":["srinivasaramanujan427@gmail.com","dotoday1#"], 'linkedin_get_crawl.log':["srinivasaramanujan427@gmail.com","dotoday1#"]}
	
