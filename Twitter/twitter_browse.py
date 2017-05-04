import MySQLdb

class TwitterBrowse(object):
    def __init__(self):
        self.con = MySQLdb.connect(db='TWITTER',
                              user='root', 
                              passwd='hdrn59!',
                              charset="utf8", 
                              host='localhost',    
                              use_unicode=True)
        self.cur = self.con.cursor()
        self.insert_query = 'insert into twitter_crawl(sk, url, crawl_type, content_type,related_type,crawl_status,meta_data,created_at,modified_at)values(%s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at = now()'
    def main(self):
                with open('Twitter_cn.txt', 'r') as f:
                    rows = f.readlines()
                    for row in rows:
                        email_id, screen_url = row.strip('\n').strip().replace('\r','').split(',')
                        if not screen_url: continue
                        name = screen_url.split('/')[-1].strip()
                        vals = (str(name),str(screen_url),'keepup','Twitter','related_type',0,str(email_id))
                        self.cur.execute(self.insert_query,vals)
                        self.con.commit()
                        
    def __del__(self):
        self.con.close()
        self.cur.close()


if __name__ == '__main__':
    TwitterBrowse().main()

