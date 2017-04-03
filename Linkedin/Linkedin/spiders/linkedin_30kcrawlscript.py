import MySQLdb
import datetime
import json
import re
#import urllib



class Linkedincrawl3(object):

	def __init__(self):
		self.con = MySQLdb.connect(db='FACEBOOK',
		user='root', passwd='root',
		charset="utf8", host='localhost', use_unicode=True)
		self.cur = self.con.cursor()
		self.query = 'insert into linkedin_crawl(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values(%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at=now(), content_type=%s, crawl_status=%s, meta_data=%s, sk=%s'
		self.selectqry = 'select sk, clean_url, meta_data, flag from linkedin_crawl30'

	def __del__(self):
		self.cur.close()
		self.con.close()

	def rep_spl(self, var):
        	"""To remove unwanted characters"""
	        var = str(var).replace('\r', '').replace('\n', '')\
        	.replace('\t', '').replace(u'\xa0', '').replace(u'\xc2\xa0', '').replace(u'\xc3\u0192\xc2\xb1',' ').strip()
	        if 'none' in var.lower():
        	    var = ''
	        return var
	def main(self):
		self.cur.execute(self.selectqry)
		records = self.cur.fetchall()
		for inde , record in enumerate(records):
			sk, clean_url, meta_data, flag = record
			#try: clean_url = urllib.quote(clean_url)
			#except: import pdb;pdb.set_trace()
			stau  = 5
			if 'true' in flag.lower(): stau  = 0
			values = (sk, clean_url, 'linkedin', stau, meta_data,'linkedin', stau, meta_data,sk)
			self.cur.execute(self.query, values)
if __name__ == '__main__':
    Linkedincrawl3().main()

