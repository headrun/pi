from linkedin_voyager_functions import *

class Lvccp(object):
	def __init__(self, options):
		self.modified_at       = options.modified_at
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		self.query = 'insert into linkedin_crawl(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values(%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at=now(), content_type=%s, crawl_status=0,meta_data=%s'
		self.query2 = "select connections_profile_url, member_id, sk from FACEBOOK.linkedin_connections where date(modified_at) >= '%s'" % self.modified_at
		self.main()

	def __del__(self):
		close_mysql_connection(self.con, self.cur)

	def main(self):
		total_connection_records = fetchall(self.cur, self.query2)
		counter = 0
		for tocr in total_connection_records:
			meta_date_from_browse = {}
			linkedin_profilef, member_id, connection_sk = tocr
			meta_date_from_browse.update({"linkedin_url":linkedin_profilef, 'member_id': member_id})
			#sk_v = "%s%s"%(linkedin_profilef, str(member_id))
			#sk = md5(normalize(sk_v))
			sk = connection_sk
			crawl_status = 0
			try:
				values =  (sk,  MySQLdb.escape_string(normalize(linkedin_profilef)), 'linkedin', crawl_status,  MySQLdb.escape_string(json.dumps(meta_date_from_browse).encode('utf-8')), 'linkedin',  MySQLdb.escape_string(json.dumps(meta_date_from_browse).encode('utf-8')))
				counter += 1
				print counter
				#execute_query(self.cur, self.query % values)
				self.cur.execute(self.query, values)
			except: print normalize(linkedin_profilef)
			


if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-m', '--modified_at', default = '', help = 'modified_at')
	(options, args) = parser.parse_args()
	Lvccp(options)


	
