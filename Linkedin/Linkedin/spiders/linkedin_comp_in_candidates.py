from linkedin_voyager_functions import *
from linkedin_logins import ips_list
import requests

class Companyurls(object):
	def __init__(self, *args, **kwargs):
		self.con, self.cur = get_mysql_connection(DB_HOST, 'FACEBOOK', '')
		self.pulse_fe = "https://www.linkedin.com/pulse-fe/api/v1/followableEntity?vanityName=%s"
		self.conne_quer = "select profile_sk from linkedin_connections where member_id = '%s'"
		self.dic = {"46326075upasna-verma-0a362113":"upasnaverma@gmail.com",                                                                     "52397348richa-sharma-65866a15":"richasharma389@gmail.com",                                                                      "17621047anjali-kapoor-447a995":"Anjali.kapoor@positivemoves.com",                                                               "155889069ashish-khanna-6b925944": "ashish.khanna15@hotmail.com",                                                                "774879vandana-razdan-513314":"vandana.razdan@positivemoves.com",                                                                "1174250bhallapavan":"pavan.bhalla@positivemoves.com",                                                                           '11562459divya-basu-2a3a573' :"divya.basu@positivemoves.com",                                                                    "15374363christopher-fernandes-24b1955":'christopher.fernandes@positivemoves.com',                                               "1051174supriya-joshi-39a428":"supriya.joshi@positivemoves.com",                                                                 "24571177saurabh-manchanda-52128b8":"manchanda14@gmail.com",
                	"88399562sonal-bahl-1a273125":"sonalnayyar23@gmail.com",
	                 "5772697rajat-raina-821b241":"26.rajat@gmail.com",                                                                              '36474724dishabole':"dishabole@hotmail.com",                                                                                     "110636110nanda-sethi-63a07531":"nanda.sethi1@gmail.com",
        	         "15375020sudarshan-sharda-6b81955":"sudarshan.sharda@positivemoves.com",
                	"12456827vinnati-solomon-98b2084":"vinnati.solomon@pmoves.com",
	                "12555091praveen-malhotra-8172554":"praveen.malhotra@pmoves.com",
        	        "12222529vibhav-dhawan-2811154":"vibhav.dhawan@positivemoves.com",
			"5838169mohit-bhatia-6a1b561":"mohit-bhatia"}
	
	def main(self):
		with open('comp_in_candidate.txt', 'r') as f:
			rows = f.readlines()
			for row in rows:
				row = row.strip('\n').strip('/')
				public_id =  row.split('/')[-1]
				data = {}
				proxies = {'https': "%s%s%s" % ('http://',random.choice(ips_list),':3279')}
				try:
			            data = requests.get(self.pulse_fe % public_id, proxies=proxies).text
			        except:
			            data = {}
				if data:
					tmp = json.loads(data)
					member_id = tmp.get('urn')
					member_id = textify(re.findall('\d+', member_id))
					if member_id:
						profile_sk_list = list(fetchmany(self.cur, self.conne_quer % member_id))
						profile_sk = list(chain.from_iterable(profile_sk_list))
						lsit = []
						for ps in profile_sk:
							lsit.append(self.dic[ps])
						if lsit:
							print "%s is connected to %s " % (row, '<>'.join(lsit))
						
				
	
if __name__ == '__main__':
	Companyurls().main()
