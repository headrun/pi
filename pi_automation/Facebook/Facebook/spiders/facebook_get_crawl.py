from fb_constants import *
import random
import operator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
sys.path.append('/root/pi_automation/table_schemas')
from to_udrive import *
from generic_functions import *
from pi_db_operations import *



class Facebookgetcrawl(object):
	
    def __init__(self):
        self.con, self.cur = get_mysql_connection(DB_HOST, REQ_DB_NAME, '')
	self.email_dev_list = email_dev_list
	self.email_prod_list = email_prod_list
	self.facebook_taken_qry = fb_facebook_taken_qry
	self.zero_queryi = fb_zero_queryi
	self.update_pi_crawl = fb_update_pi_crawl
	self.grp_tt_qury = fb_grp_tt_qury
	self.grp_tt_qury1 = fb_grp_tt_qury1
	self.status_qry = "select count(*),crawl_status from facebook_crawl where date(modified_at)>='%s' group by crawl_status having count(sk)>=1" 

    def __del__(self):
        close_mysql_connection(self.con, self.cur)


    def mv_file(self, file_name):
        current_path = os.path.dirname(os.path.abspath(__file__))
        cuex = os.path.join(current_path, 'facebook_sheet_files')
        make_dir(cuex)
        cmd = 'mv "%s" %s' % (file_name, cuex)
        os.system(cmd)


    def main(self):
        email_from_list = self.email_dev_list
        check_inprocess = ''
        import pdb;pdb.set_trace()
        if len(sys.argv) == 2 and sys.argv[1] == 'prod':
                email_from_list = self.email_prod_list
        recs_allows = fetchall(self.cur, self.facebook_taken_qry)
        if recs_allows:
                for recs_allow in recs_allows:
                        rows = fetchall(self.cur, self.zero_queryi % (recs_allow[0]))
			execute_query(self.cur, self.update_pi_crawl % recs_allow[2])
                        while rows:
                                rows = fetchall(self.cur, self.zero_queryi % (recs_allow[0]))
                                if not rows: break
                                check_inprocess = 'yes'
                                cmd = scrapy_run_cmd_fb % (random.choice(constants_dict.keys()), recs_allow[0])
                                try: os.system(cmd)
				except : check_inprocess = ''
                data = fetchall(self.cur, self.status_qry % (recs_allow[1]))
                if data :
                            import pdb;pdb.set_trace()
                            ava = int(data[0][0])
                            not_avai = int(data[1][0])
                            total = not_avai + ava
                            self.alert_mail(ava,not_avai,total)

    def alert_mail(self, ava, not_avai, total):
        sender_mail = sender_mail_pi
        receivers_mail_list = ['anushab@headrun.net']
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = ' Runs are Done and below are the data stats for facebook'
        mas = '<h4>Stats for Facebook<h4></br>'
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
    Facebookgetcrawl().main()
