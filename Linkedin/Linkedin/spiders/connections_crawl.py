from linkedin_functions import *
#from crontab import CronTab

class Connections(object):
        def main(self):
		"""verify_cron_closed = commands.getstatusoutput("cat /tmp/linkedin_profiles.log | grep 'Spider closed'")
		if verify_cron_closed and len(verify_cron_closed) == 2:
			if 'Spider closed' in verify_cron_closed[1]:
				print "need to execute cron"
				#crontab -l > mycron
				#cron = CronTab(user=True)
				#job = cron.new(command='scrapy crawl linkedinpremiumprofilesibkup_browse -a login="ccv" --set ROBOTSTXT_OBEY=0 2>/tmp/linkedin_connectionsbkup.log 1>/tmp/linkedin_connectionsbkup.log')
				#job.minute.on(2)
				#job.hour.on(12)
				#os.execute('scrapy crawl linkedinpremiumprofilesibkup_browse -a login="ccv" --set ROBOTSTXT_OBEY=0') 2>/tmp/linkedin_connectionsbkup.log 1>/tmp/linkedin_connectionsbkup.log"""
		verify_runscrapy = commands.getstatusoutput("pgrep -fl linkedinconnectionsnew_terminal")
		import pdb;pdb.set_trace()
		if verify_runscrapy and len(verify_runscrapy) == 2:
			if not 'scrapy' in verify_runscrapy[1]:
				current_path = os.path.abspath(os.path.dirname(__file__))
				cmd = "cd %s; /usr/local/bin/scrapy crawl linkedinconnectionsnew_terminal --set ROBOTSTXT_OBEY=0"%current_path
				os.system(cmd)
		
			
if __name__ == '__main__':
    Connections().main()

