
import re
import json
import datetime
from copy import deepcopy
from juicer.items import *

from json_validator import validate_json_record


SOURCES_LIST = {}


class JuicerPipeline(object):

    def get_source(self, spider):
        return spider.name.split('_', 1)[0].strip()


    def write_item_into_avail_file(self, item, spider, content_type):
        source = self.get_source(spider)

        if SOURCES_LIST.has_key(source):
            SOURCES_LIST[source](item, spider.get_avail_file(), spider.get_json_file())

    def process_item(self, item, spider):

		if isinstance(item, AmazonBestSellersItem):
			best_seller_values = '#<>#'.join([
				item['name'], item.get('no_of_reviews', ''),  item.get('star', ''),item.get('price', ''),item.get('rank',''), item.get('is_prime', '') str(item.get('aux_info', '')), item.get('reference_url', '')
			])
			spider.get_best_sellers_file().write('%s\n' %best_sellers_values)
			spider.get_best_sellers_file().flush()

			self.write_item_into_avail_file(item, spider, 'best_seller')


		return item
