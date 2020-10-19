import scrapy
from urllib.parse import urljoin
from obj_parse.items import Hotel

class HotelSpider(scrapy.Spider):
    name = 'HotelSpider'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = ["https://www.tripadvisor.ru/Restaurants-g2324049-Nizhny_Novgorod_Oblast_Volga_District.html"]

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
        yield obj     