# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiquItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_name = scrapy.Field()
    app_info = scrapy.Field()
