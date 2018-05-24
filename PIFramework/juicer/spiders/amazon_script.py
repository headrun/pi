import MySQLdb
import json
import xlwt
import datetime

excel_file_name = 'amazon_data_on.xls'
todays_excel_file = xlwt.Workbook(encoding="utf-8")
todays_excel_sheet1 = todays_excel_file.add_sheet("sheet1", cell_overwrite_ok=True)

header = ['product_url', 'product_id', 'name', 'price', 'is_prime', 'original_price', 'discount_price', 'best_sellerrank', 'features', 'description',\
	  'seller_name', 'seller_price', 'product_condition',\
          'reviewed_by', 'reviewed_on', 'review', 'review_rating','review_votes', 'review_title', 'verified_purchase_flag']
for i, row in enumerate(header):
    todays_excel_sheet1.write(0, i, row)


def connect():
        con = MySQLdb.connect(db='AMAZON', user='root', passwd='root', charset="utf8", host='localhost', use_unicode=True).cursor()
	return con

def run_main():
	query = 'select product_url, product_id, name, price, is_prime from BestSellers'
           
	con = connect()
	con.execute(query)
	rows = con.fetchall()
	row_count = 1
       
	for row in rows:
		product_url, product_id, name, price, is_prime = row
		seller_query = 'select seller_name, seller_price, product_condition from RelatedSellers where product_id = "%s"' % product_id
		con.execute(seller_query)
              
		sellers = con.fetchall()
		seller_lists = []
		for seller in sellers:
			seller_name, seller_price, product_condition = seller
			seller_lists.append([seller_name, seller_price, product_condition])
		product_query = 'select original_price, discount_price, best_sellerrank, features, description from Products where id = "%s"' % product_id
                
		con.execute(product_query)
		products = con.fetchall()
                if not products : continue
		for product in products:
			original_price, discount_price, best_sellerrank, features, description = product	
		#product_sellers = '<>'.join([''.join(seller) for seller in sellers])
		review_query = 'select reviewed_by, reviewed_on, review, review_rating, aux_info, verified_purchase_flag from CustomerReviews where product_id = "%s"' % product_id
		con.execute(review_query)
		reviews = con.fetchall()
		reviewed_by, reviewed_on, review, review_rating, review_votes, review_title, verified_purchase_flag = '', '', '', '', '', '', ''
		reviews_list = []
		for review in reviews:
			reviewed_by, reviewed_on, review, review_rating, aux_info, verified_purchase_flag = review
                        #if '"Don"t'  in aux_info : aux_info = aux_info.replace('"Don"t','"dont')
			reviewed_on = reviewed_on.date().strftime('%Y-%m-%d')
			review_rating = str(review_rating)
			try : 
                            aux = json.loads(aux_info)
                            review_votes = aux.get('review_votes', '')
                            review_title = aux.get('review_title', '')
                        except : 
		            review_votes = ''
			    review_title = ''
			reviews_list.append([reviewed_by, reviewed_on, review, review_rating, review_votes, review_title, verified_purchase_flag])
		if not reviews_list:
			reviews_list = [[reviewed_by, reviewed_on, review, review_rating, review_votes, review_title, verified_purchase_flag]]
		if not seller_lists:
			seller_lists = [['', '', '']]
		for seller_list in seller_lists:
                         
			values = [product_url, product_id, name, price, is_prime, original_price, discount_price, best_sellerrank, features, description]
                        if  len(values) < 10 : 
                            import pdb;pdb.set_trace()
                        if '/ref' in product_id : product_id = str(product_id.split('/')[0])
			values.extend(seller_list)
			values_orig = values
                        #print values_orig
			for review_list in reviews_list:
		                values.extend(review_list)
                                #if len(values)!=20 : 
				for col_count, value in enumerate(values):
			                todays_excel_sheet1.write(row_count, col_count, value)
                                #mport pdb;pdb.set_trace()
				values = values[:11]
				row_count = row_count+1
			values = []

	todays_excel_file.save(excel_file_name)


if __name__ == '__main__':
	run_main()
