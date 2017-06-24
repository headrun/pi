from linkedin_functions import *

class Linkedinkey(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.query1 = "select b.sk, a.url, b.member_id, a.meta_data from LINKEDIN_VOYAGER_CRAWL.linkedin_crawl a, FACEBOOK.linkedin_meta b where (a.meta_data like '%\"keys\"%'  or  a.meta_data like '%\"key\"%') and (SUBSTRING(a.sk, 1, CHAR_LENGTH(a.sk) - 7) = b.sk);"
		self.query2 = "select meta_data, sk from  LINKEDIN_VOYAGER_CRAWL.linkedin_crawl where (meta_data like '%\"keys\"%'  or meta_data like '%\"key\"%') and SUBSTRING(sk, 1, CHAR_LENGTH(sk) - 7)  not in (select sk from FACEBOOK.linkedin_meta);"

		self.track = 'INSERT INTO linkedin_track(sk, member_id, login_mail_id, machine_ip, crawl_status, given_key, aux_info,created_at, modified_at, last_seen) values("%s", "%s", "%s", "%s", "%s", "%s", "%s", now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk="%s", member_id="%s", login_mail_id="%s", machine_ip="%s", crawl_status="%s", given_key="%s", aux_info="%s"'

	def __del__(self):
		close_mysql_connection(self.con, self.cur)

	def main(self):
		list_of_qy = [self.query1, self.query2]
		for lq in list_of_qy:
			execute_query(self.cur, lq)
			counter = 0
			records = self.cur.fetchmany(80)
			for rec in records:
				counter += 1
				sk, url, member_id, meta_data, crawl_status = ['']*5
				if len(rec) == 4:
					sk, url, member_id, meta_data = rec
					crawl_status = '1'
				if len(rec) == 2:
					meta_data, sk = rec
					crawl_status = '6'
					member_id = '0'
				json_ke = json.loads(meta_data)
				given_key = json_ke.get('key','')
				if not given_key:
					given_key = json_ke.get('keys', '')	
				values = (sk, str(member_id), 'srinivasaramanujan427@gmail.com', '176.9.181.34', crawl_status, given_key, MySQLdb.escape_string(meta_data), sk, str(member_id), 'srinivasaramanujan427@gmail.com', '176.9.181.34', crawl_status, given_key, MySQLdb.escape_string(meta_data))
				execute_query(self.cur, self.track%values)


if __name__ == "__main__":
	Linkedinkey().main()
		
	
