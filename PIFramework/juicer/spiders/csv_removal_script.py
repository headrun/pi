import datetime
import os
import glob
def main():
    range_start = 0
    processed_files = glob.glob('/root/PIFramework/juicer/spiders/paytm_csv_files/*')
    date_list = []
    for i in range(3, 7):
	delete_date = datetime.datetime.now() + datetime.timedelta(days=-i)
	date_list.append(delete_date.date())
    for file_ in processed_files: 
    	for date_ in date_list:
	    if str(date_) in file_:
		os.remove(file_)

if __name__ == '__main__':
   main()
