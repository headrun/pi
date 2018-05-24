import sys
import os
import csv

absoulte_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append('/'.join(absoulte_path.split('/')[:-1]))
from utils import *

class Flipkartcsv(object):
	def __init__(self, *args, **kwargs):
		self.db_name = 'FLIPKART'
		self.con, self.cur = get_mysql_connection('localhost', self.db_name, '')
		self.excel_file_name = 'flipkart_clothing_electronics_products_reviews_%s.csv' % str(datetime.datetime.now().date())
		self.excel_file_name2 = 'flipkart_clothing_electronics_products_relatedsellers_%s.csv' % str(datetime.datetime.now().date())
		four_sheets = [self.excel_file_name, self.excel_file_name2]
		for fil_nam in 	four_sheets:
			self.if_file_exists(fil_nam)
		oupf = open(self.excel_file_name, 'ab+')
                oupf2 = open(self.excel_file_name2, 'ab+')
		self.todays_excel_file  = csv.writer(oupf)
                self.todays_excel_file2  = csv.writer(oupf2)
		self.main_headers_list = ['product_id', 'name', 'original_price', 'discount_price', 'features', 'description', 'item_number', 'date_available', 'best_sellerrank', 'sub_title', 'specifications', 'images', 'reference_url']
		self.main_headersdup_list = ['product_id', 'name', 'original_price', 'discount_price', 'features', 'description', 'item_number', 'date_available', 'best_sellerrank', 'sub_title', 'specifications','images','reference_url']
		self.reviews_headers_list = ['reviewed_by', 'reviewed_on', 'review', 'category', 'review_url', 'review_rating', 'verified_purchase_flag']
		self.relatedsellers_list = ['category', 'product_condition', 'seller_name', 'seller_no_of_rating', 'seller_rating_percentage', 'seller_price', 'is_prime', 'delivery_info', 'offer_info'] # [3:-2]-1 have aux_info
		self.query1 = 'select * from %s'
		self.query2 = 'select * from %s where %s = "%s"'
		self.images1 = 'select image_url from RichMedia where product_id="%s"'

	def if_file_exists(self, file_name):
		if os.path.isfile(file_name):
			os.system('rm %s' % file_name)

	def join_headers(self, j_fir, j_sec):
		j_fir.extend(j_sec)
		return j_fir

	def fetchmany(self, cursor, query):
		execute_query(cursor, query)
		recs = cursor.fetchmany(5000)
		return recs
	
	def querydesign(self, product_id, table):
		final_to_update = []
		values = self.fetchmany(self.cur, self.query2%(table[1], 'product_id', product_id))
		for ind, val in enumerate(values):
			if table[1] == 'CustomerReviews':
				vals_ = list(val)[3:-3]
			else:
				vals_ = list(val)[3:-2]
				vals_1 = {}
				try:
					vals_1 = json.loads(vals_[-1])
				except:
					vals_1  = {}
				del vals_[-1]
				vals_.append(vals_1.get('delivery_info', ''))
				vals_.append(vals_1.get('offer_info', ''))
			final_to_update.append(vals_)
		if not final_to_update:
			final_to_update.append(['' for i in table[0]])
		return final_to_update


	def main(self):
		records = fetchall(self.cur, self.query1%('Products'))
		three_more = [(self.reviews_headers_list, 'CustomerReviews'), (self.relatedsellers_list, 'RelatedSellers')]
		for inde, rec in enumerate(records):
			info_rec = list(rec)[:-2]
			jsdata = {}
			try:
				jsdata = json.loads(info_rec[-2])
			except:
				jsdata = {}
			info_rec[-2] = jsdata.get('specifications','')
			info_rec.insert(-2, jsdata.get('sub_title',''))
			total_richme_list = self.fetchmany(self.cur, self.images1% info_rec[0])
			richme_list = list(chain.from_iterable(total_richme_list))
			info_rec.insert(-1, '<>'.join(richme_list).strip('<>'))
			for table in three_more:
				if inde == 0:
					new_headers = self.join_headers(self.main_headers_list[0:13], table[0])
					if table[1] == 'CustomerReviews':
						self.todays_excel_file.writerow(new_headers)
					else:
						self.todays_excel_file2.writerow(new_headers)
				callfun = self.querydesign(info_rec[0], table)
				for cf in callfun:
					info_rec.extend(cf)
					info_rec = [str(row) if isinstance(row, long) or isinstance(row, int) or isinstance(row, datetime.datetime) else row for row in info_rec]
					info_rec = [normalize(i) for i in info_rec]
					if table[1] == 'CustomerReviews':
						self.todays_excel_file.writerow(info_rec)
					else:
						self.todays_excel_file2.writerow(info_rec)
					print len(info_rec), table[1]
					info_rec = info_rec[0:len(self.main_headersdup_list)]
				#self.main_headers_list = self.main_headersdup_list

if __name__ == '__main__':
	Flipkartcsv().main()
	
