from linkedin_voyager_functions import *
from linkedin_voyage_queries import *
from linkedin_logins import mails_dict

class Lidefault(object):

	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')

	def __del__(self):
		self.con.close()
		self.cur.close()


	def main(self):
		for key, value in mails_dict.iteritems():
			logind_date = "%s%s"%(str(datetime.datetime.now().date()), ' 00:00:00')
			account_mail = value[0]
			get_sk_login = fetchall(self.cur, get_insert_count_qry % (key, logind_date))
			if not get_sk_login:
                		insert_count = execute_query(self.cur, (insert_count_qry % (key, account_mail, 0, logind_date, key, account_mail, 0, logind_date)))


if __name__ == '__main__':
	Lidefault().main()
	

