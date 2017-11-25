from juicer.utils import *

def extract_data(data, path, delem=''):
    return delem.join(data.select(path).extract()).strip()

def extract_list_data(data, path):
    return data.select(path).extract()

def get_nodes(data, path):
    return data.select(path)

domain_url = 'http://www.glassdoor.co.in'

class GlasdoorReviews(JuicerSpider):
    name = 'glassdoor_reviews'
    allowed_domains = ['www.glassdoor.co.in']
    start_urls = ['http://www.glassdoor.co.in/Reviews/ITC-Infotech-India-Reviews-E19730.htm?sort.sortType=RD&sort.ascending=false', 'http://www.glassdoor.co.in/Reviews/ITC-Infotech-Reviews-E31854.htm?sort.sortType=RD&sort.ascending=false']

    def parse(self, response):
        sel = HTML(response)

        if self.latest_dt:
            self.latest_dt = parse_date(self.latest_dt.strftime("%Y-%m-%d"))
        else:
            self.latest_dt = parse_date(self._latest_dt.strftime("%Y-%m-%d"))

        company_name = extract_data(sel, '//div[@class="header cell info"]/p[@class="h1 strong tightAll"]/text()')
        review_nodes = get_nodes(sel, '//div[@class="pad"]//ol[@class="empReviews tightLt"]//li[contains(@id, "empReview_")]')

        next_page = ''
        for review_node in review_nodes:
            _date = extract_data(review_node, './/time/@datetime')
            if not _date:
                continue
            _date = parse_date(_date)

            if _date <= self.latest_dt:
                continue

            self.update_dt(_date)

            review_id = extract_data(review_node, './@id').split('_')[1]
            title = extract_data(review_node, './/div[@class="tbl fill padTop"]//h2[contains(@class, "summary")]//span[@class="summary "]/text()')

            title = company_name + " :: " + title
            review_url = domain_url + extract_data(review_node, './/div[@class="tbl fill padTop"]//h2[contains(@class, "summary")]//a/@href')
            author = extract_list_data(review_node, './/span[contains(@class, "authorJobTitle")]//text()')[:2]
            text = extract_data(review_node, './/div[@class="description"]//div[contains(@class,"prosConsAdvice")]//text()')

            next_page = extract_data(sel, '//li[@class="next"]/a/@href')

            item = Item(response)
            item.set('url', textify(review_url))
            item.set('title', textify(title))
            item.set('author.name', textify(author))
            item.set('dt_added', _date)
            item.set('sk', str(textify(review_id)))
            item.set('text', textify(text))

            yield item.process()

        if next_page:
            next_page = urlparse.urljoin(response.url, next_page)
            yield Request(next_page, callback=self.parse)
