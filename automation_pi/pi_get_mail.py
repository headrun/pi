"""fetching sheets from mail"""
import email
import imaplib
import os
import re
import datetime
from table_schemas.generic_functions import make_dir, textify
from table_schemas.pi_db_operations import *
from pi_excelsheet_parsing import *

class Pimail(object):
	""" start """
	def __init__(self, options):
		self.set_up = options.setup
		current_path = os.path.dirname(os.path.abspath(__file__))
		self.social_processing_path = os.path.join(current_path, 'excelfiles')
		make_dir(self.social_processing_path)
		self.main()

	def main(self):
		mid = imaplib.IMAP4_SSL("imap.gmail.com")
                import pdb;pdb.set_trace()
		mid.login(sender_mail_pi, sender_pwd_pi)
		mid.select('INBOX')
		items = mid.search(None, "UNSEEN")
		email_from_list = email_dev_list 
		if self.set_up == 'prod':
			items = mid.search(None, "UNSEEN")
			email_from_list = email_prod_list
		items = items[1][0].split()
		check_true = ''
		for emailid in items:
			data = mid.fetch(emailid, "(RFC822)")[1]
			email_body = data[0][1]
			mail = email.message_from_string(email_body)
			mail_from = mail['From']
                        import pdb;pdb.set_trace()
			mail_from = textify(re.findall('<(.*?)>', mail_from))
			email_from_list = email_dev_list 
			if mail_from in mailids_from_list:
				subject = mail['Subject']
				date_time = mail['Date']

				if 'profiles' in subject.lower() or "Run the crawler for FB" in subject.lower():
                                    import pdb;pdb.set_trace()
				    check_true = 'yes'
				    for part in mail.walk():
					    if part.get_content_maintype() == 'multipart':
							continue
					    if part.get('Content-Disposition') is None:
							continue
					    filename = part.get_filename()
					    cnt = 1
					    if not filename:
							filename = 'part-%03d%s' % (cnt, 'bin')
							cnt += 1
					    att_path = os.path.join(self.social_processing_path, filename)
					    if not os.path.isfile(att_path):
							filep = open(att_path, 'wb')
							filep.write(part.get_payload(decode=True))
							filep.close()
					    if items and check_true and filename:
							Piparsing().main(email_from_list)
			

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-s', '--setup', default='', help = 'setup')
    (options, args) = parser.parse_args()
    Pimail(options)

