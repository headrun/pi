from linkedin_voyager_db_operations import *
from db_qry2 import*
import ast

class Picsdenormalization(object):

    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection(DB_HOST, 'CRAWL_AUTOMATION', '')
        self.file_dirs = os.path.join(os.getcwd(), 'OUTPUT')
        self.QUERY_FILES_DIR = os.path.join(self.file_dirs, 'processing')
        self.QUERY_FILES_CRAWLOUT_DIR = os.path.join(
            self.file_dirs, 'crawl_out')
        self.tables_file = self.get_tables_file()
        self.tables_file1 = self.get_tables_file1()
        self.sk = options.sk
        self.inner_dict = {}
        self.main()

    def __del__(self):
        self.con.close()
        self.cur.close()

