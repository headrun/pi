from linkedin_voyager_functions import *
from ConfigParser import SafeConfigParser
_cfg = SafeConfigParser()
_cfg.read('linkedin_voyager.cfg')
from datetime import date, timedelta

class Licrawlaws(object):

        def get_cursor_dbs(self, username, hostname, db_name, password):
                self.con = MySQLdb.connect(user = _cfg.get('aws', 'user'),
                host = hostname, db = db_name,
                passwd= password, use_unicode=True)
                self.cur  = self.con.cursor()
                self.con.set_character_set('utf8')
                self.cur.execute('SET NAMES utf8;')
                self.cur.execute('SET CHARACTER SET utf8;')
                self.cur.execute('SET character_set_connection=utf8;')
                return self.cur, self.con

        def __init__(self, options):
                self.modified_at = options.modified_at
                self.cur, self.con = self.get_cursor_dbs( _cfg.get('aws', 'user'), _cfg.get('aws', 'host'), _cfg.get('aws', 'db_name'), _cfg.get('aws', 'awspasswd'))
                self.con1, self.cur1 = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
                self.cur1.execute('select now()')
                aws_date = self.cur1.fetchall()[0][0]
                aws_date = str(aws_date.date())
                start_date = aws_date+' '+'03:30:00'
                end_date = aws_date+' '+'18:30:00'
                self.query = 'insert into linkedin_crawl(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values(%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at=now(), content_type=%s, crawl_status=0,meta_data=%s'
                self.query2 = 'select %s from %s where %s between "%s" and "%s" ' % (
                   _cfg.get('aws', 'input_fields'),  _cfg.get('aws', 'input_table'), _cfg.get('aws', "where_field"),start_date, end_date)
                self.main()

        def __del__(self):
                close_mysql_connection(self.con, self.cur)
                close_mysql_connection(self.con1, self.cur1)

        def main(self):
                total_connection_records = fetchall(self.cur, self.query2)
                counter = 0
                for tocr in total_connection_records:
                        meta_date_from_browse = {}
                        id_, url_, created_date_ = tocr
                        try : meta_date_from_browse.update(
                                {"linkedin_url": url_, 'id': id_, 'created_date': str(created_date_.date())})
                        except :
                             meta_date_from_browse.update(
                                {"linkedin_url": url_, 'id': id_, 'created_date': created_date_})

                        sk = md5(url_)
                        crawl_status = 0
                        try:
                                values = (sk,  MySQLdb.escape_string(normalize(url_)), 'linkedin', crawl_status,  MySQLdb.escape_string(
                                          json.dumps(meta_date_from_browse).encode('utf-8')), 'linkedin',  MySQLdb.escape_string(json.dumps(meta_date_from_browse).encode('utf-8')))
                                counter += 1
                                self.cur1.execute(self.query, values)
                        except Exception as e:
                            logging.debug(e.message)
if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option(
            '-m', '--modified_at', default='', help='modified_at')
        (options, args) = parser.parse_args()
        Licrawlaws(options)
