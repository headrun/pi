from linkedin_voyager_functions import *

class Lvcc(object):
	def __init__(self):
		current_path = os.path.dirname(os.path.abspath(__file__))
		self.filec_path = os.path.join(current_path, 'linkedin2.csv')
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		self.query = 'insert into linkedin_mails(sk, email, pass, priority, crawl_type ,crawl_status,created_at, modified_at) values(%s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now(), sk =%s'

	def __del__(self):
		close_mysql_connection(self.con, self.cur)

        def main(self):
            with open(self.filec_path, 'r') as f:
                rows = f.readlines()
                counte = 0 
                for row in rows:
                    print row
                    email_id, passw = row.strip('\n').strip().split(',')
                    if not email_id: continue
                    counte += 1
                    values = (md5(email_id), email_id, passw, counte, 'linkedin', 0, md5(email_id))
                    self.cur.execute(self.query, values)

if __name__ == '__main__':
   Lvcc().main()


	
