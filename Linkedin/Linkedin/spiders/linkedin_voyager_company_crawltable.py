from linkedin_voyager_functions import *
import openpyxl as px
import collections

class Lvccc(object):
	def __init__(self):
		current_path = os.path.dirname(os.path.abspath(__file__))
		self.filec_path = os.path.join(current_path, 'pm_companies_linkedin_urls.csv')
		self.con, self.cur = get_mysql_connection(DB_HOST, DB_NAME_REQ, '')
		print DB_NAME_REQ
		self.query = 'insert into linkedin_company_crawl(sk, url, content_type ,crawl_status, meta_data,created_at, modified_at) values(%s, %s, %s, %s, %s,now(), now()) on duplicate key update modified_at=now(), content_type=%s, crawl_status=0,meta_data=%s'

	def __del__(self):
		close_mysql_connection(self.con, self.cur)

        def main(self):
		files_list = ['pm_companies_linkedin_urls.xlsx']
		url_list = []
		for _file in files_list:
			ws_ = px.load_workbook(_file, use_iterators=True)
			sheet_list = ws_.get_sheet_names()
			for xl in sheet_list:
				sheet_ = ws_.get_sheet_by_name(name=xl)
				for row in sheet_.iter_rows():
				    	sno, comp, url = row[0:3]
					sno = sno.value
					comp = comp.value
					url = url.value
					if 'linkedin.com' not in url:continue
					url_list.append(url)
				    	meta_date_from_browse = {"sno":sno, "company_url":url, "company_given_name":comp}
			    		crawl_status = 0
				    	sk = md5(url)
				    	values = (sk, url, 'linkedin_company', crawl_status, json.dumps(meta_date_from_browse),'linkedin_company', json.dumps(meta_date_from_browse))
			                self.cur.execute(self.query, values)
		dupe_list = [item for item, count in collections.Counter(url_list).items() if count > 1]
		print dupe_list
		for dp in dupe_list:
			file("duplicate_linkedin_company_urls_list.txt","ab+").write("%s\n" %dp)
		

if __name__ == '__main__':
   Lvccc().main()


	
