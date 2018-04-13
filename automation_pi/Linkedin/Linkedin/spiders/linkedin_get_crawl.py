from linkedin_logins import *
import random
import operator
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
sys.path.append('/root/automation_pi/table_schemas')
from to_udrive import *
from generic_functions import *
from pi_db_operations import *

class Linkedingetcrawl(object):
	
    def __init__(self):
        self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
	self.email_dev_list = email_dev_list
	self.email_prod_list = email_prod_list
	self.linkedin_taken_qry = ln_linkedin_taken_qry
	self.zero_queryi = ln_zero_queryi
	self.update_pi_crawl = fb_update_pi_crawl
	self.grp_tt_qury = ln_grp_tt_qury

    def __del__(self):
        close_mysql_connection(self.con, self.cur)

    def mv_file(self, file_name):
	current_path = os.path.dirname(os.path.abspath(__file__))
	cuex = os.path.join(current_path, 'linkedin_sheet_files')
	make_dir(cuex)
	cmd = 'mv "%s" %s' % (file_name, cuex)
	os.system(cmd)


    def main(self):
        email_from_list = self.email_dev_list
        check_inprocess = ''
        if len(sys.argv) == 2 and sys.argv[1] == 'prod':
                email_from_list = self.email_prod_list
	
        recs_allows = fetchall(self.cur, self.linkedin_taken_qry)
        if recs_allows:
                for recs_allow in recs_allows:
                        rows = fetchall(self.cur, self.zero_queryi % (recs_allow[0]))
			execute_query(self.cur, self.update_pi_crawl % recs_allow[2])
                        while rows:
                                rows = fetchall(self.cur, self.zero_queryi % (recs_allow[0]))
                                if not rows: break
                                check_inprocess = 'yes'
                                cmd = random.choice(login_cmds_ip) % (recs_allow[0])
                                os.system(cmd)
				file("linkedin_command","ab+").write("%s\n" %cmd)
                        if check_inprocess and recs_allow:
				variable_grp = self.grp_tt_qury % recs_allow[0]
				variable_tcgrp = fetchmany(self.cur, variable_grp)
				if variable_tcgrp:
					total_counts = str(sum(map(operator.itemgetter(0), variable_tcgrp)))
					success_count = [item for item in variable_tcgrp if item[1] == 1]
					if success_count:
						success_count = success_count[0][0]
					else:
						success_count = 0
					faliure_count = [item for item in variable_tcgrp if item[1] != 1]
					if faliure_count:
						 faliure_count = sum(map(operator.itemgetter(0), faliure_count))
					else:
						faliure_count = 0
					self.alert_mail(success_count, faliure_count, email_from_list, '', '')
					set_limit_to = '1000'
					file_ids_limit = []
					if (int(total_counts)) <=1000:
						linkedin_file_name = 'linkedin_data_on_%s.csv' % str(datetime.datetime.now())
						cmd1 = 'python linkedin_csvsheetprofiles.py -i %s -f "%s"' % (recs_allow[0].replace(' ','#'), linkedin_file_name)
						print cmd1
						os.system(cmd1)
						
						file_id = Googleupload().main('Linkedin', email_from_list, linkedin_file_name)
						if os.path.isfile(linkedin_file_name):
							file_ids_limit.append((file_id, linkedin_file_name))
							self.mv_file(linkedin_file_name)
					else:
						new_limit = set_limit_to
						for ic in range(int(total_counts)):
							linkedin_file_namel = 'linkedin_data_on_%s_limit_%s.csv' % (str(datetime.datetime.now()), new_limit.replace(',','_'))
							cmd1 = 'python linkedin_csvsheetprofiles.py -i %s -l %s -f "%s"' % (recs_allow[0].replace(' ','#'), new_limit, linkedin_file_namel)
							os.system(cmd1)
							if os.path.isfile(linkedin_file_namel):
								file_id = Googleupload().main('Linkedin', email_from_list, linkedin_file_namel)
								file_ids_limit.append((file_id, linkedin_file_namel))
								self.mv_file(linkedin_file_namel)
								
							if ',' not in new_limit:
								new_limit = "%s%s%s" % ((int(new_limit)+1), ',', '1000')
							else:
								if ',' in new_limit:
									new_limit = "%s%s%s" % ((int(new_limit.split(',')[0])+int(new_limit.split(',')[1])), ',', '1000')
							if int(new_limit.split(',')[0])>int(total_counts):
								break
					self.alert_mail(success_count, faliure_count, email_from_list, file_ids_limit, 'again')
                                	execute_query(self.cur, self.update_pi_crawl % recs_allow[2])


    def alert_mail(self, avai, unava, email_from_list, file_ids_limit, again):
        sender_mail = sender_mail_pi
        receivers_mail_list = email_from_list
        sender, receivers  = sender_mail, ','.join(receivers_mail_list)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Test mail: Final stats for Linkedin'
        mas = '<h3>Runs are completed, Please find stats for Linkedin<h3></br>'
        mas += '<br />Total : %s' % str(avai+unava)
        mas += '<br />Available : %s' % str(avai)
        mas += '<br />UnAvailable : %s' % str(unava)
	if not again:
	        mas += '<br /> <br />[Note: Sheet runs are in progress]'
	else:
		if len(file_ids_limit) == 1:
			mas += '<br />File name : %s'% str(file_ids_limit[0][1])
			mas += '<br />File is uploaded in Linkedin [sub-folder] of  PositiveIntegers [folder] in google drive of %s' % sender_mail_pi
			mas += '<br />Doc Link : "https://docs.google.com/spreadsheets/d/%s"' % str(file_ids_limit[0][0])
		else:
			if len(file_ids_limit) > 1:
				mas += '<br />Below are the list of sheets that are uploaded in google drive with respect to limit'
				file_ms_names = ', '.join(list(map(itemgetter(1), file_ids_limit)))
				file_ms_links = list(map(itemgetter(0), file_ids_limit))
				doc_sp_links = "https://docs.google.com/spreadsheets/d/%s"
				doc_sp_lks = ', '.join([doc_sp_links % itemg for itemg in file_ms_links])
				mas += '<br />File names : %s'% str(file_ms_names)
				mas += '<br />Files are uploaded in Linkedin [sub-folder] of  PositiveIntegers [folder] in google drive of %s' % sender_mail_pi
				mas += '<br />Doc Links : %s' % str(doc_sp_lks)
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
    Linkedingetcrawl().main()
