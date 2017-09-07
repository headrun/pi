from linkedin_voyager_functions import *
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
class Companysurlup(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.qu1 = 'insert into linkedin_mapping_meta(sk, pi_id, lnkd_original_url, lnkd_profile_url, member_id, company_logo, candidate_profile_picture, company_logo_path, candidate_profile_picture_path, modified_url, created_at, modified_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now(), sk=%s, pi_id=%s, lnkd_original_url=%s, lnkd_profile_url=%s, member_id=%s, company_logo=%s, candidate_profile_picture=%s, company_logo_path=%s, candidate_profile_picture_path=%s, modified_url=%s'
		self.qu2 = 'select sk, member_id, profile_image from linkedin_meta where profile_url like "%s" order by modified_at desc limit 1'
		self.qu4 = 'select sk, member_id, profile_image, profile_url from linkedin_meta where member_id  = "%s" order by modified_at desc limit 1'
		self.qu3 = 'select exp_company_logo from linkedin_experiences where profile_sk = "%s" limit 1'
		self.pulse_url = 'https://www.linkedin.com/pulse-fe/api/v1/followableEntity?vanityName=%s'

	def main(self):
		dicts_of_ids = {}
		counter = 0
		with open('mapping.csv') as f:
			r = csv.reader(f)
			for line in r:
				counter += 1
				#if counter < 63134:
					#continue
				if line[0] == 'pi_id':
					continue
				pattern = "%s%s" % (line[2].strip('/'), '%')
				rowp = fetchmany(self.cur, self.qu2 % pattern)
				sk, member_id, candidate_profile_picture, exp_company_logo, modified_url = ['']*5
				if rowp:
					sk, member_id, candidate_profile_picture = rowp[0]
				if sk:
					rowcm = fetchmany(self.cur, self.qu3 % sk)
					print sk
					if rowcm:
						exp_company_logo = rowcm[0][0]
				if not rowp:
                                        ros = line[2].strip('\n')
                                        if ros.endswith('/en') or ros.endswith('/fr'): ros = ros[:-3]
                                        if ros.endswith('/'): ros = ros[-1]
					ros = ros.split('/')[-1]
                                        developer_pf_url = self.pulse_url % ros
					try:
						reql = json.loads(requests.get(developer_pf_url).text)
						reql_member_id = reql.get('urn', '')
						if reql_member_id:
							reql_member_id = reql_member_id.split('urn:li:member:')[1]
							rowp = fetchmany(self.cur, self.qu4 % reql_member_id)
							if rowp:
								sk, member_id, candidate_profile_picture, modified_url = rowp[0]
					except:
						import traceback
						traceback.print_exc()
				if not rowp:
					print line[2].strip('/')
					file("mapping_meta_new1","ab+").write("%s\n" % line[2].strip('/'))
				
				pi_id, linkedin_orig_url, linkedin_prof_url = line
				values = (md5(pi_id+linkedin_prof_url), pi_id, linkedin_orig_url, linkedin_prof_url, member_id, exp_company_logo, candidate_profile_picture, '', '', modified_url, md5(pi_id+linkedin_prof_url), pi_id, linkedin_orig_url, linkedin_prof_url, member_id, exp_company_logo, candidate_profile_picture, '', '', modified_url)
				self.cur.execute(self.qu1 , values)

if __name__ == '__main__':
	Companysurlup().main()
		
		
		
