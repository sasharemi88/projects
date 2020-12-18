import scrapy
from urllib.parse import urljoin
from all_obj.items import TourObject
from datetime import datetime
import requests
import re
import time


class AllObjectSpider(scrapy.Spider):
    name = 'AllObjectSpider'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = [
                  "https://www.tripadvisor.ru/Tourism-g2323955-Moscow_Oblast_Central_Russia-Vacations.html"
                  ]
    
    parse_date = datetime.date(datetime.today())
    visited_urls = [] 
    subcat = ['Рестораны', 'Быстрые перекусы', 'Фастфуд', 'Десерты', 'Кофе и чай', 'Бар', 'Паб', 'Кафе', 'Булочные', 'Гастропаб']
    domain = "https://www.tripadvisor.ru"
    pgn = 30
    
    def parse(self, response):
        hotels_page = response.xpath("//a[@title='Отели']/@href").get()
        hotels_page_url = urljoin(self.domain, hotels_page)        
        dost_page = response.xpath("//a[@title='Развлечения']/@href").get()
        dost_page_url = urljoin(self.domain, dost_page)
        reca_page = response.xpath("//a[@title='Рестораны']/@href").get()
        reca_page_url = urljoin(self.domain, reca_page)
        spiders = {hotels_page_url: self.hotels_parse,
                   dost_page_url: self.dost_parse,
                   reca_page_url: self.reca_parse}
        for s in spiders.items():
            yield response.follow(s[0], callback=s[1])

#Парсим отели    
    def hotels_parse(self, response):
         time.sleep(0.1)
         if response.url not in self.visited_urls:
             self.visited_urls.append(response.url)
             for obj_link in response.xpath('//div[@class="listing_title"]/a[@class="property_title prominent "]/@href').extract():
                 url = urljoin(self.domain, obj_link)                
                 yield response.follow(url, callback=self.hotels_parse_obj)
                
             next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
             next_page_url = urljoin(self.domain, next_page)
             yield response.follow(next_page_url, callback=self.hotels_parse)

    def hotels_parse_obj(self, response):
        obj = TourObject()
        id_obj_mask = re.compile("-d\d+")
        id_obj = id_obj_mask.search(response.url)[0].replace('-d','')
        obj["с0_id"] = id_obj 
        obj["с1_region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
        obj["с2_city"] = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
        obj["с3_category"] = 'Отели'
        obj["с4_subcategory"] = ''
        obj["с5_tags"] = ''
        obj["с6_name"] =  response.xpath('//h1[@class="_1mTlpMC3"]/text()').get() 
        obj["с7_adress"] = response.xpath('//div[@class="_1sPw_t0w _3sCS_WGO"]/span[2]/span/text()').get()
        #ищем координаты отеля на карте    
        r = requests.get(response.url)
        coor_pat = re.compile('"coords":"\d+.\d+,\d+.\d+"')
        coor = coor_pat.search(r.text).group(0).split(':')[1].replace('"', '')
        lat = coor.split(',')[0]
        lon = coor.split(',')[1] 
        obj["с8_latitude"] = lat
        obj["с9_longitude"] = lon  
        obj["с10_date"] = self.parse_date          
        yield obj         
        
#Парсим достопримечательности        
    def dost_parse(self, response):
            time.sleep(0.1)            
            if response.url not in self.visited_urls:
                self.visited_urls.append(response.url)
                for obj_link in response.xpath('//a[@class="_255i5rcQ"]/@href').extract():
                    url = urljoin("https://www.tripadvisor.ru", obj_link)
                    yield response.follow(url, callback=self.dost_parse_obj)
            pagination = response.url.split('-Activities-')
            next_page_url = pagination[0] + '-Activities-oa' + str(self.pgn) + pagination[1]
            self.pgn = self.pgn + 30
            yield response.follow(next_page_url, callback=self.dost_parse)
            
    def dost_parse_obj(self, response): 
            obj = TourObject()
            id_obj_mask = re.compile("-d\d+")
            id_obj = id_obj_mask.search(response.url)[0].replace('-d','')
            obj["с0_id"] = id_obj
            #поиск города заменить на  response.xpath("//h1[contains(@class, 'masthead_h1')]/text()").get() + регулярки
            breadcrumbs = response.xpath('//li[@class="breadcrumb"]/a/span/text()').extract()
            if len(breadcrumbs) == 6:
                city = breadcrumbs[4]
            else:
                city = breadcrumbs[3] 
            obj["с1_region"] = breadcrumbs[3]           
            obj["с2_city"] = city
            obj["с3_category"] = 'Достопримечательности'
            subcategory = str(response.xpath("//li[@class='expandSubItemDust secondLevelSubNav']/span/a[contains(text(), city)]/text()").get())
            obj["с4_subcategory"] = subcategory.split(': ')[1]
            tags = response.xpath('//a[@class="_1cn4vjE4"]/text()').extract()
            obj["с5_tags"] = list(set(tags))
            obj["с6_name"] =  response.xpath('//h1[@class="ui_header h1"]/text()').get() 
            obj["с7_adress"] = response.xpath("//div[@class='LjCWTZdN']/span[2]/text()").get()
            #ищем координаты   
            r = requests.get(response.url)
            lat_pat = re.compile('"latitude":"\d+.\d+"')
            lat = lat_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
            lon_pat = re.compile('"longitude":"\d+.\d+"')
            lon = lon_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
            obj["с8_latitude"] = lat
            obj["с9_longitude"] = lon  
            obj["с10_date"] = self.parse_date
            yield obj    
            
#Парсим рестораны
    def reca_parse(self, response):
            time.sleep(0.2)
            if response.url not in self.visited_urls:
                self.visited_urls.append(response.url)
                for obj_link in response.xpath('//a[@class="_15_ydu6b"]/@href').extract():
                    url = urljoin(self.domain, obj_link)
                    print(url)
                    yield response.follow(url, callback=self.reca_parse_obj)
            
            next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
            next_page_url = urljoin(self.domain, next_page)
            yield response.follow(next_page_url, callback=self.reca_parse)
            
    def reca_parse_obj(self, response): 
            obj = TourObject()
            id_obj_mask = re.compile("-d\d+")
            id_obj = id_obj_mask.search(response.url)[0].replace('-d','')
            obj["с0_id"] = id_obj
            obj["с1_region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
            obj["с2_city"] = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
            obj["с3_category"] = 'Рестораны'
            obj_tags = response.xpath('//a[@class="_2mn01bsa"]/text()').extract()
            tags = [i for i in obj_tags if i in self.subcat]        
            obj["с4_subcategory"] = ''
            obj["с5_tags"] = tags
            obj["с6_name"] =  response.xpath('//h1[@class="_3a1XQ88S"]/text()').get() 
            obj["с7_adress"] = response.xpath('//a[@class="_15QfMZ2L"]/text()').get()
            #ищем координаты   
            r = requests.get(response.url)
            lat_pat = re.compile('"latitude":"\d+.\d+"')
            lat = lat_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
            lon_pat = re.compile('"longitude":"\d+.\d+"')
            lon = lon_pat.search(r.text).group(0).split(':')[1].replace('"', '').replace(' ', '')
            obj["с8_latitude"] = lat
            obj["с9_longitude"] = lon  
            obj["с10_date"] = self.parse_date
            yield obj           