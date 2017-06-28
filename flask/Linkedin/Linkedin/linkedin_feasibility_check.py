#https://www.linkedin.com/cws/member/public_profile?public_profile_url=za.linkedin.com/pub/vishrut-mittal/4/186/7a4&format=inline&related=false&original_referer=https%3A%2F%2Fdeveloper.linkedin.com%2Fetc%2Fdesigns%2Flinkedin%2Fkaty%2Fglobal%2Fclientlibs%2Fhtml%2Fsandbox.html%3Falign-class%3Dmiddle-center&token=&isFramed=true&lang=en_US&_ts=1490264453590.3835&xd_origin_host=https%3A%2F%2Fdeveloper.linkedin.com

import urllib2
import sys
import time
import traceback
import urllib

with open('/root/Linkedin/Linkedin/spiders/excelfiles/30k_linkedin.csv', 'r') as f:
	with open('30k_linkedin_check_another.csv', 'w+') as g:
		for line in f:
			try:
				_id, link, _, _, _, _ = line.strip().split(',')
			except:
				try: _id, link = line.strip().split(',')[0:2]
				except: 
					print traceback.format_exc()
			if 'linkdin_url' in link: continue
			link = urllib.quote(link)
			time.sleep(0.25)
			link = 'https://www.linkedin.com/profile/view%3Fid%3D5126548%26amp%3BauthType%3Dname%26amp%3BauthToken%3DoSoB%26amp%3Btrk%3Dprof-sb-browse'
			check_link = "%s%s%s"%("https://www.linkedin.com/cws/member/public_profile?public_profile_url=", link,"&format=inline&related=false&original_referer=https%3A%2F%2Fdeveloper.linkedin.com%2Fetc%2Fdesigns%2Flinkedin%2Fkaty%2Fglobal%2Fclientlibs%2Fhtml%2Fsandbox.html%3Falign-class%3Dmiddle-center&token=&isFramed=true&lang=en_US&_ts=1490264453590.3835&xd_origin_host=https%3A%2F%2Fdeveloper.linkedin.com")
			code = ''
			valid = False
			try:
				if 'linkedin' in link:
					code = urllib2.urlopen(check_link).getcode()
					code_text = urllib2.urlopen(check_link).read()
			except:
				code = ''
				print check_link
				print traceback.format_exc()
			if code == 200 and not 'your request could not be completed' in code_text.lower():
				valid = True
			if _id.replace('\n',''):
				g.write('%s,%s,%s\n' % (_id, link.replace('\n',''), valid))
				print _id, link.replace('\n',''), valid
		
