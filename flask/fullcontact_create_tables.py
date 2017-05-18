from fullcontact_table_schemas import TABLES
from linkedin_functions import *

class FullCreateschemas(object):

    def __init__(self, *args, **kwargs):
        self.main()

    def get_cursor(self):
        conn = MySQLdb.connect(host='localhost', user="root", passwd="hdrn59!")
        cursor = conn.cursor()
        return conn, cursor

    def create_tables(self, db_name, cursor):
        try:
            cursor.execute('USE %s;' % db_name)
            query = "ALTER DATABASE " + db_name + " CHARACTER SET utf8;"
            cursor.execute(query)
            for ttype, table in TABLES.iteritems():
                try:
                    cursor.execute(table)
                except:
                    print "Table: ", table
                    traceback.print_exc()
            print "New Database '%s' Created Successfully." % (db_name)
        except:
            traceback.print_exc()

    def main(self):
        db_name = options.db_name
        conn, cursor = self.get_cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s;' % (db_name))
        self.create_tables(db_name, cursor)

if __name__ == '__main__':
        parser = optparse.OptionParser()
        parser.add_option('-d', '--db-name', default='', help = 'db_name')
        (options, args) = parser.parse_args()
        FullCreateschemas(options)


