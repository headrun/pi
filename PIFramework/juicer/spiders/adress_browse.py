import requests
import json
import MySQLdb
import optparse
import smtplib
import datetime
import time
from datetime import timedelta
import email
import getpass
import imaplib
import datetime
import os
import MySQLdb
import re
from auto_input import *


def read():
            
	    m = imaplib.IMAP4_SSL("imap.gmail.com")
	    m.login(sender_mail,sender_pass)
	    m.select('INBOX')

	    resp, items = m.search(None, "FLAGGED")
	    items = items[0].split()

	    for emailid in items:
		resp, data = m.fetch(emailid, "(RFC822)")
		email_body = data[0][1]
		mail = email.message_from_string(email_body)
	
		if 'Addresses for latitude' in mail['Subject'] :
               
		    processing_path = address_processing_path
	            import pdb;pdb.set_trace()	
		    if processing_path:
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

			    att_path = os.path.join(processing_path, filename)
                            import pdb;pdb.set_trace()
			    if not os.path.isfile(att_path) :
				fp = open(att_path, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()

			    files_list = glob.glob(address_processing_path+'/*.xlsx')
			    for _file in files_list:
				W = px.load_workbook(_file, use_iterators = True)
				sheet_list = W.get_sheet_names()

				for xl in sheet_list:

				    sheet_ = W.get_sheet_by_name(name = xl)
				    failed_rows = []

				    for row in sheet_.iter_rows():
					status, indent_number, indent_date, origin_plant_code, origin_plant,\
					dest_plant_code, dest_plant, truck_type_code, truck_type, truck_num, truck_conf = row
					status = status.value







def main():
   
    read_mail = read()
 
   
if __name__ == '__main__':
    main()
