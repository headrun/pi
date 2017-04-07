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
	#self.query1 = "select url,sk from linkedin_crawl where crawl_status!=10 and url like '%/pub/%'"
	#self.query1 = "select sk , url, meta_data from linkedin_crawl where  date(modified_at)>= '2017-03-27' and crawl_status!=5 and meta_data like '%/pub/%';"
	#self.query1 = "select sk , url, meta_data from linkedin_crawl where  date(modified_at)>= '2017-03-27' and crawl_status=6 and meta_data like '%/pub/%'"
	#self.query1 = "select sk , url, meta_data from linkedin_crawl where date(modified_at)>= '2017-03-27' and meta_data like '%/fr\"%' and (crawl_status=6 or crawl_Status=0)"
	self.query1 = "select sk , url, meta_data from linkedin_crawl where date(modified_at)>= '2017-03-27' and crawl_status=6"
	self.updateqry1 = "update linkedin_crawl set crawl_status=0, url = '%s' where sk = '%s'"
	self.queryon = "select member_url from Linkedin where sk = '%s'"

    def send_xls(self):
	self.cur.execute(self.query1)
	records = self.cur.fetchall()
	for rec in records:
		sk, url, meta_data = rec
		linke_url = json.loads(meta_data).get('linkedin_url','')
		self.cur.execute(self.queryon%sk)
		new_on = self.cur.fetchall()
		#cvvb = ''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',linke_url))).split('/')
		#import pdb;pdb.set_trace()
		#if len(cvvb[1]) == 2:
		final_k, final_k1 = ['']*2
		for indexc, cle in enumerate([linke_url, new_on[0][0]]):
			#urlclear = linke_url
			if cle == new_on[0][0] and '?' in cle: cle = cle.split('?')[0].strip()
			urlclear = cle
			if 'http:' in urlclear: urlclear = urlclear.replace('http:','https:')
			if 'id.www' in  urlclear: urlclear = urlclear.replace('id.www','https://www')
			if 'www.linkedin.com' and 'https:' not in urlclear: urlclear = urlclear.replace('www.','https://www')
			if urlclear.startswith('linkedin.com'): urlclear = urlclear.replace('linkedin.com','https://www.linkedin.com')
			if 'https:' not in urlclear:
			    urlclear = re.sub('(\D+)\.linkedin.com','https://www.linkedin.com', urlclear)
			urlclear = re.sub('https://(.*?).linkedin.com/','https://www.linkedin.com/',urlclear)
			if not urlclear.startswith('https://www.linkedin.com') and crawl_status!=10: urlclear = ''.join(re.findall('.*(https://.*)', urlclear))
			urlclear = urlclear.strip('"').strip().strip("'").strip().strip('/').strip()

			if urlclear.endswith('/en'): urlclear = urlclear[:-3]
			if urlclear.endswith('/fr'): urlclear = urlclear[:-3]
			cv = ''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',urlclear))).split('/')[::-1]
			cv[0] = cv[0].zfill(3)
			cv[1] = cv[1].zfill(3)
			if cv[-1] == '0': del cv[-1]
			if '/pub/' in urlclear: urlclear = ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',urlclear)),'-',''.join(cv)))
			if indexc !=0: final_k = urlclear
			else: final_k1 = urlclear
		self.cur.execute(self.updateqry1%(final_k,sk))
		print final_k1.encode('utf-8')
		print final_k.encode('utf-8')
		file("date","ab+").write("%s\n" %final_k1.encode('utf-8'))
		file("date","ab+").write("%s\n" %final_k.encode('utf-8'))
		#print '*******************'
		#import pdb;pdb.set_trace()	
		#self.cur.execute(self.updateqry1%(urlclear,sk))	
		#new_url =  ( '%s%s%s%s'%('https://www.linkedin.com/in/',''.join(re.findall('https://www.linkedin.com/pub/(.*?)/.*',rec[0])),'-',''.join(''.join(filter(None,re.split('https://www.linkedin.com/pub/.*?/(.*)',rec[0]))).split('/')[::-1])))
		#print (self.updateqry1%(new_url,rec[1])).encode('utf-8')
		#self.cur.execute(self.updateqry1%(new_url,rec[1]))

def main():
        obj = Lixlspub()
        obj.send_xls()
if __name__ == '__main__':
        main()

