from linkedin_functions import *

class Mahareracsv(object):
    def __init__(self, *args, **kwargs):
        self.con, self.cur = get_mysql_connection('localhost', 'MAHARERA', 'root') 
        self.columns_query = 'SELECT COLUMN_NAME FROM information_schema.columns where table_schema= "MAHARERA" and table_name = "%s"'
        self.main()

    def main(self):
        tables_qry = "show tables"
        self.cur.execute(tables_qry)
        tables = self.cur.fetchall()
        for table_name in tables :
            table_nme = table_name[0]
            self.cur.execute(self.columns_query%table_nme)
            headers = []
            headers_list =  self.cur.fetchall()
            for header in headers_list :
                headers.append(header[0])
            excel_file_name = 'Mahaonline_%s_%s.csv'%(table_nme,datetime.datetime.now().date())
            oupf = open(excel_file_name, 'wb+')
            todays_excel_file  = csv.writer(oupf)
            todays_excel_file.writerow(headers)
            select_qry = 'select * from %s' % table_nme
            self.cur.execute(select_qry)
            rows = self.cur.fetchall()
            for row in rows:
                todays_excel_file.writerow(row)

if __name__ == '__main__':
    Mahareracsv()

