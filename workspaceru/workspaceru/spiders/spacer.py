import scrapy


class SpacerSpider(scrapy.Spider):
    name = 'spacer'
    allowed_domains = ['https://workspace.ru/contractors/']
    start_urls = ['http://https://workspace.ru/contractors//']

    def parse(self, response):
        pass
