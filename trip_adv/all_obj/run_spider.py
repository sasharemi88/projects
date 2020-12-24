from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# Получение настроек и подготовка к запуску пауков
settings = get_project_settings()
process = CrawlerProcess(settings)

process.crawl('tripadvisor')
process.start()
