import scrapy
from urllib.parse import urljoin
from dost_parser.items import dost

class DostSpider2(scrapy.Spider):
    name = 'DostSpider2'
    allowed_domains = ["www.tripadvisor.ru"]
    pgn = 30
    start_urls = ["https://www.tripadvisor.ru/Attractions-g2324055-Activities-oa30-Samara_Oblast_Volga_District.html"]

    visited_urls = []    
    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            for obj_link in response.xpath('//a[@class="_1QKQOve4"]/@href').extract():
                url = urljoin("https://www.tripadvisor.ru", obj_link)

                yield response.follow(url, callback=self.parse_obj)
            self.pgn = self.pgn + 30            
            next_page_url = "https://www.tripadvisor.ru/Attractions-g2324055-Activities-oa" + str(self.pgn) + "-Samara_Oblast_Volga_District.html"
            print("Next page: ", next_page_url)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_obj(self, response):   
        obj = dost()
        obj["region"] = response.xpath('//li[@class="breadcrumb"][4]/a/span/text()').get()
        city = response.xpath('//li[@class="breadcrumb"][5]/a/span/text()').get()
        obj["city"] = city
        obj["category"] = 'Достопримечательности'
        subcat = str( response.xpath("//li[@class='expandSubItemDust secondLevelSubNav']/span/a[contains(text(), city)]/text()").get())
        obj["subcategory"] = subcat.split(': ')[1]
        tags = response.xpath('//a[@class="_1cn4vjE4"]/text()').extract()
        obj["tags"] = list(set(tags))
        obj["name"] =  response.xpath('//h1[@class="ui_header h1"]/text()').get() 
        yield obj     