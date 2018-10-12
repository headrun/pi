import requests
url = 'https://www.mcmaster.com/'

with open('ips-zone1.txt', 'r') as f:
	rows = f.readlines()
for row in rows:
	row = row.replace('\n', '')
	ip, port, username, pass_ = row.split(':')
	prxy = 'http://%s:%s@%s:%s'%(username, pass_, ip, port)
	proxy = {'http':prxy, 'https':prxy}
	try:
		
		response = requests.get(url ,proxies=proxy)
	except:
		print row


