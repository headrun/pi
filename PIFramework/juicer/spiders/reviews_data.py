import xlwt
import MySQLdb
import json
import datetime
import re
import sys
import optparse

class Lixlsfile(object):

    def __init__(self, options):
        self.db_list     = options.db_name
        self.row_count = 1
        self.db_list = self.db_list.split(',')
        self.commentqry = 'select sk ,review_sk, comment_name, comment_by, comment_on, comment, comment_votes, aux_info from Comments where review_sk ="%s"'
        self.selectqry = 'select sk , product_id, name, reviewed_by, reviewed_on, review, review_url, review_rating, aux_info from CustomerReviews'
        self.selectqry1 = 'select sk , product_id, name, reviewed_by, reviewed_on, review, category,  review_url, review_rating, aux_info from CustomerReviews'
        self.excel_file_name = 'reviews_%s.xls'%str(datetime.datetime.now().date())
        self.todays_excel_file = xlwt.Workbook(encoding="utf-8")
        self.todays_excel_sheet1 = self.todays_excel_file.add_sheet("sheet1")
        header_params = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp', 'star_rating', 'count_views', 'count_likes', 'count_comments', 'count_replies', 'count_helpful', 'location', 'flake_flag', 'authors_no_of_reviews', 'review url', 'author_url', 'review_text']
        header_params1 = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp','category', 'location', 'review url', 'author_url', 'author_email', 'author_contact_number', 'author_address']
        header_params2 = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp','count_replies', 'count_views', 'post_title', 'author_url','review url', 'forum_url', 'forum_name', 'user_title','last_post_author', 'last_post_author_url','last_post_date']
        header_params3 = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp',  'post_title', 'author_url','review url','location','author_location','author_since_date']
        header_params4 = ['source', 'search_keyword', 'title', 'post_text', 'author', 'post_timestamp', 'review_rating', 'count_comments', 'location','category', 'review url', 'author_url', 'review_text', 'comment','comment_by','comment_on','comment_votes','no_of_votes','aggregate_rating_value', 'address','author_location','author_since_date', 'author_reputation_points','author_no_of_comments','author_no_of_complaints','author_location','author_badge_bronze','author_badge_silver', 'author_badge_gold']
        header_params5 = ['source', 'search_keyword', 'title', 'post_text', 'author','post_timestamp', 'review_rating', 'location','review url','author_url','product_score']
        header_params6 = ['source', 'search_keyword', 'title', 'post_text', 'author','post_timestamp', 'no_of_comments', 'category', 'country', 'state', 'city', 'review url']
        if 'INDIA' in ''.join(self.db_list):
            header_params = header_params1
        elif 'COURT' in ''.join(self.db_list):
            header_params =  header_params2
        elif  ''.join(self.db_list) == "COMPLAINTBOARD":
            header_params =  header_params3
        elif ''.join(self.db_list) == "COMPLAINTSBOARD":
            header_params =  header_params4
        elif ''.join(self.db_list) == "CONSUMERDADDY":
            header_params =  header_params5
        elif ''.join(self.db_list) == "COMPLAINTLISTS":
            header_params =  header_params6
        for i, row in enumerate(header_params):
            self.todays_excel_sheet1.write(0, i, row)
        self.main()

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

    def restore(self, text):
        try:
            text = text.replace('<>#<>','"').replace("<>##<>","'").replace('###',',').replace('\\','')
            if '<>' in text:
                text = set(text.split('<>'))
                text = '<>'.join(text)
        except: text = text
        return text

    def replacefun(self, text):
        text = text.replace('"','<>#<>').replace("'","<>##<>").replace(',','###')
        return text

    def send_xls(self):
        dbs = self.db_list
        for db in dbs:
            con2_,cur2_ = self.create_cursor(db, 'root','hdrn59!','localhost')
            if 'INDIA' in db or 'COMPLAINTSBOARD' in db or 'COMPLAINTLISTS' in db:
                cur2_.execute(self.selectqry1)
            else:
                cur2_.execute(self.selectqry)
            records = cur2_.fetchall()
            for record in records:
                if 'INDIA' in db or 'COMPLAINTSBOARD' in db or 'COMPLAINTLISTS' in db:
                    sk , product_id, name, reviewed_by, reviewed_on, review, category, review_url, review_rating, aux_info = record
                else: sk , product_id, name, reviewed_by, reviewed_on, review, review_url, review_rating, aux_info = record
                recordscomment1 = [('sk' ,'review_sk', 'comment_name', 'comment_by', 'comment_on', 'comment', 'comment_votes', 'aux_info')]
                if 'COMPLAINTSBOARD' in db:
                    cur2_.execute(self.commentqry%sk)
                    recordscomment = cur2_.fetchall()
                    if not recordscomment:
                        recordscomment = recordscomment1
                if sk:
                    aux_infof = {}
                    useful = ''
                    try:
                        aux_infof = re.sub('"useful": "(.*\})",', '', aux_info)
                        aux_infof = json.loads(aux_infof.replace('\\',''))
                        try: useful = re.findall('"useful": "(.*\})"', aux_info)[0]
                        except: pass
                    except:
                        pass
                    keywor = self.restore(aux_infof.get('browse','').replace('%20',' ').replace('+',' ').replace('-',' '))
                    views = self.restore(aux_infof.get('views', ''))
                    likes = self.restore(aux_infof.get('likes', ''))
                    comment = self.restore(aux_infof.get('no_comments',''))
                    if not comment: comment = self.restore(aux_infof.get('no_of_comments',''))
                    if not comment: comment = self.restore(aux_infof.get('comment',''))
                    if not comment: comment = self.restore(aux_infof.get('no_comments:',''))
                    location = self.restore(aux_infof.get('location',''))
                    authorurl = self.restore(aux_infof.get('author_url',''))
                    last_post_date = self.restore(aux_infof.get('last_post_date',''))
                    if not authorurl: authorurl = self.restore(aux_infof.get('author_profile',''))
                    revits = self.restore(aux_infof.get('post_title',''))
                    email = self.restore(aux_infof.get('email',''))
                    address = self.restore(aux_infof.get('address',''))
                    contact_num = self.restore(aux_infof.get('contact_no',''))
                    noofrev = self.restore(aux_infof.get('no_of_reviews',''))
                    comment = ''.join(re.findall('\d+',comment))
                    noofrev = ''.join(re.findall('\d+',noofrev))
                    views =  ''.join(re.findall('\d+',views))
                    fake = self.restore(aux_infof.get('fake',''))
                    forum_title = self.restore(aux_infof.get('forum_title',''))
                    forum_replies = self.restore(aux_infof.get('forum_replies',''))
                    forum_views = self.restore(aux_infof.get('forum_views',''))
                    last_post_author_name = self.restore(aux_infof.get('last_post_author_name',''))
                    last_post_author_url = self.restore(aux_infof.get('last_post_author_url',''))
                    forum_url = self.restore(aux_infof.get('forum_url',''))
                    forum_name = self.restore(aux_infof.get('forum_name',''))
                    user_title = self.restore(aux_infof.get('author_title',''))
                    author_location = self.restore(aux_infof.get('author_location',''))
                    author_since_date = self.restore(aux_infof.get('author_since_date',''))
                    aggregate_rating_count = self.restore(aux_infof.get('aggregate_rating_count',''))
                    aggregate_rating_value = self.restore(aux_infof.get('aggregate_rating_value',''))
                    author_reputation_points = self.restore(aux_infof.get('author_reputation_points',''))
                    author_badge_bronze = self.restore(aux_infof.get('badge-bronze',''))
                    author_badge_silver = self.restore(aux_infof.get('badge-silver',''))
                    author_badge_gold = self.restore(aux_infof.get('badge-gold',''))
                    author_no_of_comments = self.restore(aux_infof.get('author_no_of_comments',''))
                    author_no_of_complaints = self.restore(aux_infof.get('author_no_of_complaints',''))
                    rated_score = self.restore(aux_infof.get('rated_score',''))
                    product_score = self.restore(aux_infof.get('product_score',''))
                    review_on = self.restore(aux_infof.get('review_on',''))
                    country = self.restore(aux_infof.get('country',''))
                    city = self.restore(aux_infof.get('city',''))
                    state = self.restore(aux_infof.get('state',''))
                    if db =='COMPLAINTSBOARD':
                        keyword = self.check_keyword(review, name)
                        for recorcom in recordscomment:
                            skc ,review_skc, comment_namec, comment_byc, comment_onc, commentc, comment_votesc, aux_infoc = recorcom
                            keywordc = ''
                            if not keyword:
                                if 'apollo hospitals' in commentc.lower():
                                    keyword = 'Apollo hospitals'
                                    keywordc = 'check'

                            if keywor:
                                    if keywordc: keyword = ''
                                    if skc == 'sk': skc = review_skc= comment_namec=comment_byc = comment_onc = commentc = comment_votesc = ''
                                    comment_votesc =  ''.join(re.findall('\d+',comment_votesc))
                                    values = [db.lower(),keywor,name,review,reviewed_by,str(reviewed_on),review_rating,comment, location, category, review_url, authorurl, revits, commentc, comment_byc, str(comment_onc), comment_votesc, aggregate_rating_count, aggregate_rating_value, address,author_location, author_since_date, author_reputation_points, author_no_of_comments, author_no_of_complaints, author_location, author_badge_bronze, author_badge_silver, author_badge_gold]
                                    for col_count, value in enumerate(values):
                                        self.todays_excel_sheet1.write(self.row_count, col_count, value)
                                    self.row_count = self.row_count+1
                    else:
                        if 'INDIA' in db:
                            values = [db.lower(), keywor, name, review, reviewed_by, str(reviewed_on), category, location, review_url, authorurl, email, contact_num, address]
                        elif db == 'CONSUMERDADDY':
                            values = [db.lower(), keywor, name, review, reviewed_by, review_on, rated_score, location,review_url, authorurl, product_score]
                        elif db == "COMPLAINTLISTS":
                            values = [db.lower(), keywor, name, review, reviewed_by, str(reviewed_on), comment, category, country, city, state, review_url]
                        elif  db == 'COMPLAINTBOARD':
                            keyword = self.check_keyword(review, name)
                            if not keyword: continue
                            values = [db.lower(), keywor, name, review, reviewed_by, str(reviewed_on), revits, authorurl, review_url, location, author_location, author_since_date]
                        elif 'COURT' in db:
                            values = [db.lower(), keywor, forum_title, review, reviewed_by, str(reviewed_on),forum_replies, forum_views,  name, authorurl, review_url,forum_url, forum_name, user_title, last_post_author_name, last_post_author_url, last_post_date]
                        else:
                            values = [db.lower(), keywor, name, review, reviewed_by, str(reviewed_on), review_rating, views, likes, comment, '', useful,  location, fake, noofrev, review_url, authorurl, revits]
                        for col_count, value in enumerate(values):
                            self.todays_excel_sheet1.write(self.row_count, col_count, value)
                        self.row_count = self.row_count+1
            self.close_sql_connection(con2_, cur2_)
        self.todays_excel_file.save(self.excel_file_name)

    def check_keyword(self, review, name):
        keyword =  ''
        if 'apollo hospital' in review.lower(): keyword = 'Apollo hospital'
        if 'apollo' in name.lower() and  'hospital' in name.lower(): keyword = 'Apollo hospital'
        return keyword

    def main(self):
        self.send_xls()

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        (options, args) = parser.parse_args()
        Lixlsfile(options)


