# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LinkedinItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sk          = Field()
    profile_sk 	= Field()
    connections_profile_url = Field()
    member_id   = Field()
    headline	= Field()
    name        = Field()
    image_url       = Field()
    image_path 	= Field()
    aux_info    = Field()
    reference_url = Field()
class Linkedinaccounts(Item):
    profile_sk 	= Field()
    status	= Field()
    username	= Field()
    password	= Field()
    aux_info	= Field()
    reference_url = Field()

class ImageItem(Item):
    image_urls = Field()
    images = Field()
