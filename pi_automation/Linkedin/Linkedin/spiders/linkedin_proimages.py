"""from stats_gen_functions import *
import urllib
import os
import sys
import requests
import urllib.request

class LinkedinimgScript(object):
	def __init__(self):
		self.con = MySQLdb.connect(db   = 'FACEBOOK',host = 'localhost', charset="utf8", use_unicode=True,user = 'root', passwd ='root')
		self.cur = self.con.cursor()
		#self.select_query1 ="select member_id from linkedin_meta where profile_image !='' limit 1"
		self.select_query1 = " select sk from linkedin_meta where image_path!= '' limit 32,10"
		self.select_query2 = "select sk, member_id, profile_url, profile_image,image_path from linkedin_meta where sk ='%s'"
		self.insert_query = "insert into linkedin_profic.linkedin_profilepic_meta(sk,url,data_size,image_width,image_height,image_path,image_url,aux_info,reference_url,status,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()"
		self.main()

	def main(self):
		self.cur.execute(self.select_query1)
		profile_id = self.cur.fetchall()
		pro_id = profile_id
		for index, pro_ids in enumerate(pro_id):
			pro_ids1 = pro_ids[0]
			meta_img = self.select_query2%(pro_ids1)
			self.cur.execute(meta_img)
			data_img = self.cur.fetchall()
			data_images = data_img
			for data_image in data_images:
				sk = data_image[0]
				mem_id = data_image[1]
				profile_url = data_image[2]
				pro_url = ''.join(re.findall('/in/(\w+)', ''.join(profile_url)))
				#pro_img_url= 'https://www.linkedin.com/pulse-fe/api/v1/followableEntity?vanityName=%s'%(pro_url)
				profile_image1 = data_image[3]
				profile_image_path = data_image[4]
				mems_ids = ''.join(pro_url)+'_'+str(mem_id)
				profile_image_path1,status = '',''
				image = urllib.URLopener()
				real_path =  os.path.dirname(os.path.realpath(__file__))
				os.chdir("%s%s" % (real_path, '/images/image'))
                                '''proxies = {'http': 'http://144.76.48.143:3279',
					   'http': 'http://144.76.48.144:3279',
					   'http':'http://144.76.48.145:3279'}'''
				proxy = urllib.request.ProxyHandler({'http://144.76.48.144:3279'})
				opener = urllib.request.build_opener(proxy)
				urllib.request.install_opener(opener)
				urllib.request.urlretrieve('http://www.google.com')
				import pdb;pdb.set_trace()
				#img_aq = urllib.urlopen(profile_image1, proxies=proxies)
				#image_name = image.retrieve("".join(img_aq), '%s.jpg'%str(mems_ids))
				img_data = requests.get("".join(profile_image1),proxies=proxies)
				#img_data =  urllib.urlopen(profile_image1,proxies=proxies)
				#status1 = img_data.status_code
				import pdb;pdb.set_trace()
				print img_data
				if status1 == 200:
					status='available'
					with open(mems_ids, 'w+') as f:
						f.write(''.join(img_data.url))
						#f.write(profile_image1)
						import pdb;pdb.set_trace()
					image_name = [profile_image1,mems_ids]
					img_path = os.path.dirname(os.path.abspath(mems_ids))
					#profile_image_path1 = "%s%s%s%s%s"%("/root/Linkedin/Linkedin/spiders/images/image/",pro_url,'_',mem_id,'.jpg')
					#path = "/root/Linkedin/Linkedin/spiders/images/image"
					#cmd = "mv '%s' '%s'" % (mems_ids, path)
					#os.system(cmd)
					os.chdir(real_path)
					'''values =[sk,profile_url,'','','',profile_image_path1,profile_image2,'',profile_url,status]
					self.cur.execute(self.insert_query,values)
					self.con.commit()
				else: 
					status = '404'
					profile_image_path1 = "%s%s%s%s%s"%("/root/Linkedin/Linkedin/spiders",pro_url,'_',mem_id,'.jpg')
					os.chdir(real_path)
					values =[sk,profile_url,'','','',profile_image_path1,profile_image1,'',profile_url,status]
					self.cur.execute(self.insert_query,values)
					self.con.commit()'''

if __name__ == '__main__':
	LinkedinimgScript()"""
	
