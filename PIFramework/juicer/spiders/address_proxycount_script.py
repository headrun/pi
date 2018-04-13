import MySQLdb
import datetime
import os
import smtplib



class SecurityAlert(object):

    def __init__(self):
        self.con = MySQLdb.connect(db = 'address_components',
                      user        = 'root',
                      passwd      = 'root',
                      charset     = "utf8",
                      host        = 'localhost',
                      use_unicode = True)
        self.cur = self.con.cursor()
        self.select_qry = 'select count(distinct sk) from pincode_new where proxy_ip="%s" and date(modified_at)>="2017-06-29"'
        self.select_qry2 = 'select distinct proxy_ip  from pincode_new where status="OVER_QUERY_LIMI" and date(modified_at)>="2017-06-23"'

    def main(self) :
        ip_list = ['http://144.76.48.150:3279','http://144.76.48.146:3279','http://144.76.48.147:3279','http://176.9.181.37:3279','http://144.76.48.149:3279','http://176.9.181.40:3279','http://144.76.48.143:3279','http://144.76.48.144:3279','http://144.76.48.145:3279','http://144.76.48.148:3279','http://144.76.48.149:3279']
 
        for ip in ip_list : 
            self.cur.execute(self.select_qry%ip)
            data = self.cur.fetchall()
            if data : data = int(data[0][0])
            print data
           
            if data and data >=2500 : 
                self.send_mail(ip)

        """self.cur.execute(self.select_qry2)
        records = self.cur.fetchall()
        if records :
            for row in records:
                ip = row[0]
                self.send_mail(ip)"""
            

    def send_mail(self,ip):
	    from email.mime.multipart import MIMEMultipart
	    from email.mime.text import MIMEText
	    from email.mime.base import MIMEBase
	    from email import encoders
	    import smtplib,ssl
	    sender  = 'facebookdummyfb01@gmail.com'
            #receivers_mail_list = ['kiranmayi@notemonk.com','anushab@notemonk.com','aravind@headrun.com']
            receivers_mail_list = ['kiranmayi@notemonk.com','anushab@notemonk.com']
            sender, receivers = sender, ','.join(receivers_mail_list)
	    msg = MIMEMultipart('alternative')
	    msg['Subject'] = "Alert mail of google address API requests on '%s'"%str(datetime.datetime.now().date())
	    msg['From'] = sender
	    msg['To'] = receivers
	    html = '<html><head></head><body>'
	    html += '<h2>Reached the maximum usage limit of proxy in pi machine "%s"</h2>'%ip
	    tem = MIMEText(html, 'html')
	    msg.attach(tem)
	    s = smtplib.SMTP('smtp.gmail.com:587')
	    s.ehlo()
	    s.starttls()
	    s.ehlo()
	    #s.login(sender, '01123123')
	    #s.sendmail(sender, receivers_mail_list, msg.as_string())
            


if __name__ == '__main__':
    SecurityAlert().main()
