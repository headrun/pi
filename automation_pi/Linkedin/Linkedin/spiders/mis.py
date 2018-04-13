import  MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(db   ='FACEBOOK', host = 'localhost', charset="utf8", use_unicode=True, user = 'root', passwd = 'root')
cur = conn.cursor()
x=[]
select_query = 'select url from linkedin_crawl where date(created_at)>="2018-02-21"'
cur.execute(select_query)
data = cur.fetchall()
ll = []
for da in data:
        ll.append(da[0])

with open('linkedin_26.txt', 'r') as f: rows = f.readlines()
for row in rows:
	row = row.replace('\n','')
        if row in ll:
                continue
        else:
                file("missingkeyword1.html","ab+").write("%s" % row)

