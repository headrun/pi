import MySQLdb

db_user = 'root'
db_passwd = ''
db_host  = 'localhost'
db_name = 'LINKEDIN_COMMENTS'

con = MySQLdb.connect(db=db_name,
                      user=db_user,
                      passwd=db_passwd,
                      charset="utf8",
                      host=db_host,
                      use_unicode=True)
cur = con.cursor()

query1 = 'insert into Linkedin_comments(comment_sk, comment_main_sk, comment_by, comment_time, comment_by_image, comment_by_url, comment_description, comment_title, comment_total_likes, comment_count, reference_url, created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,now(),now()) on duplicate key update modified_at = now(), comment_sk=%s'

query2 = 'insert into Linkedin_replies(sk, comment_sk, comment_main_sk, reply_by, reply_time, reply_by_image, reply_by_url, reply_text, reply_title, reply_total_likes, reply_count, reference_url, created_at,modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(),now()) on duplicate key update modified_at = now(), sk=%s'
