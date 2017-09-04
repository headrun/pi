from linkedin_voyager_functions import *
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from  dict_ids import dics
class Companysurlup(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		#self.qu1 = 'select meta_data from linkedin_crawltable where url = "%s"'
		self.qu1 =  "select member_id from linkedin_voyager_profiles1 where profile_url = '%s'"

	def main(self):
		dicts_of_ids = {}
		with open('id_mapping_for_candidates.csv') as f:
			r = csv.reader(f)
			for line in r:
				if line[0] == 'url':
					continue
				recs = fetchmany(self.cur, self.qu1 % line[0])
				if recs:
					print recs
					dicts_of_ids.update({normalize(recs[0][0]):line[1]})
		file("dict_ids_new.py","ab+").write("%s\n" % dicts_of_ids)
			
					

if __name__ == '__main__':
	Companysurlup().main()
		
		
		
