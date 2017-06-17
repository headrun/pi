from linkedin_functions import *

class Linkedinfetching(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.limit = options.limit
		self.con1, self.cur1 = get_mysql_connection(DB_HOST, 'LINKEDIN_VOYAGER', '')
		self.query1 = "select count(*), member_id, sk from linkedin_meta where date(modified_at)<'2017-05-02' group by member_id having count(*)>=1 limit %s"% self.limit
		self.query2 = 'select sk from FACEBOOK.linkedin_meta where member_id = "%s" order by modified_at desc limit 1;'
		self.query3 = "select sk from FACEBOOK.linkedin_connectionprofiles where member_id = '%s'"
		self.query4 = "select sk from linkedin_get_member_ids where member_id = '%s'"
		self.update_qry = "insert into linkedin_get_member_ids(sk, member_id, created_at, modified_at, last_seen) values ('%s', '%s', now(), now(), now()) ON DUPLICATE KEY UPDATE last_seen=now(), sk='%s'"
		self.query1_ = "select count(*), member_id, sk from linkedin_meta where member_id = '%s' group by member_id having count(*)>=1"
		self.main()

	def __del__(self):
		close_mysql_connection(self.con, self.cur)
		close_mysql_connection(self.con1, self.cur1)

	def main(self):
		execute_query(self.cur, self.query1)
		counter = 0
		while True:
			records = self.cur.fetchmany(10)
			if not records: break
			for rec in records:
				counter += 1
				count_m, member_id, sk = rec
				if count_m > 1:
					sk = fetchone(self.cur1, self.query2%member_id)
				check = fetchone(self.cur1, self.query3%member_id)
				if not check:
					execute_query(self.cur1, self.update_qry%(sk, member_id, sk))
				print counter

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-l','--limit', default = '', help = 'limit')
	(options, args) = parser.parse_args()
	Linkedinfetching(options)
		
	
