import os
import MySQLdb

class Login(object):

    def __init__(self):
        self.con = MySQLdb.connect(db='TWITTER',
                              user='root',
                              passwd='hdrn59!',
                              charset="utf8",
                              host='localhost',
                              use_unicode=True)
        self.cur = self.con.cursor()
        self.select_qry = 'select  sk,url,meta_data from twitter_crawl where crawl_status = 0 limit 1'
        self.update_qry = 'update twitter_crawl set crawl_status=9 where sk= "%s"'

    def main(self):
        self.cur.execute(self.select_qry)
        rows = self.cur.fetchall()
        for row in rows:
            args_name,screen_url,email_id=row
            cmd = 'python tweet_analyser.py -n %s -e %s'%(args_name,email_id)
            self.cur.execute(self.update_qry % args_name)
            self.con.commit()
            os.system(cmd)

    def __del__(self):
        self._db_connection.close()
        self._db_cur.close()


if __name__ == '__main__':
    Login().main()

