import MySQLdb
import json
import xlwt
import datetime
from linkedin_functions import *

header = ['product_url', 'product_id', 'name', 'price', 'is_prime', 'original_price', 'discount_price', 'best_sellerrank', 'features', 'description','seller_name', 'seller_price', 'product_condition','reviewed_by', 'reviewed_on', 'review', 'review_rating', 'review_votes', 'review_title', 'item_weight','model','weight','comfort','number','color','dimension','Installation_Type','brand','console','Batteries_Included','Batteries_Required','Maximum_Rotational_Speed','Wattage','Voltage','special_features','Noise_Level','verified_purchase_flag']

excel_file_name = 'Amazon_data_on_%s.csv'%str(datetime.datetime.now().date())
oupf = open(excel_file_name, 'wb+')
todays_excel_file  = csv.writer(oupf)
todays_excel_file.writerow(header)


def connect():
    con = MySQLdb.connect(db='AMAZON', user='root', passwd='root',
                          charset="utf8", host='localhost', use_unicode=True).cursor()
    return con


def run_main():
    query = 'select product_url, product_id, name, price, is_prime from BestSellers where date(modified_at)>="2018-06-03"'
    con = connect()
    con.execute(query)
    rows = con.fetchall()
    for row in rows:
        product_url, product_id, name, price, is_prime = row
        seller_query = 'select seller_name, seller_price, product_condition from RelatedSellers where product_id = "%s" limit 1' % product_id
        con.execute(seller_query)
        sellers = con.fetchall()
        
        try : seller_name, seller_price, product_condition = sellers[0]
        except : seller_name, seller_price, product_condition = '','',''
        product_query = 'select original_price, discount_price, best_sellerrank, aux_info, features, description from Products where id = "%s"' % product_id
        con.execute(product_query)
        products = con.fetchall()
        if not products : continue
        original_price, discount_price, best_sellerrank, aux_info, features, description = products[0]
        try : aux = json.loads(aux_info.replace('\t','').replace('\n','').replace('\r',''))
        except : 
            aux = {} 
        item_weight = aux.get('Item Weight','') or aux.get('Capacity','') or aux.get('Water Consumption','')
	model = aux.get('Item Model Number','') or aux.get('Model','')
	weight = aux.get('Shipping Weight','')
	comfort = aux.get('Mattress Comfort','') or aux.get('Form Factor','')
	number = aux.get('Item Part Number','')
	color = aux.get('Color','') or aux.get('Colour','') or aux.get('Material','')
	dimension = aux.get('Product Dimensions','')
	Installation_Type = aux.get('Installation Type','')
	brand = aux.get('Brand','')
	console = aux.get('Control Console','')
	Batteries_Included = aux.get('Batteries Included','')
	Batteries_Required = aux.get('Batteries Required','')
	Maximum_Rotational_Speed = aux.get('Maximum Rotational Speed','')
	Wattage = aux.get('Wattage','')
	Voltage = aux.get('Voltage','')
	special_features = aux.get("Special Features",'') or aux.get('Included Components','')
	Noise_Level = aux.get('Noise Level','')
           
        review_query = 'select reviewed_by, reviewed_on, review, review_rating, aux_info, verified_purchase_flag from CustomerReviews where product_id = "%s"' % product_id
        con.execute(review_query)
        reviews = con.fetchall()
        reviewed_by, reviewed_on, review, review_rating, review_votes, review_title, verified_purchase_flag = '', '', '', '', '', '', ''
        for review_ in reviews:
            reviewed_by, reviewed_on, review, review_rating, aux_info_, verified_purchase_flag = review_
            reviewed_on = reviewed_on.date().strftime('%Y-%m-%d')
            review_rating = str(review_rating)
            try : 
                aux_ = json.loads(aux_info_)
                review_votes = aux_.get('review_votes', '')
                review_title = aux_.get('review_title', '')

            except : 
                review_votes = ''
                review_title = ''

 
            product_id = product_id.split('/')[0]
            values = [product_url, str(product_id), name, str(price), str(is_prime),str(original_price), str(discount_price), str(best_sellerrank), features, description, seller_name, str(seller_price), product_condition,reviewed_by, reviewed_on, review, str(review_rating), review_votes, review_title, item_weight,model,weight,comfort,number,color,dimension,Installation_Type,brand,console,Batteries_Included,Batteries_Required,Maximum_Rotational_Speed,Wattage,Voltage,special_features,Noise_Level,str(verified_purchase_flag)]
            values = [normalize(i) for i in values]
            todays_excel_file.writerow(values)

if __name__ == '__main__':
    run_main()
