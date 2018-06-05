from juicer.utils import *
from juicer.items import *

class AmazonBestsellersbrowse(JuicerSpider):
    name = "amazon_bestseller_browse"
    start_urls = ['https://www.amazon.in/washing-machines-Dryers-Large-Appliances/s?ie=UTF8&page=1&rh=n%3A1380369031%2Ck%3Awashing%20machines']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(AmazonBestsellersbrowse, self).__init__(*args, **kwargs)
        self.con = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'root', db = 'AMAZON', charset = 'utf8', use_unicode = True)
        self.cur = self.con.cursor()
        self.URL = "http://www.amazon.in"
        self.pattern = re.compile(r'dp/(.*)[\?.;_/][.*\?.;_/]')
        self.pattern1 = re.compile(r'dp/(.*)[\?.;_/][.*\?.;_/]?')
        self.pattern2 = re.compile(r'dp/(.*)[\?.;_/]')


    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="s-item-container"]')
        for node in nodes :
                rank = "".join(node.xpath('./a//span[@class="a-size-base a-color-price s-price a-text-bold"]//text()').extract())
                product_link = node.xpath('.//div[@class="a-row a-spacing-mini"]//a//@href').extract()[0]
                stars_rating = "".join(node.xpath('.//div[@class="a-row a-spacing-none"]//i//span[contains(text(),"stars")]/text()').extract())
                price = "".join(node.xpath('.//div[@class="a-row a-spacing-mini"]//span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract())
                prime_icon = "".join(node.xpath('.//div[@class="a-row a-spacing-mini"]//i[@aria-label="prime"]//text()').extract())
                product_title = "".join(node.xpath('.//a//h2//text()').extract())
                sk = textify(self.pattern.findall(product_link))
                if not sk: sk = textify(self.pattern1.findall(product_link))
                if not sk: sk = textify(self.pattern2.findall(product_link))
                no_of_reviews = "".join(node.xpath('.//div[@class="a-row a-spacing-none"]//a[contains(@href,"customerReviews")]/text()').extract())
                if product_link and not sk: print product_link,"sk missing"
                stars_ratings = textify(re.findall('(.*?) out',stars_rating))
                is_pri = ''
                if prime_icon: is_pri = True
                if '/ref' in sk : sk = sk.split('/')[0]
                if sk and product_link:
                    best_sellers = BestSellers()
                    best_sellers.update({"product_id":str(sk),"name":normalize(product_title),"star_rating":str(stars_ratings),"no_of_reviews":str(no_of_reviews),"price":str(price),"rank":'0',"week_number":str(datetime.datetime.now().isocalendar()[1]),"category":"Home & Kitchen","is_prime":str(is_pri),"product_url":normalize(product_link),"reference_url":normalize(response.url)})
                    yield best_sellers
                    aux_info = {"category":'Home & Kitchen',"product_title":product_title}
                    if '/ref' in sk : sk = sk.split('/')[0]
                    self.get_page('amazon_bestsellers_terminal', product_link, sk, aux_info)
        nav = "".join(sel.xpath('//span[@class="pagnRA"]//a[@class="pagnNext"]//@href').extract())
        if nav : 
            nav_link = self.URL +  nav
            yield Request(nav_link,callback=self.parse)


