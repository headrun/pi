from generic_functions import *

class Fbpagescrawl(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.insert_query = 'insert into facebook_pages_crawl(sk, url, \
		content_type ,crawl_status, meta_data,created_at, modified_at)\
		 values("%s", "%s", "%s", "%s", "%s", now(), now())\
		 on duplicate key update modified_at=now(), meta_data="%s"'

	def __del__(self):
		close_mysql_connection(self.con, self.cur)
		
	def main(self):
		with open('facebook_pages.txt', 'r') as f:
			rows = f.readlines()
			for inde, row in enumerate(rows):
				row = row.strip('\n')
				meta_date_from_browse = {}
				sk = md5(row)
				values = (sk, row, 'facebook_page', 0,
				MySQLdb.escape_string(json.dumps(meta_date_from_browse)),
				MySQLdb.escape_string(json.dumps(meta_date_from_browse)))
				execute_query(self.cur, self.insert_query % values)
if __name__ == '__main__':
	Fbpagescrawl().main()
