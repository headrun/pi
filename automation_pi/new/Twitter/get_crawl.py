import os
from twitter_constants import *
import pymysql


class Login(object):

    def __init__(self):

        self.con = pymysql.connect(db=db_name,
                      user=db_user,
                      password=db_passwd,
                      charset="utf8mb4",
                      host=db_host)

        self.cur = self.con.cursor()
        self.select_qry = select_qry
        self.update_qry = upd_qry

    def main(self):
        self.cur.execute(self.select_qry)
        rows = self.cur.fetchall()
        for row in rows:
            args_name,screen_url,email_id=row
            #import pdb;pdb.set_trace()
            if email_id : cmd = 'python tweet_analyzer.py -n %s -e %s'%(args_name,email_id)
            else : cmd = 'python tweet_analyzer.py -n %s'%(args_name)
            self.cur.execute(self.update_qry % args_name)
            self.con.commit()
            os.system(cmd)

    def __del__(self):
        self.con.close()
        self.cur.close()


if __name__ == '__main__':
    Login().main()

