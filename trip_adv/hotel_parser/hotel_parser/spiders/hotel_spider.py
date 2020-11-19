import scrapy
from urllib.parse import urljoin
from hotel_parser.items import Hotel
from datetime import datetime
import requests
import re

class HotelSpider(scrapy.Spider):
    name = 'HotelSpider'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = ["https://www.tripadvisor.ru/Hotels-g2324055-Samara_Oblast_Volga_District-Hotels.html"]
    parse_date = datetime.date(datetime.today())    
    visited_urls = []   
    
    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            for obj_link in response.xpath('//div[@class="listing_title"]/a[@class="property_title prominent "]/@href').extract():
                url = urljoin("https://www.tripadvisor.ru", obj_link)
                print(url)
                yield response.follow(url, callback=self.parse_obj)
            
            next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
            next_page_url = urljoin("https://www.tripadvisor.ru", next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_obj(self, response):
        obj = Hotel()
        obj["region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
        obj["city"] = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
        obj["category"] = 'Отели'
        obj["subcategory"] = ''
        obj["tags"] = ''
        obj["name"] =  response.xpath('//h1[@class="_1mTlpMC3"]/text()').get() 
        obj["adress"] = response.xpath('//span[@class="_3ErVArsu jke2_wbp"]/text()').get() 
        r = requests.get(response.url)
        coor_pat = re.compile('"coords":"\d+.\d+,\d+.\d+"')
        coor = coor_pat.search(r.text).group(0).split(':')[1].replace('"', '')
        lat = coor.split(',')[0]
        lon = coor.split(',')[1] 
        obj["latitude"] = lat
        obj["longitude"] = lon  
        obj["date"] = self.parse_date          
        yield obj     