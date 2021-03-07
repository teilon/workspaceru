import scrapy


class WorkspaceCrawlerSpider(scrapy.Spider):
    name = 'workspace_crawler'
    allowed_domains = ['workspace.ru']
    start_urls = ['https://workspace.ru/contractors']

    def parse(self, response):
        categories = response.xpath("//div[@class='categories__item']//div[@class='categories__card']")
        for category in categories:
            category_name = category.xpath(".//span[@class='categories__card-title']/text()").get()
            
            cats = category.xpath(".//ul[@class='categories__card-list']/li")
            for cat in cats:
                link = cat.xpath("/a/@href").get()

                link_name = cat.xpath("/a/text()").get()
                yield {
                    'cat': category_name,
                    'link': link_name
                }

                # yield response.follow(url=link, callback=self.parse_cats, meta={'category_name': category_name})
    
    def parse_cats(self, responce):
        pass
