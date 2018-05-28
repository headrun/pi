'''import MySQLdb

conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '', db = 'urlqueue_dev', charset = 'utf8', use_unicode = True)
cur =  conn.cursor()
qry = "select doctor_id from practo_duplicate_urls group by reference_url having count(*) < 10 and reference_url!='https://www.practo.com/chennai/doctors?page=769'" 
cur.execute(qry)
ids = cur.fetchall()
for id_ in ids:
    id_ = id_[0]
    
    qry1 = 'delete from practo_duplicate_urls where doctor_id = %s'%id_
    cur.execute(qry1)
    conn.commit()'''
    
