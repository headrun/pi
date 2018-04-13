from scrapy.http import FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import Selector

class LinkedIn(BaseSpider):
    name = 'linkedin_browse'
    start_urls = ['https://in.linkedin.com/']

    def parse(self, response):
        sel = Selector(response)
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,fil;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'authority': 'www.linkedin.com',
        }
        link = 'https://www.linkedin.com/pulse-fe/api/v1/followableEntity'
        params = (
            ('vanityName', 'chimango-chikwanda-56a2b7a'),
            )
        yield FormRequest(link, callback = self.parse_next, headers=headers, formdata=params, method='GET')

    def parse_next(self, response):
        import pdb;pdb.set_trace()
