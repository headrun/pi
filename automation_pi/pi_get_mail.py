"""fetching sheets from mail"""
import email
import imaplib
import os
import re
import datetime
from generic_functions import make_dir, textify
from pi_excelsheet_parsing import *

class Pimail(object):
	""" start """
	def __init__(self):
		current_path = os.path.dirname(os.path.abspath(__file__))
		self.social_processing_path = os.path.join(current_path, 'excelfiles')
		make_dir(self.social_processing_path)

	def main(self):
		mid = imaplib.IMAP4_SSL("imap.gmail.com")
		mid.login('facebookdummyfb01@gmail.com', '01123123')
		mid.select('INBOX')
		items = mid.search(None, "FLAGGED")
		items = items[1][0].split()
		for emailid in items:
			data = mid.fetch(emailid, "(RFC822)")[1]
			email_body = data[0][1]
			mail = email.message_from_string(email_body)
			mail_from = mail['From']
			mail_from = textify(re.findall('<(.*?)>', mail_from))
			if mail_from in ['kiranmayi@headrun.net', 'facebookdummyfb01@gmail.com']:
				subject = mail['Subject']
				date_time = mail['Date']
				if subject.lower():
				    for part in mail.walk():
					    if part.get_content_maintype() == 'multipart':
							continue
					    if part.get('Content-Disposition') is None:
							continue
					    filename = part.get_filename()
					    filename = 'Social_%s.xlsx'\
				 % datetime.datetime.strftime(datetime.datetime.now(), '%s')
					    cnt = 1
					    if not filename:
							filename = 'part-%03d%s' % (cnt, 'bin')
							cnt += 1
					    filename = mail["From"]+'___'+str(date_time) + '_' + filename
					    att_path = os.path.join(self.social_processing_path, filename)
					    if not os.path.isfile(att_path):
							filep = open(att_path, 'wb')
							filep.write(part.get_payload(decode=True))
							filep.close()
		Piparsing().main()

if __name__ == '__main__':
    Pimail().main()

