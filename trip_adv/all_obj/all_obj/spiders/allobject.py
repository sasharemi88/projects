import json

import scrapy
from all_obj.items import TourObject
from datetime import datetime
import re


OBJECT_TYPES = {'HOTEL': 'Отели', 'ATTRACTION': 'Достопримечательности',
                'EATERY': 'Рестораны'}


class AllObjectSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = [
        'https://www.tripadvisor.ru/Tourism-g298484-Moscow_Central_Russia-Vacations.html'
        # 'https://www.tripadvisor.ru/Tourism-g798123-Lipetsk_Lipetsk_Oblast_Central_Russia-Vacations.html'
    ]

    parse_date = datetime.date(datetime.today())
    domain = "https://www.tripadvisor.ru"

    def parse(self, response):
        # Парсинг отелей
        hotels_url = response.xpath("//a[@title='Отели']/@href").get()
        yield response.follow(hotels_url, callback=self.parse_hotels)

        # Парсинг развлечений (достопримечательности)
        attraction_url = response.xpath("//a[@title='Развлечения']/@href").get()
        attraction_url = re.sub(r'Activities(-)', r'\g<0>a_allAttractions.true-', attraction_url)
        yield response.follow(attraction_url, callback=self.parse_attraction)

        # Парсинг ресторанов
        restaurants_url = response.xpath("//a[@title='Рестораны']/@href").get()
        yield response.follow(restaurants_url, callback=self.parse_restaurants)

    # Парсим отели
    def parse_hotels(self, response):
        for obj_link in response.xpath(
                '//div[@class="listing_title"]/a[@class="property_title prominent "]/@href').extract():
            yield response.follow(obj_link, callback=self.parse_obj)

        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_hotels)

    # Парсим достопримечательности
    def parse_attraction(self, response):
        for obj_link in response.xpath('//h2/../@href').extract():
            yield response.follow(obj_link, callback=self.parse_obj)

        next_page = response.xpath("//a[text()='Далее']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_attraction)

    # Парсим рестораны
    def parse_restaurants(self, response):
        for obj_link in response.xpath('//a[@class="_15_ydu6b"]/@href').extract():
            yield response.follow(obj_link, callback=self.parse_obj)

        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_restaurants)

    def parse_obj(self, response):
        obj = TourObject()

        # Выдергиваем из текста страницы json с последними объектами и берем 1 из них
        try:
            entity = json.loads(
                re.search(r'recentHistoryList.+?(\[.+?)\)', response.text)[1]
            )[0]
        except:
            print()

        # Категория, подкатегория
        category = OBJECT_TYPES[entity['type']]
        subcategory = ''
        if category == 'Достопримечательности':
            subcategory = response.xpath(
                "//li[@class='expandSubItemDust secondLevelSubNav']"
                "/span/a[contains(text(), city)]/text()").get()
            subcategory = subcategory.split(': ')[1]

        # Адрес
        address = response.xpath('//span[contains(@class, "ui_icon map-pin")]'
                                 '/following-sibling::span//text()').get()

        # Координаты
        coords = entity.get('coords')
        if coords:
            lat = entity['coords'].split(',')[0]
            lon = entity['coords'].split(',')[1]
        else:
            lat, lon = '', ''

        name = entity['details']['name']

        # Регион, город
        geo = entity['name'].replace(name + ', ', '')
        geo = geo.split(',')

        obj["с0_id"] = entity['value']
        obj["с1_region"] = ','.join(geo[1:]).strip()
        obj["с2_city"] = geo[0]
        obj["с3_category"] = category
        obj["с4_subcategory"] = subcategory
        obj["с5_tags"] = ''
        obj["с6_name"] = name
        # obj["с6_name"] = response.xpath('//h1[@class="_1mTlpMC3"]/text()').get()
        obj["с7_adress"] = address or ''
        obj["с8_latitude"] = lat
        obj["с9_longitude"] = lon
        obj["с10_date"] = self.parse_date

        yield obj
