import MySQLdb


class Login(object):

    def __init__(self):
        self.con = MySQLdb.connect(db='FACEBOOK',
                      user='root',
                      passwd='root',
                      charset="utf8",
                      host='localhost',
                      use_unicode=True)

        self.cur = self.con.cursor()
        self.select_qry1 = 'select sk from linkedin_meta' 
        self.select_qry2 = 'select exp_duration  from linkedin_experiences where profile_sk ="%s"'
        self.insert_qry = 'insert into experiences_count(profile_sk,exp_duration,created_at,modified_at) values (%s, %s,now(),now())on duplicate key update modified_at = now()'

    def main(self):
        self.cur.execute(self.select_qry1)
        rows = self.cur.fetchall()
        for row in rows:
            sk = row
            sk = sk[0]
            self.cur.execute(self.select_qry2%sk)
            count = self.cur.fetchall()
            for data in count :
                exp = data
                exp = exp[0]
                if 'years' in exp :
                    exp_ = exp.split('years')[0]
                    if exp_ > 2:
                        print sk , exp_
                        values = (sk,exp)
                        self.cur.execute(self.insert_qry,values)

    def __del__(self):
        self.con.close()
        self.cur.close()
 

if __name__ == '__main__':
    Login().main()

