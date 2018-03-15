from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *

class Login(object):

    def __init__(self):
	self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.select_qry = twitter_select_qry
        self.update_qry = twitter_upd_qry
	
    def __del__(self):
	close_mysql_connection(self.con, self.cur)

    def main(self):
	email_from_list = email_dev_list
	check_inprocess = ''
	if len(sys.argv) == 2 and sys.argv[1] == 'prod':
		email_from_list = email_prod_list
	recs_allows = fetchall(self.cur, twitter_taken_qry)
	if recs_allows:
		for recs_allow in recs_allows:
			rows = fetchall(self.cur, self.select_qry % (recs_allow[0], recs_allow[1]))
			execute_query(self.cur, update_twitter_pi_crawl % recs_allow[2])
			while rows:
				rows = fetchall(self.cur, self.select_qry % (recs_allow[0], recs_allow[1]))
				if not rows: break
			        for row in rows:
				    check_inprocess = 'yes'
				    sk,screen_url,aux_info = row
                                    args_name = screen_url.split('/')[-1]
			       	    email_id = json.loads(aux_info).get('email_address', '')
		        	    cmd = "python tweet_analyzer.py -n %s -e %s -sk %s"%(args_name,email_id,sk)
				    if not email_id:
					cmd = "python tweet_analyzer.py -n %s -sk %s" % (args_name,sk)
				    self.update_status(sk, '9', 'twitter_crawl', self.update_qry)
        			    self.cur.execute(self.update_qry % sk)
				    self.con.commit()
		        	    os.system(cmd)
			"""if check_inprocess and recs_allow:
				cmd1 = 'python twitter_xlsheet.py -d %s -m %s -p %s' % (DB_NAME_REQ, recs_allow[0].replace(' ','#'), ','.join(email_from_list))
				print cmd1
				os.system(cmd1)
				execute_query(self.cur, update_twitter_sheet_pi_crawl % recs_allow[2])"""

    def update_status(self, sk, crawl_status, table_name, update_qrys):
	delete_query = 'DELETE FROM %s WHERE crawl_status=%s AND sk ="%s"' % (table_name, crawl_status, sk)
	execute_query(self.cur, delete_query)
	bkup_query = 'select sk from %s where sk = "%s" group by sk  having count(sk)>1' % (table_name, sk)
	try: self.cur.execute(update_qrys % sk)
	except: 
		try:
			recs_ = fetchall(self.cur, bkup_query)
			if recs_:
				query2 = 'select max(modified_at) from %s where sk ="%s"'%(table_name, sk)
				recs_1 = fetchall(self.cur, query2)
				del_qu = "delete from %s where sk ='%s' and modified_at not like '%s'" % (table_name, sk, str(recs_1[0][0]))
				execute_query(self.cur, del_qu)
				self.cur.execute(update_qrys % sk)
		except:
			pass


if __name__ == '__main__':
    Login().main()

