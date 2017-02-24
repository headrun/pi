import xlwt
import MySQLdb
import json
import datetime
import re

class Lixlsfile(object):

    def __init__(self, *args, **kwargs):
        self.row_count = 1
        self.selectqry = 'select sk , product_id, name, reviewed_by, reviewed_on, review, review_url, review_rating, aux_info from CustomerReviews'
        self.excel_file_name = 'reviews_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp', 'star_rating', 'count_views', 'count_likes', 'count_comments', 'count_replies', 'count_helpful', 'location', 'flake_flag', 'authors_no_of_reviews', 'review url', 'author_url', 'review_text']
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)

    def create_cursor(self, db_, user_, pswd_, host_):
        try:
            con = MySQLdb.connect(db   = db_,
                  user                      = user_,
                  passwd                    = pswd_,
                  charset                   = "utf8",
                  host                      = host_,
                  use_unicode               = True)
            cur = con.cursor()
        except:
            pass
        return con, cur

    def close_sql_connection(self, conn, cursor):
        if cursor: cursor.close()
        if conn: conn.close()

    def send_xls(self):
        #dbs = ['MOUTHSHUT', 'CONSUMERCOMPLAINTS']
        dbs = ['MOUTHSHUT']
        for db in dbs:
            con2_,cur2_ = self.create_cursor(db, 'root','hdrn59!','localhost')
            cur2_.execute(self.selectqry)
            records = cur2_.fetchall()
            for record in records:
                sk , product_id, name, reviewed_by, reviewed_on, review, review_url, review_rating, aux_info = record
                aux_infof = {}
                useful = ''
                try:
                    aux_infof = re.sub('"useful": "(.*\})",', '', aux_info)
                    aux_infof = json.loads(aux_infof.replace('\\',''))
                    try: useful = re.findall('"useful": "(.*\})"', aux_info)[0]
                    except: pass
                except: pass
                keywor = aux_infof.get('browse','').replace('%20',' ').replace('+','')
                views = aux_infof.get('views', '')
                likes = aux_infof.get('likes', '')
                comment = aux_infof.get('no_comments','')
                if not comment: comment = aux_infof.get('comment','')
                if not comment: comment = aux_infof.get('no_comments:','')
                location = aux_infof.get('location','')
                authorurl = aux_infof.get('author_url','')
                revits = aux_infof.get('post_title','')
                noofrev = aux_infof.get('no_of_reviews','')
                comment = ''.join(re.findall('\d+',comment))
                noofrev = ''.join(re.findall('\d+',noofrev))
                views =  ''.join(re.findall('\d+',views))
                fake = aux_infof.get('fake','')
                values = [db.lower(), keywor, name, review, reviewed_by, str(reviewed_on), review_rating, views, likes, comment, '', useful,  location, fake, noofrev, review_url, authorurl, revits]
                print values
                for col_count, value in enumerate(values):
                    self.todays_excel_sheet1.write(self.row_count, col_count, value)
                self.row_count = self.row_count+1
            self.close_sql_connection(con2_, cur2_)
        self.todays_excel_file.save(self.excel_file_name)

def main():
        obj = Lixlsfile()
        obj.send_xls()
if __name__ == '__main__':
        main()


