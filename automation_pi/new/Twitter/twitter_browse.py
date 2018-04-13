import collections
from twitter_constants import *

class TwitterBrowse(object):

    def __init__(self):

        self.con = pymysql.connect(db=db_name,
                      user=db_user,
                      password=db_passwd,
                      charset="utf8mb4",
                      host=db_host)
 
        self.cur  = self.con.cursor() 
        self.insert_query = insert_query

    def main(self):
                dup_list = []
                email_id = '' 
                import pdb;pdb.set_trace()
                with open('20180411_twitter_urls.txt', 'r') as f:
                    rows = f.readlines()
                    for row in rows:
                        if ',' in row :
                            data= row.split(',')
                            screen_url = data[0]
                            if "twitter.com" in screen_url and "gmail.com" not in screen_url : name = screen_url.split('/')[-1].strip('\n').strip().replace('\r','')
                            if "twitter.com" not in screen_url and "gmail.com" not in screen_url : name = screen_url.split('/')[-1].strip('\n').strip().replace('\r','')
                            elif 'gmail.com' in screen_url : email_id = screen_url
                            else : email_id =  data[1]

                        else :
                            name = row.strip('\n').strip().replace('\r','')
                            if 'gmail.com' in name : print "Email id is given in place of screen name"
                            screen_url = "https://twitter.com/"+str(name).replace('@','')

                        dup_list.append(screen_url)
                        vals = (str(name),str(screen_url),'keepup','Twitter','related_type',0,str(email_id))
                        if screen_url : 
                            self.cur.execute(self.insert_query,vals)
                            self.con.commit()
                print([item for item, count in collections.Counter(dup_list).items() if count > 1])
    def __del__(self):
        self.con.close()
        self.cur.close()


if __name__ == '__main__':
    TwitterBrowse().main()

