import MySQLdb
import json
import datetime
import re
class Lixlspub(object):

    def __init__(self, *args, **kwargs):
        self.con = MySQLdb.connect(db   = 'FACEBOOK', \
        host = 'localhost', charset="utf8", use_unicode=True, \
        user = 'root', passwd ='root')
        self.cur = self.con.cursor()
	self.query1 = "select url,sk from linkedin_crawl where crawl_status!=10 and url like '%/pub/%'"
	self.updateqry1 = "update linkedin_crawl set crawl_status=0, url = '%s' where sk = '%s'"

    def send_xls(self):
	self.cur.execute(self.query1)
	records = self.cur.fetchall()
	for rec in records:
		new_url =  ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',rec[0])),'-',''.join(''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',rec[0]))).split('/')[::-1])))
		print (self.updateqry1%(new_url,rec[1])).encode('utf-8')
		self.cur.execute(self.updateqry1%(new_url,rec[1]))

def main():
        obj = Lixlspub()
        obj.send_xls()
if __name__ == '__main__':
        main()

