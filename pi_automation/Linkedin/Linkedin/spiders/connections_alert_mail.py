from linkedin_voyager_functions import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Connectionsalert(object):
        def main(self):
		real_path = os.path.dirname(os.path.realpath(__file__))
		dic = dic_ln
		os.chdir('/tmp')
		consumer_chal = commands.getstatusoutput("grep -l consumer-captcha-v2?challengeId *.log")
		account_blocked = commands.getstatusoutput("grep -l account-restricted?email *.log")
		account_c = commands.getstatusoutput("grep -l closed *.log")
		os.chdir(real_path)
		sender_mail = sender_mail_pi
		receivers_mail_list = ['anushab@notemonk.com']
		sender, receivers  = sender_mail, ','.join(receivers_mail_list)
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'Alert mail for security challenges'
		mas = '<h4>Linkedin accounts facing issues at this time, need to solve this </h4>'
		listch = []
		for i in [(consumer_chal,'consumerchallenge'),(account_blocked,'account blocked')]:#,(account_c,'closed files')]:
			if i[0][-1]:
				mas += '<table border="1">'
				files_list = i[0][-1].split('\n')
				mas += '<tr><th>logfile</th><th>Account mail</th><th>Account password</th><th>Facing issue</th>'
				for s in files_list:
					if s in dic.keys():
						listch.append(s)
					
						mas += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(s, dic[s][0], dic[s][1], i[1])
				mas += '</table>\n'
		if listch:
			msg['From'] = sender
			msg['To'] = receivers
			tem = MIMEText(''.join(mas), 'html')
			msg.attach(tem)
			s = smtplib.SMTP('smtp.gmail.com:587')
			s.ehlo()
			s.starttls()
			s.ehlo()
			s.login(sender_mail, sender_pwd_pi)
			s.sendmail(sender, receivers_mail_list, msg.as_string())
			s.quit()
				
if __name__ == '__main__':
    Connectionsalert().main()

