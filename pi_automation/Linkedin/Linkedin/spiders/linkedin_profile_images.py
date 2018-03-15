from stats_gen_functions import *
import urllib
import os
import sys
import re
import requests
import shutil

class LinkedinImageScript(object):
	def __init__(self):
		self.con = MySQLdb.connect(db   = 'FACEBOOK',host = 'localhost', charset="utf8", use_unicode=True,user = 'root', passwd ='root')
		self.cur = self.con.cursor()
		self.select_query1 = "select sk from linkedin_meta where image_path != ''"
		self.select_query2 = "select sk, member_id, profile_url, profile_image,image_path from linkedin_meta where sk ='%s'"
		self.insert_query = "insert into linkedin_profic.linkedin_profilepic_meta(sk,url,data_size,image_width,image_height,image_path,image_url,aux_info,reference_url,status,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now(), data_size=%s"
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
				pro_url = profile_url.split('/')[-1]
				if pro_url:
					pro_url = ''.join(pro_url).encode('utf-8').strip()
				else:
					pro_url = profile_url.split('/')[-2].encode('utf-8').strip()
				profile_image1 = data_image[3]
				if 'shrink' in profile_image1:
					continue
				profile_image_path = data_image[4]
				mems_ids = ''.join(pro_url)+'_'+str(mem_id)+'.jpg'
				print mems_ids
				real_path =  os.path.dirname(os.path.realpath(__file__))
				os.chdir("%s%s" % (real_path, '/images/image'))
				profile_image_path1,status = '',''
                                import urllib2
				proxy = urllib2.ProxyHandler({'http':'http://144.76.48.1454:3279'})
				opener = urllib2.build_opener(proxy)
				urllib2.install_opener(opener)
				req = urllib2.Request(profile_image1)
				dim_hei,dim_wei,data_size='','',''
				try:
					x = urllib2.urlopen(req)
					size = x.headers.get("content-length",'')
					if size : data_size = str(round(float(size)/1024,2)) + 'Kb'
					with open(mems_ids,'wb') as f:
						f.write(x.read())
					status = '200'
					dim_hei = re.findall('_(\d+)_\d+',''.join(profile_image1))
					dim_wei = re.findall('_\d+_(\d+)',''.join(profile_image1))
				except urllib2.HTTPError as e:
					if e.code == 410:
						status='410'
					else:
						status='404'
				image_path = os.path.dirname(os.path.abspath(mems_ids))+'/'+mems_ids
				os.chdir(real_path)
				values =[sk,profile_url,''.join(data_size),''.join(dim_wei),''.join(dim_hei),image_path,profile_image1,'',profile_url,status,''.join(data_size)]
                                self.cur.execute(self.insert_query,values)
                                self.con.commit()
				

if __name__ == '__main__':
	LinkedinImageScript()
	
