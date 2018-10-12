import MySQLdb
import json
def main():

	conn = MySQLdb.connect(db='MCMASTER',user='root',passwd='root', host='localhost', use_unicode=True)
        cur = conn.cursor()
	conn1 = MySQLdb.connect(db='urlqueue_dev',user='root',passwd='root', host='localhost', use_unicode=True)
        cur1 = conn1.cursor()
	qry = 'select sk from urlqueue_dev.mcmaster_crawl'
	cur1.execute(qry)
        sks = cur1.fetchall()
	sk_list = []
	for sk_ in sks:
  	    sk_list.append(sk_[0].encode('utf8'))
	query = 'select sk, category,price,reference_url,main_link from mcmaster where title="" AND sk not in {0}'
	cur.execute(query.format(tuple(sk_list)))
	rows = cur.fetchall()
	cur.close()
	conn.close()
	for row in rows:
		sk, category,price,reference_url,main_link = row
		url = 'https://www.mcmaster.com/#%s'%sk
		meta_data = {"product_id": sk, "price": price, "constructed_url": main_link, "main_cat": category, "ref_url": url}
		query1 = 'insert into mcmaster_crawl(sk, url, crawl_type, content_type, related_type, crawl_status, meta_data, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, now(), now())'
		values = (sk, reference_url,'keepup','data','','0',json.dumps(meta_data))
		cur1.execute(query1,values)
	cur1.close()
	conn1.close()

if __name__ == "__main__":
    main()
