from juicer.utils import *

class UpcitemdbTerminal(JuicerSpider):
	name = 'upcitemdb_company_terminal'
	
	def __init__(self, *args, **kwargs):
            super(UpcitemdbTerminal, self).__init__(*args, **kwargs)
	    self.insert_query1 = "INSERT INTO upcitem_meta(sk,upc,ean,amazon_asin,country_of_registration,brand,model,size,color,weight,product_dimension,last_scanned,product_title,product_name_variations,isbn,isbn_identifier_group,isbn_publisher,isbn_title_id,isbn_check_digit,image,aux_info,reference_url,created_at,modified_at,last_seen) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now(),now()) on duplicate key update modified_at = now()"
            
	
	def execute_query(self, query, values):
	    conn = MySQLdb.connect(db='UPCITEMDB',
                      user='root',
                      passwd='root',
                      charset="utf8",
                      host='localhost',
                      use_unicode=True)
	    cursor = conn.cursor()
	    if values:
		cursor.execute(query , values)
	    conn.commit()
	    cursor.close()
	    conn.close()
	    return		

	def parse(self, response):
	    sel = Selector(response)
	    sk = response.meta['sk']
	    dict1 = {}
	    list1 = []
	    aux_info = {}
	    title = normalize(''.join(sel.xpath('//p[@class="detailtitle"]/b/text()').extract()))
	    image = normalize('<>'.join(response.xpath('//div[@class="imglist"]/img/@src').extract()))
	    description = normalize('<>'.join(sel.xpath('//div[@class="cont"]/ol/li/text()').extract()))
	    extra_info = normalize(''.join(sel.xpath('//div[@class="wheretobuy"]/text()').extract()))
	    if extra_info:
		aux_info.update({'extra_info':extra_info})
	    list1 = sel.xpath('//div[@id="info"]/dl[@class="detail-list"]/dt/text()').extract()
	    list2 = ['UPC-A:','EAN-13:','Amazon ASIN:','Country of Registration:','Brand:','Model #:','Size:','Color:','Weight:','Product Dimension:','Last Scanned:','ISBN:','ISBN Identifier Group:','ISBN Publisher:','ISBN Title ID:','ISBN Check Digit:']
	    for i in list2:
		values1 = normalize(''.join(sel.xpath('//div[@id="info"]/dl[@class="detail-list"]/dt[contains(text(),"%s")]/following-sibling::dd[1]//text()'%i).extract()))
	    	dict1.update({normalize(i):values1})

	    for i in list1:
		if i not in list2:
		    values2 = normalize(''.join(sel.xpath('//div[@id="info"]/dl[@class="detail-list"]/dt[contains(text(),"%s")]/following-sibling::dd[1]//text()'%i).extract()))
                    aux_info.update({normalize(i):values2})
	    values3 = (normalize(sk),dict1.get('UPC-A:',''),dict1.get('EAN-13:',''),dict1.get('Amazon ASIN:',''),dict1.get('Country of Registration:',''),\
			dict1.get('Brand:',''),dict1.get('Model #:',''),dict1.get('Size:',''),dict1.get('Color:',''),dict1.get('Weight:',''),\
			dict1.get('Product Dimension:',''),\
			dict1.get('Last Scanned:',''),title,description,dict1.get('ISBN:',''),dict1.get('ISBN Identifier Group:',''),\
			dict1.get('ISBN Publisher:',''),dict1.get('ISBN Title ID:',''),dict1.get('ISBN Check Digit:',''),image,\
			json.dumps(aux_info),normalize(response.url))
	    self.execute_query(self.insert_query1, values3)
	    nodes = response.xpath('//table[@class="list"]/tbody/tr')
	    for node in nodes:
                link = 'http://www.upcitemdb.com'+normalize(''.join(node.xpath('./td/a/@href').extract()))
                name = normalize(''.join(node.xpath('.//td/b/text()').extract()))
                price = normalize(''.join(node.xpath('./td/text()').extract()[-2]))
                date  = normalize(''.join(node.xpath('./td/text()').extract()[-1]))
		values = (dict1.get('UPC-A:',''),link,name,price,date)
		self.execute_query(self.insert_query2, values)
