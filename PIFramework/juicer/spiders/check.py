from juicer.utils import *

class wWatsmyipaddr(JuicerSpider):
        name ='whatsmyipaddr_browse'
        start_urls =['https://whatismyipaddress.com/']

        def parse(self,response):
                sel = HTML(response)
                import pdb;pdb.set_trace()
                ip = sel.xpath('//div[@id="main_content"]/div/div/a/text()').extract()[0]
                print ip
