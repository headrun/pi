import os
from twitter_constants import *


class Login(object):

    def __init__(self):

        self.con = MySQLdb.connect(db=db_name,
                      user=db_user,
                      passwd=db_passwd,
                      charset="utf8",
                      host=db_host,
                      use_unicode=True)

        self.cur = self.con.cursor()
        self.select_qry = select_qry
        self.update_qry = upd_qry

    def main(self):
        self.cur.execute(self.select_qry)
    
        rows = self.cur.fetchall()
        for row in rows:
            args_name,screen_url,email_id=row
            cmd = 'python tweet_analyzer.py -n %s -e %s'%(args_name,email_id)
            
            self.cur.execute(self.update_qry % args_name)
            self.con.commit()
            os.system(cmd)

    def __del__(self):
        self.con.close()
        self.cur.close()


if __name__ == '__main__':
    Login().main()

