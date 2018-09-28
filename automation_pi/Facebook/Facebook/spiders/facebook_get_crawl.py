from fb_constants import *
import random
import operator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
sys.path.append('/root/automation_pi/table_schemas')
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
	

    def __del__(self):
        close_mysql_connection(self.con, self.cur)


    def mv_file(self, file_name):
        current_path = os.path.dirname(os.path.abspath(__file__))
        cuex = os.path.join(current_path, 'facebook_sheet_files')
        make_dir(cuex)
        cmd = 'mv "%s" %s' % (file_name, cuex)
        os.system(cmd)


    def main(self):
        import pdb;pdb.set_trace()
        email_from_list = self.email_dev_list
        check_inprocess = ''
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
				print cmd
                                try: os.system(cmd)
				except : check_inprocess = ''
                        if check_inprocess and recs_allow:
				variable_agrp_rec = fetchmany(self.cur, self.grp_tt_qury % recs_allow[0])
				variable_tgrp_rec = fetchmany(self.cur, self.grp_tt_qury1 % recs_allow[0])
				if variable_agrp_rec:
					variable_agrp_rec = variable_agrp_rec[0][0]
				else: variable_agrp_rec = '0'
				if variable_tgrp_rec:
					variable_tgrp_rec = variable_tgrp_rec[0][0]
				else: variable_tgrp_rec = '0'
				variable_ugrp_rec = int(variable_tgrp_rec) - int(variable_agrp_rec)
				if variable_agrp_rec or variable_tgrp_rec or variable_ugrp_rec:
					self.alert_mail(variable_tgrp_rec, variable_agrp_rec, variable_ugrp_rec, email_from_list, '', '', '')
					facebook_file_name = 'facebook_data_on_%s.xlsx' % str(datetime.datetime.now())
					cmd1 = 'python xlsheet.py "%s" "%s"' % (recs_allow[0], facebook_file_name)
					print cmd1
					os.system(cmd1)
                                	execute_query(self.cur, self.update_pi_crawl % recs_allow[2])
					file_id = Googleupload().main('Facebook', email_from_list, facebook_file_name)
					self.alert_mail(variable_tgrp_rec, variable_agrp_rec, variable_ugrp_rec, email_from_list, 'again', file_id, facebook_file_name)
					self.mv_file(facebook_file_name)

    def alert_mail(self, totalc, avai, unava, email_from_list, again, file_id, facebook_file_name):
        sender_mail = sender_mail_pi
        receivers_mail_list = email_from_list
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Test mail: Final stats for Facebook'
        mas = '<h3>Runs are completed, Please find stats for facebook<h3></br>'
        mas += '<p>Total : %s</p>' % str(totalc)
        mas += '<p>Available : %s</p>' % str(avai)
        mas += '<p>UnAvailable : %s</p>' % str(unava)
	if not again:
	        mas += '<p>[Note: Sheet runs are in progress]</p>'
	else:
	        mas += '<p>File name : %s</p>'% str(facebook_file_name)
        	mas += '<p>File is uploaded in Linkedin [sub-folder] of  PositiveIntegers [folder] in google drive of %s</p>' % sender_mail_pi
	        mas += '<p>Doc Link : "https://docs.google.com/spreadsheets/d/%s"</p>' % str(file_id)
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
