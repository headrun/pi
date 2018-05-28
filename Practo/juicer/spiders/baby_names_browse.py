from juicer.utils import *

class Babynamesterminal(JuicerSpider):
        name = 'baby_names_browse'
        start_urls = ['https://www.babynamesdirect.com/baby-names/indian/']

        def parse(self, response):
            sel = Selector(response)
            listing_urls = sel.xpath('//div[contains(@class, "alfa tcboy")]//i/a/@href').extract()
            for listing_url in listing_urls:
                yield Request(listing_url, callback=self.parse_next)

        def parse_next(self, response):
            sel = Selector(response)
            alp_urls = sel.xpath('//li[@class="ntr"]//dl/dt/b/a/@href').extract()
            for alp_url in alp_urls:
                sk=''.join(alp_url).split('/')[-1]
                self.get_page('baby_names_terminal',alp_url,sk)
            next_page = sel.xpath('//nav[@class="pages"]/a[@class="next"]/@href').extract()
            if next_page and self.crawl_type=='catchup':
                yield Request(''.join(next_page), callback=self.parse_next)


