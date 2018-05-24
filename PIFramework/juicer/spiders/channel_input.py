
#Inputs to crawl channel info

channel_id = 'UCGBnz-FR3qaowYsyIEh2-zw'
Access_key = 'AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E'
start_link = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&id=UCGBnz-FR3qaowYsyIEh2-zw&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E'
meta_link = 'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId=UCGBnz-FR3qaowYsyIEh2-zw&maxResults=50&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E'
 
video_link = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId={video Id}&key=AIzaSyBgUp3y8lmbuyCShJvnbuZT9HwX-EH8E8E&maxResults=100'

#queries

channel_insert_query = "insert into Channel(sk, title, description, channel_country, image, reference_url, created_at, modified_at, last_seen) values (%s, %s, %s, %s, %s, %s, now(), now(), now())"

video_insert_qry = 'insert into Video_Info(sk, program_sk, title, description, video_link, reference_url, created_at, modified_at, last_seen) values (%s, %s, %s, %s, %s, %s, now(), now(), now())'

richmedia_insert_qry = 'insert into RichMedia(sk, program_sk, program_type, image_url, reference_url, created_at, modified_at) values (%s, %s, %s, %s, %s, now(), now())'

update_qry = 'update  Channel set crawl_status=0  where sk = %s and crawl_status = 9'

del_qry = 'delete from %s where sk = "%s"' 


comments_insert_qry = 'insert into comments(sk, program_sk, channel_sk, comment, no_of_comments, likes, rating, author_name, reference_url, published_at, updated_at, created_at, modified_at, last_seen, auth_channel_url, auth_channel_id, auth_image_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now(), now(), %s, %s, %s)'

