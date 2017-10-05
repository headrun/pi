from linkedin_voyager_functions import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Connectionsalert(object):
        def main(self):
		real_path = os.path.dirname(os.path.realpath(__file__))
		dic = {"linkedin_profilesskira2.log":["kira2headrun@gmail.com",'kira^123'],"linkedin_profilesmiley.log":["smileykutie@gmail.com","smileykutie$"], "linkedin_profilesccv.log":["ccvy1.pavani1886@gmail.com",'ccvy1.pavani@1886'],"linkedin_profilesmeat.log":["meatproject05@gmail.com","ram123123"],"linkedin_profiles.log":["srinivasaramanujan427@gmail.com","dotoday1#"], "linkedin_profileskumar1.log":['kumararajukumar57@gmail.com', 'kumararaja1234'], "linkedin_profileschinni1.log":['rajachintala3@gmail.com', 'raja1234'], "linkedin_profilesmeat1.log":["meatproject05@gmail.com","ram123123"], "linkedin_profilesmiley1.log":["smileykutie@gmail.com","smileykutie$"], "linkedin_profiles1.log":["srinivasaramanujan427@gmail.com","dotoday1#"], "linkedin_profilesccv1.log":["ccvy1.pavani1886@gmail.com",'ccvy1.pavani@1886']}
		os.chdir('/tmp')
		consumer_chal = commands.getstatusoutput("grep -l consumer-captcha-v2?challengeId *.log")
		account_blocked = commands.getstatusoutput("grep -l account-restricted?email *.log")
		account_c = commands.getstatusoutput("grep -l closed *.log")
		os.chdir(real_path)
		sender_mail = 'facebookdummyfb01@gmail.com'
		receivers_mail_list = ['kiranmayi@notemonk.com', 'anushab@notemonk.com', 'aravind@headrun.com']
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
			s.login(sender_mail, '01123123')
			s.sendmail(sender, receivers_mail_list, msg.as_string())
			s.quit()
				
if __name__ == '__main__':
    Connectionsalert().main()

