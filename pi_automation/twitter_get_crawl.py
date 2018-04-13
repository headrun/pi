from table_schemas.generic_functions import *
from table_schemas.pi_db_operations import *
from  table_schemas.generic_functions import *
from table_schemas.to_udrive import *
from table_schemas.pi_db_operations import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
from email import encoders


class Login(object):

    def __init__(self):
	self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
        self.select_qry = twitter_select_qry
        self.update_qry = twitter_upd_qry
        self.status_qry = "select count(*),crawl_status from twitter_crawl where date(modified_at)>='%s' group by crawl_status having count(sk)>1"
	
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
                                    s_no = str(json.loads(aux_info).get('sno', ''))
		        	    cmd = "python tweet_analyzer.py -n %s -e %s -sk %s" %(args_name,email_id,sk)
				    if not email_id:
					cmd = "python tweet_analyzer.py -n %s -sk %s" % (args_name,sk)
				    self.update_status(sk, '9', 'twitter_crawl', self.update_qry)
        			    self.cur.execute(self.update_qry % sk)
				    self.con.commit()
		        	    os.system(cmd)
                                    cmd1 = 'python twitter_denormalisation_script.py -s %s -k %s'% (sk , s_no)
                                    os.system(cmd1)
                        data = fetchall(self.cur, self.status_qry % (recs_allow[1]))
                        if data :
                            ava = int(data[0][0])
                            not_avai = int(data[1][0])
                            total = not_avai + ava
                            self.alert_mail(ava,not_avai,total)
                 
				
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


    def alert_mail(self, ava, not_avai, total):
        sender_mail = sender_mail_pi
        receivers_mail_list = ['anushab@headrun.net']
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = ' Runs are Done and below are the data stats for Twitter'
        mas = '<h4>Stats for Twitter<h4></br>'
        mas += '<p>Total : %s</p>' % str(total)
        mas += '<p>Available : %s</p>' % ava
        mas += '<p>UnAvailable : %s</p>' % not_avai
        msg['From'] = sender
        msg['To'] = receivers
        tem = MIMEText(''.join(mas), 'html')
        msg.attach(tem)
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        s.login(sender_mail, sender_pwd_pi)
        s.sendmail(sender, receivers_mail_list, msg.as_string())
        s.quit()




if __name__ == '__main__':
    Login().main()

