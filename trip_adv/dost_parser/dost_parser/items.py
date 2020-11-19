# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class dost(scrapy.Item):
    region = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    tags = scrapy.Field()
    name = scrapy.Field()
