import MySQLdb
import json
class McmasterScript(object):

    def __init__(self):
        self.conn = MySQLdb.connect(db = 'MCMASTER', user='root', host='localhost', passwd='root', charset="utf8", use_unicode=False)
        self.cur = self.conn.cursor()
	self.query = 'select sk, title, category, description, image_url, price, item_data, reference_url, main_link from mcmaster limit 10'
	self.main()

    def main(self):
	self.cur.execute(self.query)
	rows = self.cur.fetchall()
	self.cur.close()
	self.conn.close()
	dict_ = {'result':[]} 
	for row in rows:
	    id_, title, category, description, image, price, item_data, url, main_link = row 
	    if image:
	        image = 'http://www.mcmaster.com%s'%image
	    try:	   
	    	item_ = {'title' : title.decode("ascii","ignore").encode('ascii'), 'description' : description.decode("ascii","ignore").encode('ascii'), 'image' : image.decode("ascii","ignore").encode('ascii'), 'price' : price.decode("ascii","ignore").encode('ascii'),  'url' : url.decode("ascii","ignore").encode('ascii'), 'main_link' : main_link.decode("ascii","ignore").encode('ascii')}
		for key,value in json.loads(item_data).iteritems():
			item_.update({key : value.decode("ascii","ignore").encode('ascii')})
	    except:
	    dict_['result'].append({'id' : id_, 'meta' : item_})
	with open('data.json', 'w') as outfile:
		json.dump(dict_, outfile)
if __name__ == '__main__':
        McmasterScript()

