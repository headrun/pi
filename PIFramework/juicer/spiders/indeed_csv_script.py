import csv
import MySQLdb
import datetime
class IndeedCsvScript():

    def __init__(self):
	self.conn = MySQLdb.connect(db='INDEED', user='root', host='localhost', passwd='root', charset="utf8", use_unicode=False)
        self.cur = self.conn.cursor()
	self.headers = ['Keyword','Url','Total_job_cnt','Job1_title','Job1_Company_Name','Job1_rating','Job1_Reviews','Job1_Location','Job1_Description','Job1_Salary','Job1_Posted','Job1_url','Job2_title','Job2_Company_Name','Job2_rating','Job2_Reviews','Job2_Location','Job2_Description','Job2_Salary','Job2_Posted','Job2_url','Job3_title','Job3_Company_Name','Job3_rating','Job3_Reviews','Job3_Location','Job3_Description','Job3_Salary','Job3_Posted','Job3_url','Job4_title','Job4_Company_Name','Job4_rating','Job4_Reviews','Job4_Location','Job4_Description','Job4_Salary','Job4_Posted','Job4_url','Job5_title','Job5_Company_Name','Job5_rating','Job5_Reviews','Job5_Location','Job5_Description','Job5_Salary','Job5_Posted','Job5_url','Job6_title','Job6_Company_Name','Job6_rating','Job6_Reviews','Job6_Location','Job6_Description','Job6_Salary','Job6_Posted','Job6_url','Job7_title','Job7_Company_Name','Job7_rating','Job7_Reviews','Job7_Location','Job7_Description','Job7_Salary','Job7_Posted','Job7_url','Job8_title','Job8_Company_Name','Job8_rating','Job8_Reviews','Job8_Location','Job8_Description','Job8_Salary','Job8_Posted','Job8_url','Job9_title','Job9_Company_Name','Job9_rating','Job9_Reviews','Job9_Location','Job9_Description','Job9_Salary','Job9_Posted','Job9_url','Job10_title','Job10_Company_Name','Job10_rating','Job10_Reviews','Job10_Location','Job10_Description','Job10_Salary','Job10_Posted','Job10_url']
	self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'Indeed_data_%s.csv'% self.today_date
	self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.headers)
	self.query1 = 'select sk, keyword, reference_url, job_count from job_meta'
	self.query2 = 'select title, company_name, rating, reviews, location, description, salary, posted_on, reference_url from jobs where job_sk=%s'

    def __del__(self):
	self.conn.close()
        self.cur.close()
    
    def main(self):
	self.cur.execute(self.query1)
	rows = self.cur.fetchall()
	for row in rows:
	    sk, keyword, url, job_count = row
	    values = list((keyword, url, job_count))
	    self.cur.execute(self.query2,sk)
	    job_rows = self.cur.fetchall()
	    for i in range(0, 10):
		try:
		    job_row = job_rows[i]
		    values.extend(list(job_row))
		except:
		    values.extend(['', '', '', '', '', '', '', '', ''])
	    self.todays_excel_file.writerow(values)
	
if __name__ == '__main__':
    OBJ = IndeedCsvScript()
    OBJ.main()



