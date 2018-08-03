from fb_constants import *
from fb_browse_queries import *
import sys
sys.path.append('/root/alekhys/automation_pi/table_schemas')
from generic_functions import *

class FacebookReviewBrowse(BaseSpider):
    name = "facebook_review_browse"
    start_urls = ['https://mbasic.facebook.com/escapecinemas/reviews/']

    def parse_review(self, response):
	sel = Selector(response)
	nodes = sel.xpath('//div[@class="bf"]/div/div[not(@class)]')
	for node in nodes:
	    review_by = node.xpath('.//span[@class]/text()').extract()[0]
	    review = ''.join(node.xpath('.//span[not(@class)]/text()').extract())
	    review_on = ''.join(node.xpath('.//abbr/text()').extract())
	    comment = ''.join(node.xpath('.//a[contains(text(), "Comment")]/text()').extract())
	    review_c = ''.join(node.xpath('.//a[contains(text(),"Review")]/text()').extract())
	    likes = ''.join(node.xpath('.//a[@href="#"]/text()').extract())
	    print review_by.encode('utf8')+':'+review.encode('utf8')+':'+review_on.encode('utf8')+':'+comment.encode('utf8')+':'+review_c.encode('utf8')+':'+likes.encode('utf8')
