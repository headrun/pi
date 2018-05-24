from juicer.utils import *
from juicer.items import *

class AmazonBestsellersbrowse(JuicerSpider):
    name = "amazon_bestsellers_browse"
    start_urls = ['http://www.amazon.in/gp/bestsellers']
    handle_httpstatus_list = [404, 302, 303, 403, 500, 999, 503]

    def __init__(self, *args, **kwargs):
        super(AmazonBestsellersbrowse, self).__init__(*args, **kwargs)
        self.URL = "http://www.amazon.in"
        self.pattern = re.compile(r'dp/(.*)[\?.;_/][.*\?.;_/]')
        self.pattern1 = re.compile(r'dp/(.*)[\?.;_/][.*\?.;_/]?')
        self.pattern2 = re.compile(r'dp/(.*)[\?.;_/]')

    def parse(self, response):
        sel = Selector(response)
        navigation_list = get_nodes(sel,'//ul[contains(@id,"browse")]//ul[li]/li/a')[7:8]
        for nv in navigation_list:
            main_url = extract_data(nv,'./@href')
            main_category = extract_data(nv, './text()')
            if 'http' in main_url:
                yield Request(main_url, callback=self.parse_nexttab, meta={"main_category":main_category,'next_page':''})

    def parse_nexttab(self, response):
        sel = Selector(response)
        fortext = response.meta.get('main_category','')
        nexp = response.meta.get('next_page','')
        if not nexp:
            fortext = response.meta['main_category']
            another_nav = get_nodes(sel,'//ul[contains(@id,"browse")]//li[span[contains(text(),"%s")]]/following-sibling::ul/li/a'%fortext)
            for av in another_nav:
                main_url = extract_data(av,'./@href')
                main_category = extract_data(av, './text()')
                if 'http' in main_url: yield Request(main_url, callback=self.parse_nexttab, meta={"main_category":main_category,"next_page":''},dont_filter=True)
             
        if 'Sunglasses & Spectacle Frames' in fortext.encode('utf8') or 'Sunglasses' in fortext.encode('utf8') or 'Spectacle Frames' in fortext.encode('utf8'):

            nodes = get_nodes(sel,'//div[@class="zg_itemImmersion"]')
            for nd in nodes:
                rank = extract_data(nd,'.//span[contains(@class,"rankNumber")]//text()')
                product_link = extract_data(nd,'.//div[@class][a[div[img[@alt]]]]/a/@href')
                stars_rating = extract_data(nd, './/a[contains(@title,"stars")]/@title')
                price = extract_data(nd,'.//span[contains(@class,"price")]/text()')
                prime_icon = extract_data(nd,'.//i[contains(@class,"icon-prime")]/text()')
                product_title =  extract_data(nd,'.//div[@class][a[div[img[@alt]]]]/a/div/img/@alt')
                sk = textify(self.pattern.findall(product_link))
                if not sk: sk = textify(self.pattern1.findall(product_link))
                if not sk: sk = textify(self.pattern2.findall(product_link))
                no_of_reviews = extract_data(nd,'.//div[contains(@class,"spacing-none")]/a[not(@title)][contains(@class,"small")]/text()')
                if product_link and not sk: print product_link,"sk missing"
                stars_ratings = textify(re.findall('(.*?) out',stars_rating))
                is_pri = ''
                if prime_icon: is_pri = True
                if '/ref' in sk : continue
                if sk and product_link:
                    product_link = "%s%s"%(self.URL,product_link)
                    best_sellers = BestSellers()
                    best_sellers.update({"product_id":normalize(sk),"name":normalize(product_title),"star_rating":normalize(stars_ratings),"no_of_reviews":normalize(no_of_reviews),"price":normalize(price),"rank":normalize(rank.strip('.')),"week_number":str(datetime.datetime.now().isocalendar()[1]),"category":normalize(fortext),"is_prime":is_pri,"product_url":normalize(product_link),"reference_url":normalize(response.url)})
                    yield best_sellers
                    aux_info = {"category":fortext,"product_title":product_title}
                    print product_link
                    if '/ref' in sk : continue
                    self.get_page('amazon_bestsellers_terminal', product_link, sk, aux_info)
            navigation = extract_data(sel,'//ol[contains(@class,"pagination")]/li[contains(@class,"selected")]/following-sibling::li[1]/a/@href')
            if navigation:
                yield Request(navigation, callback=self.parse_nexttab,meta={"main_category":fortext,"next_page":'yes'})

