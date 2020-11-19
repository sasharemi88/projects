import scrapy
from urllib.parse import urljoin
from obj_parse.items import TourObject

class ObjectsSpider(scrapy.Spider):
    name = 'ObjectsSpider'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = ["https://www.tripadvisor.ru/Restaurants-g2324055-Samara_Oblast_Volga_District.html"]

    visited_urls = []
    subcat = ['Рестораны', 'Быстрые перекусы', 'Фастфуд', 'Десерты', 'Кофе и чай', 'Бар', 'Паб', 'Кафе', 'Булочные', 'Гастропаб']
    def parse(self, response):
        top = 'Топ ресторан - ' +  response.xpath('//a[@class="_15_ydu6b"][1]/text()').get()
        print(top)
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            for obj_link in response.xpath('//a[@class="_15_ydu6b"]/@href').extract():
                url = urljoin("https://www.tripadvisor.ru", obj_link)
                print(url)
                yield response.follow(url, callback=self.parse_obj)
            
            next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
            next_page_url = urljoin("https://www.tripadvisor.ru", next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_obj(self, response):
        obj = TourObject()
        obj["region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
        obj["city"] = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
        obj["category"] = 'Рестораны'
        obj_tags = response.xpath('//a[@class="_2mn01bsa"]/text()').extract()
        tags = [i for i in obj_tags if i in self.subcat]        
        obj["subcategory"] = ''
        obj["tags"] = tags
        obj["name"] =  response.xpath('//h1[@class="_3a1XQ88S"]/text()').get() 
        yield obj     