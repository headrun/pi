
import itertools

from juicer.utils import *
from juicer.items import *
 
class CleanBrowse(JuicerSpider):
    name = 'clean_address_browse'
  
    #start_urls = ['https://docs.google.com/spreadsheets/d/1lSkO9fMsrcfrTtVuB5DRtYKlsbbyBfRXSAHw3JSzHdg/edit']
    start_urls = ['https://docs.google.com/spreadsheets/d/104iijFYtMvApZFK5qafLr4hQJQxkJrgr2zeTq6qjPaw/edit']
     

    def __init__(self, *args, **kwargs):
        super(CleanBrowse, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(db  = 'address_components',
                      user        = 'root',
                      passwd      = 'root',
                      charset     = "utf8",
                      host        = 'localhost',
                      use_unicode = True)
        self.cur = self.con.cursor()
        self.select_qry = 'select distinct sk from Clean_address where status = "ZERO_RESULTS" limit 100'
        
    def parse(self, response):
        sel = Selector(response)
        rows = self.get()

	for zero in rows:
		count = 0
		s_no, key_value, old_address, new_address, localityname, location3, city, state, code, country = zero
                if key_value == 283 :
	            lists = [[localityname, location3, city], [location3, city]]
		    for main in lists:
	                permutes = list(itertools.permutations([state, code, country]))
	                for temp in permutes:
			    count += 1
			    address = ','.join([i for i in itertools.chain(*[main, temp])])
                            #print address
			    url =  "http://maps.googleapis.com/maps/api/geocode/json?sensor=true&address=<%s>" %address
			    sk = md5(url+str(count))
                            print address,sk
			    self.get_page("address_clean_terminal",url,sk,meta_data={'address':address,'new_address':new_address,'old_address':old_address,'s_no':s_no,'key_value':key_value})
	

    def get(self):
        self.cur.execute(self.select_qry)
	records = self.cur.fetchall()
	self.select_permutations_qry = 'select sk,key_value,old_address,address_new,localityname, location3, city, state, code, country from Clean_address_permutations where sk in %s' % str(tuple([int(e) for l in records for e in l]))
	self.cur.execute(self.select_permutations_qry)
	rows = self.cur.fetchall()
	return rows

        

