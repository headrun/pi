import random
import os
login_list = ['pavani','rama','kolla','bala','niki']
fil = open('user.txt', 'r')
flag = True
while flag:
	inde = random.randint(0,len(login_list)-1)
	if login_list[inde] not in fil.read():
		Fil = open('user.txt', 'w')
		Fil.write(login_list[inde])
		Fil.close()
		flag = False
	
cmd = 'scrapy crawl fbbrowse -a login="%s" --set  ROBOTSTXT_OBEY=0'%(login_list[inde])
os.system(cmd)
print cmd
print login_list[inde]

