import scrapy
from scrapy_splash import SplashRequest
from time import sleep
from random import randint

# Название
# Сайт
# Тел
# Страна, город
# Основной раздел (пример: Разработка сайтов)
# Подраздел (пример: Сайт под ключ)
# Описание (прим. Вёрстка адаптивных макетов в HTML/CSS/JS))
# Рейтинг SEO-компаний
# Рейтинг агентств контекстной рекламы
# Рейтинг веб-студий 

class WorkspaceCrawlerSpider(scrapy.Spider):
    name = 'workspace_crawler'
    allowed_domains = ['workspace.ru']
    #start_urls = ['https://workspace.ru/contractors']

    show_categories = '''
        function main(splash, args)
            splash:on_request(function(request)
                request:set_header('User-Agent', "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")
            end)

            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end    
    '''
    load_more = '''
        function main(splash, args)
            splash.private_mode_enabled = false
  
	        splash:on_request(function(request)
  	            request:set_header('User-Agent', "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")
            end)

            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
    
            while (true)
            do
                stoped = splash:select(".alert"and".alert-success"and".green-success")
		        if (stoped~=nil)
                then
                    break
                end
    
                a_more = assert(splash:select("#loadMore"))
                a_more:mouse_click()
                assert(splash:wait(2))
            end

            splash:set_viewport_full()
            return splash:html()
        end  
    '''

    def start_requests(self):
        yield SplashRequest(url="https://workspace.ru/contractors",
                            callback=self.parse,
                            endpoint='execute',
                            args={
                                'lua_source': self.show_categories
                            })

    def parse(self, response):
        categories = response.xpath("//div[@class='categories__item']//div[@class='categories__card']")
        for category in categories:
            category_name = category.xpath(".//span[@class='categories__card-title']/text()").get()
            
            cats = category.xpath(".//ul[@class='categories__card-list']/li")
            for cat in cats:
                link = cat.xpath(".//a/@href").get()
                link_name = cat.xpath(".//a/text()").get()

                absolute_url = response.urljoin(link)

                # yield {
                #     'category_name': category_name,
                #     'link_name': link_name,
                #     'link': link,
                # }

                # yield response.follow(url=link, callback=self.parse_cats, meta={'category_name': category_name})
                yield SplashRequest(url=absolute_url,
                                    callback=self.parse_cats,
                                    endpoint='execute',
                                    args={
                                        'lua_source': self.load_more
                                    },
                                    meta={
                                        'category_name': category_name,                                        
                                    })
    
    def parse_cats(self, response):
        category_name = response.meta['category_name']
        items = response.xpath("//div[@class='vacancies__card']")
        for item in items:
            item_link = item.xpath(".//div[@class='vacancies__card-info-title _companies']/a/@href").get()
            item_name = item.xpath(".//div[@class='vacancies__card-info-title _companies']/a/@title").get()
            absolute_url = response.urljoin(item_link)

            sec = randint(50, 120)
            sleep(sec)

            yield{
                'category_name': category_name,
                'comand': item_name,
                'link': absolute_url,                
            }

