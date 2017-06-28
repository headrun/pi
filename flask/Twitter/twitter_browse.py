import collections
from twitter_constants import *

class TwitterBrowse(object):

    def __init__(self):

        self.con = MySQLdb.connect(db=db_name,
                      user=db_user,
                      passwd=db_passwd,
                      charset="utf8",
                      host=db_host,
                      use_unicode=True)
 
        self.cur  = self.con.cursor() 
        self.insert_query = insert_query

    def main(self):
                dup_list = [] 
                with open('twitter_ash.txt', 'r') as f:
                    rows = f.readlines()
                    print len(rows)
                    for row in rows:
                        #import pdb;pdb.set_trace()
                        email_id, screen_url = row.strip('\n').strip().replace('\r','').split(',')
                        if not screen_url: continue
                        name = screen_url.split('/')[-1].strip()
                        dup_list.append(screen_url)
                        print [item for item, count in collections.Counter(dup_list).items() if count > 1]

                        vals = (str(name),str(screen_url),'keepup','Twitter','related_type',0,str(email_id))
                        if screen_url and  email_id : 
                            self.cur.execute(self.insert_query,vals)
                            self.con.commit()
    def __del__(self):
        self.con.close()
        self.cur.close()


if __name__ == '__main__':
    TwitterBrowse().main()

