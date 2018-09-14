import csv
import MySQLdb
import datetime

class GithubCsvScript():

    def __init__(self):
        self.conn = MySQLdb.connect(db='Github', user='root', host='localhost', passwd='root', charset="utf8", use_unicode=False)
        self.cur = self.conn.cursor()
        self.headers = ['Repositories','Stars','Followers','Following','First Name','Last Name','Username','Summary','Location','Url','Organization Group','Pinned Repository1','Pinned Repository1_description','Pinned Repository1_type','Pinned Repository1_stargazers','Pinned Repository1_network','Pinned Repository2','Pinned Repository2_description','Pinned Repository2_type','Pinned Repository2_stargazers','Pinned Repository2_network','Pinned Repository3','Pinned Repository3_description','Pinned Repository3_type','Pinned Repository3_stargazers','Pinned Repository3_network','Pinned Repository4','Pinned Repository4_description','Pinned Repository4_type','Pinned Repository4_stargazers','Pinned Repository4_network','Pinned Repository5','Pinned Repository5_description','Pinned Repository5_type','Pinned Repository5_stargazers','Pinned Repository5_network','Pinned Repository6','Pinned Repository6_description','Pinned Repository6_type','Pinned Repository6_stargazers','Pinned Repository6_network','Count of Contributions','Contribution Activity1','Contribution Activity1_desc','Contribution Activity1_date','Contribution Activity2','Contribution Activity2_desc','Contribution Activity2_date','Contribution Activity3','Contribution Activity3_desc','Contribution Activity3_date']
	self.today_date = str(datetime.datetime.now()).split('.')[0].replace(' ','_')
        self.excel_file_name = 'Github_data_%s.csv'% self.today_date
        self.oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file  = csv.writer(self.oupf)
        self.todays_excel_file.writerow(self.headers)
	self.query1 = 'select id, first_name, last_name, username, summary, location, following, followers, repositories, stars,organization,reference_url,contributions from profile_meta'
        self.query2 = 'select id, name, description, type, stargazers, network from repositories where profile_id=%s'

    def __del__(self):
        self.conn.close()
        self.cur.close()
	
    def main(self):
        self.cur.execute(self.query1)
        rows = self.cur.fetchall()
        for row in rows:
	    id_, first_name, last_name, username, summary, location, following, followers, repositories, stars, organization, reference_url, contributors = row
	    values = [repositories, stars, following, followers, first_name, last_name, username, summary, location, reference_url, organization]
	    self.cur.execute(self.query2%id_)
	    r_rows = self.cur.fetchall()
	    for i in range(0, 6):
		try:
		    r_row = r_rows[i]
		    r_id, name, description, type_, stargazers, network = r_row
		    values.extend([name, description, type_, stargazers, network])
		except:
		    values.extend(['','','','',''])
	    self.todays_excel_file.writerow(values)

if __name__ == '__main__':
    OBJ = GithubCsvScript()
    OBJ.main()

