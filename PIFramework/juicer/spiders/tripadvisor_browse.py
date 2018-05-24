from juicer.utils import *
from tripadvisor_input import Company_names

class TripadvisorBrowse(JuicerSpider):
    name = 'tripadvisor_search_browse' 
    start_urls = []
    for company in Company_names :
        start_urls.append('https://www.tripadvisor.in/Search?q='+str(company))

    def __init__(self, *args, **kwargs):
        super(TripadvisorBrowse, self).__init__(*args, **kwargs)
        self.domain = 'https://www.tripadvisor.in'

    def parse(self, response):
        sel = Selector(response)
        links = response.xpath('//div[@class="reviews"]/a/@href').extract()
        for link in links :
            link = self.domain+str(link).replace('?t=1','')
            sk = "-".join(link.split('-')[1:3])
            self.get_page("tripadvisor_search_terminal", link, sk)
               

        offset = "".join(sel.xpath('//a[@class="ui_button pagination-next primary "]//@data-offset').extract())
        if  offset :
            nav_link =  response.url.split('&')[0] + '&o=' + str(offset)         
            yield Request(nav_link, callback=self.parse,dont_filter=True)
        



