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
        if isinstance(item, BestSellers):
            best_seller_values = '#<>#'.join([
                item['product_id'],item.get('name',''), item.get('no_of_reviews', ''),  item.get('star_rating', ''),item.get('price', ''),item.get('rank',''),item.get('week_number', ''),item.get('category', ''), item.get('is_prime', ''),item.get('product_url', ''),item.get('reference_url', '')
            ])
            spider.get_bestsellers_file().write('%s\n' %best_seller_values)
            spider.get_bestsellers_file().flush()

            self.write_item_into_avail_file(item, spider, 'bestseller')

        if isinstance(item, Products):
            product_values = '#<>#'.join([
                item['id'],item.get('name',''), item.get('original_price',''), item.get('discount_price',''), item.get('features', ''),  item.get('description', ''),item.get('item_number', ''),item.get('date_available',''),item.get('best_sellerrank', ''),str(item.get('aux_info', '')),item.get('reference_url', '')
            ])
            spider.get_products_file().write('%s\n' %product_values)
            spider.get_products_file().flush()

            self.write_item_into_avail_file(item, spider, 'products')

        if isinstance(item, RelatedSellers):
            relatedsellers_values = '#<>#'.join([
                item['related_sk'],item.get('product_id',''), item.get('name', ''),  item.get('category', ''),item.get('product_condition', ''),item.get('seller_name',''),item.get('seller_no_of_rating', ''),item.get('seller_rating_percentage', ''),item.get('seller_price',''),item.get('is_prime', ''),str(item.get('aux_info', ''))
            ])
            spider.get_relatedsellers_file().write('%s\n' %relatedsellers_values)
            spider.get_relatedsellers_file().flush()

            self.write_item_into_avail_file(item, spider, 'relatedsellers')
        if isinstance(item, RichMedia):
            richmedia_values = '#<>#'.join([
                item['sk'],item.get('product_id',''), item.get('category', ''),  item.get('size', ''),item.get('dimensions', ''),item.get('image_url',''),item.get('reference_url', ''),str(item.get('aux_info', ''))
            ])
            spider.get_richmedia_file().write('%s\n' %richmedia_values)
            spider.get_richmedia_file().flush()

            self.write_item_into_avail_file(item, spider, 'richmedia')
        if isinstance(item, CustomerReviews):
            customerreviews_values = '#<>#'.join([
                item['sk'],item['product_id'],item.get('name',''), item.get('reviewed_by', ''),  item.get('reviewed_on', ''),item.get('review', ''),item.get('category',''),item.get('review_url', ''),item.get('review_rating', ''),item.get('verified_purchase_flag',''),str(item.get('aux_info', ''))
            ])
            spider.get_customerreviews_file().write('%s\n' %customerreviews_values)
            spider.get_customerreviews_file().flush()

            self.write_item_into_avail_file(item, spider, 'customerreviews')
        if isinstance(item, Twitter):
            twitter_values = '#<>#'.join([
                item['sk'], item.get('screen_name',''), item.get('name',''), item.get('description',''),item.get('location',''),item.get('tweets',''),item.get('following',''),item.get('followers',''),item.get('likes',''),item.get('image',''),item.get('lists',''),item.get('timezone',''), item.get('language',''), item.get('is_verified',''), item.get('twitter_url',''), str(item.get('aux_info', ''))
            ])
            spider.get_twitter_file().write('%s\n' %twitter_values)
            spider.get_twitter_file().flush()
            self.write_item_into_avail_file(item, spider, 'twitter')

        if isinstance(item, Comments):
            comments_values = '#<>#'.join([
                item['sk'], item.get('review_sk',''),  item.get('comment_name',''), item.get('comment_by', ''), item.get('comment_on', ''), item.get('comment',''),item.get('comment_votes',''),str(item.get('aux_info', ''))
            ])
            spider.get_comments_file().write('%s\n' %comments_values)
            spider.get_comments_file().flush()
            self.write_item_into_avail_file(item, spider, 'comments')
        if isinstance(item, Linkedin):
            linkedin_values = '#<>#'.join([
                item['sk'], item.get('name',''), item.get('first_name',''), item.get('last_name',''), item.get('locality',''), item.get('image',''), item.get('member_url',''), item.get('mark',''), item.get('url','')
            ])
            spider.get_linkedin_file().write('%s\n' %linkedin_values)
            spider.get_linkedin_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedin')
        if isinstance(item, Linkedinpostions):
            linkedinpositions_values = '#<>#'.join([
                item['sk'], item['profile_sk'], item.get('title',''), item.get('organization','')
                ])
            spider.get_linkedinpositions_file().write('%s\n' %linkedinpositions_values)
            spider.get_linkedinpositions_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedinpositions')

        if isinstance(item, Linkedinviewers):
            linkedinviewers_values = '#<>#'.join([
                item['sk'], item['profile_sk'], item.get('title',''), item.get('viewer_url',''), item.get('viewer_name',''), item.get('viewer_headline','')
                ])
            spider.get_linkedinviewers_file().write('%s\n' %linkedinviewers_values)
            spider.get_linkedinviewers_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedinviewers')

        return item
