from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *

class Commands(object):
	def main(self, modified_date, linkedin_check, facebook_check, twitter_check, email_from_list, lastseen_date):
		con, cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		if linkedin_check:
			values = (md5("%s%s" % (modified_date, 'linkedin')), modified_date, lastseen_date, 'not_taken', 'not_taken', 'linkedin')
			execute_query(cur, insert_pi_crawl_query % values)
		if twitter_check:
			values = (md5("%s%s" % (modified_date, 'twitter')), modified_date, lastseen_date, 'not_taken', 'not_taken', 'twitter')
			execute_query(cur, insert_pi_crawl_query % values)
		if facebook_check:
			values = (md5("%s%s" % (modified_date, 'facebook')), modified_date, lastseen_date, 'not_taken', 'not_taken', 'facebook')
			execute_query(cur, insert_pi_crawl_query % values)
		close_mysql_connection(con, cur)


if __name__ == '__main__':
    Commands().main('', '', '', '')
