import scrapy
from urllib.parse import urljoin

class ObjectsSpider(scrapy.Spider):
    name = 'ObjectsSpider'
    allowed_domains = ["www.tripadvisor.ru"]
    start_urls = ["https://www.tripadvisor.ru/Restaurants-g2324049-Nizhny_Novgorod_Oblast_Volga_District.html"]

    visited_urls = []
    subcat = ['Рестораны', 'Быстрые перекусы', 'Десерты', 'Кофе и чай', 'Бары и клубы', 'Булочные']

    def parse(self, response):
        top = 'Топ ресторан - ' +  response.xpath('//a[@class="_15_ydu6b"][1]/text()').get()
        print(top)
        if response.url not in visited_urls:
            self.visited_urls.append(response.url)
            for obj_link in response.xpath('//a[@class="_15_ydu6b"]/@href').extract():
                url = urljoin("https://www.tripadvisor.ru/", obj_link)
                yield response.follow(url, callback=self.parse_obj)
            
            next_link = response.xpath("//a[contains(@class, 'next')]/@href").get()
            next_page_url = urljoin("https://www.tripadvisor.ru/", next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_obj(self, response):
        obj = Object()
        obj["region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
        obj["city"] = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
        obj["category"] = 'Рестораны'
        tags = []
        for i in response.xpath('//a[@class="_2mn01bsa"]/text()').extract():
            if i in self.subcat:
                tags.append(i)
        obj["subcategory"] = ''
        obj["tags"] = tags
        obj["name"] =  response.xpath('//h1[@class="_3a1XQ88S"]/text()').get() 
        yield obj     