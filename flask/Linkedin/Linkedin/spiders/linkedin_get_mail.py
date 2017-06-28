import email
import getpass
import imaplib
from linkedin_voyager_functions import *

class Fbmail(object):

	def __init__(self):
		current_path =  os.path.dirname(os.path.abspath(__file__))
		self.social_processing_path = os.path.join(current_path, 'excelfiles')

	def main(self):
		m = imaplib.IMAP4_SSL("imap.gmail.com")
		m.login('facebookdummyfb01@gmail.com','01123123')
		m.select('INBOX')
		resp, items = m.search(None, "FLAGGED")
		items = items[0].split()
		for emailid in items:
			resp, data = m.fetch(emailid, "(RFC822)")
			email_body = data[0][1]
			mail = email.message_from_string(email_body)
			if 'kiranmayi@headrun.net' in mail['From'] or 'facebookdummyfb01@gmail.com' in mail['From']:
				subject = mail['Subject']
				date_time =  mail['Date']
				if subject.lower():
				    processing_path = self.social_processing_path
				    for part in mail.walk():
					    if part.get_content_maintype() == 'multipart':
						continue
					    if part.get('Content-Disposition') is None:
						continue
					    filename = part.get_filename()
					    filename = 'Social_%s.xlsx'%datetime.datetime.strftime(datetime.datetime.now(), '%s')
					    cnt = 1
					    if not filename:
						filename = 'part-%03d%s' % (cnt, 'bin')
						cnt += 1
					    filename = mail["From"]+'___'+str(date_time) + '_' + filename
					    att_path = os.path.join(processing_path, filename)
					    if not os.path.isfile(att_path) :
						fp = open(att_path, 'wb')
						fp.write(part.get_payload(decode=True))
						fp.close()

if __name__ == '__main__':
    Fbmail().main()

