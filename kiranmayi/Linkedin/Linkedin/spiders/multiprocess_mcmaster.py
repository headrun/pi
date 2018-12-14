from multiprocessing import Process
import sys
import os
import re
import time

def run_scraper_overhaul(p, k, path):
        os.chdir(path)
        os.system(p)
        print p, k


class OverhaulMultiProcess(object):
        def __init__(self):
		self.r_list = ["export PATH=$PATH:/root/kiranmayi/myenv/bin; scrapy crawl mcmaster_browse --set ROBOTSTXT_OBEY=0 --set LOG_LEVEL='DEBUG' --set DOWNLOAD_DELAY=3",]
		self.RUN_PATH = "/root/kiranmayi/Linkedin/Linkedin/spiders"
                self.main()

        def main(self):
                processes = []
                for m in range(1, 11):
                        for j in self.r_list:
                                n = m + 1
                                p = Process(target=run_scraper_overhaul,
                                    args=(str(j), str(m), self.RUN_PATH))
                                p.start()
                                processes.append(p)
                                time.sleep(2)
			
                for p in processes:
                        p.join()

if __name__ == '__main__':
    OverhaulMultiProcess()


