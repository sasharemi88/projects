# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TourObject(scrapy.Item):   
    с1_region = scrapy.Field()
    с2_city = scrapy.Field()
    с3_category = scrapy.Field()
    с4_subcategory = scrapy.Field()
    с5_tags = scrapy.Field()
    с6_name = scrapy.Field()
    с7_adress = scrapy.Field()
    с8_latitude = scrapy.Field()
    с9_longitude = scrapy.Field()
    с10_date = scrapy.Field()
