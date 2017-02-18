import random
import os
class GetLogin(object):

	def main(self):
		login_list = ['pavani','rama','kolla','bala','niki', 'dummy','fbdummy','ch']
		fil = open('user.txt', 'r')
		flag = True
		while flag:
			inde = random.randint(0,len(login_list)-1)
			if login_list[inde] not in fil.read():
				Fil = open('user.txt', 'w')
				Fil.write(login_list[inde])
				Fil.close()
				flag = False
		cmd = 'scrapy crawl facebook_browse -a login="%s" --set  ROBOTSTXT_OBEY=0'%(login_list[inde])
		os.system(cmd)
if __name__ == '__main__':
    GetLogin().main()
