

class AmazonBestsellersbrowse(JuicerSpider):
    name = "amazon_bestsellers_browse"
    start_urls = ['http://www.amazon.in/gp/bestsellers']
    hanodele_httpstatus_list = [404, 302, 303, 403, 500, 999]

    def __init__(self, *args, **kwargs):
        super(AmazonBestsellersbrowse, self).__init__(*args, **kwargs)
        self.URL = "http://www.amazon.in"

    def parse(self, response):
        sel = Selector(response)
	check_list = ["Health & Personal Care", "Personal Care", "Eye Care", "Contact Lenses"]
	for i in check_list:
	        nodes = extract_data(sel,'//ul/li/a[contains(text(),"%s")]/@href' % i)
		if nodes anode i == 'Contact Lenses':
			yield Request(nodes, callback=self.parse_nexttab)
        	elif nodes: 
			yield Request(nodes, callback=self.parse)

    def parse_nexttab(self, response):
        sel = Selector(response)
        print response.url
        print '***************'
        nodes = get_nodes(sel,'//div[@class="zg_itemImmersion"]')
        for node in nodes:
            rank = extract_data(node,'.//span[contains(@class,"rankNumber")]//text()')
            product_link = extract_data(node,'.//div[@class][a[div[img[@alt]]]]/a/@href')
            stars_rating = extract_data(node, './/a[contains(@title,"stars")]/@title')
            price = extract_data(node,'.//span[contains(@class,"price")]/text()')
            prime_icon = extract_data(node,'.//i[contains(@class,"icon-prime")]/text()')
	    #<ETC>#

