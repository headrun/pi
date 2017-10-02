from stats_gen_functions import *
from datetime import date, timedelta, time
import datetime

class LinkedInScript(object):
    def __init__(self):
	self.count_list = []
	self.con = MySQLdb.connect(db='FACEBOOK',user='root',passwd='root',
                      charset="utf8",host='localhost',use_unicode=True)
	self.cur = self.con.cursor()
	self.select_query1 = "SELECT count(*) from linkedin_crawl where crawl_status=%d and created_at='%s'"
        self.main()

    def main(self):
	yesterday = str(date.today() - timedelta(1))+' '+'00:00:00'
	crawl_status1 = [0,1,9,6]
	for i in crawl_status1:
	    select_query1 = self.select_query1%(i,yesterday)
	    self.cur.execute(select_query1)
	    data = self.cur.fetchall()
	    data = data[0][0]
	    self.count_list.append(data)
	today_date = str(datetime.datetime.now())
	sender_mail = sender_mails
	receivers_mail_list = receivers_mail_lists
	sender, receivers  = sender_mail, ','.join(receivers_mail_list)
	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Li crawl automation Stats Generation'+' '+ 'on' +' '+ today_date
	crawl_status = '<html><head><Counts</head>'
	crawl_status += '<table border="1">'
	crawl_status += u'<tr> <td><b>Description</b></td>'
	crawl_status += u'<td><b>Count</b></td>'
	crawl_status += '</tr>'
	crawl_status += u'<tr> <td>No.of urls successfully crawled</td>'
	crawl_status += u'<td>%s</td>'%(self.count_list[1])
	crawl_status += '</tr>'
	crawl_status += u'<tr> <td>No.of urls has to be crawl</td>'
	crawl_status += u'<td>%s</td>'%(self.count_list[0])
	crawl_status += '</tr>'
	crawl_status += u'<tr> <td>No.of urls are in progress</td>'
	crawl_status += u'<td>%s</td>'%(self.count_list[2])
	crawl_status += '</tr>'
	crawl_status += u'<tr> <td>No.of urls not having data</td>'
	crawl_status += u'<td>%s</td>'%(self.count_list[3])
	crawl_status += '</tr>'
	crawl_status += '</table>'
	msg['From'] = sender
	msg['To'] = receivers
	tem = MIMEText(''.join(crawl_status), 'html')	
	msg.attach(tem)
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(sender_mail, password)
	server.sendmail(sender, receivers_mail_list, msg.as_string())
	server.quit()

if __name__ == '__main__':
    LinkedInScript()
