from stats_gen_functions import *
import urllib
import os
import sys
import re
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')

class TwitterimgScriptraju(object):
    def __init__(self):
        self.con = MySQLdb.connect(db   = 'FACEBOOK',host = 'localhost', charset="utf8", use_unicode=True,user = 'root', passwd ='root')
        self.cur = self.con.cursor()
        self.select_query1 = "select sk from Twitter_latest where image != 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'"
        self.select_query2 = "select sk, image, twitter_url, screen_name,email_id from Twitter_latest where sk ='%s'"
        self.insert_query = "insert into twitter_profic.twitter_profilepic_meta(sk,url,data_size,image_width,image_height,image_path,image_url,email_id,reference_url,status,created_at,modified_at) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) on duplicate key update modified_at = now()"
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
                image = ''.join(data_image[1])
                twitter_url = data_image[2]
                screen_name = data_image[3]
                email_id = data_image[4]
                twitter_id = ''.join(screen_name)+'.jpg'
                twitter_image = image.replace('normal','400x400')
                real_path =  os.path.dirname(os.path.realpath(__file__))
                os.chdir("%s%s" % (real_path, '/twitter/images'))
		req = urllib2.Request(twitter_image)
		data_size,image_path='',''
		try:
		    image_tw = urllib2.urlopen(req)
		    status = '200'
		    size = image_tw.headers.get("content-length",'')
		    if size : data_size = str(round(float(size)/1024,2)) + 'Kb'
		    with open(twitter_id,'w+') as f:
			f.write(image_tw.read())
		    image_path = os.path.dirname(os.path.abspath(twitter_id))+'/'+twitter_id
		except urllib2.HTTPError:
			status='404'
                os.chdir(real_path)
                values = [''.join(sk),''.join(twitter_url),''.join(data_size),'400','400',''.join(image_path),''.join(twitter_image),''.join(email_id),''.join(twitter_url),status]
                self.cur.execute(self.insert_query,values)
                self.con.commit()


if __name__ == '__main__':
	TwitterimgScriptraju()
