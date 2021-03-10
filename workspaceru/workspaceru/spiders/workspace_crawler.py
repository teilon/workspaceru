import scrapy
from scrapy_splash import SplashRequest


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
                assert(splash:wait(1))
            end

            splash:set_viewport_full()
            return splash:html()
        end  
    '''
    
    # <a 
    #     href="javascript:void(0)" 
    #     class="box-more__btn" 
    #     id="loadMore" 
    #     data-service-code="crm"
    #     >
    # Загрузить ещё
    # </a>

    # <a 
    #     href="javascript:void(0)" 
    #     class="box-more__btn" 
    #     id="loadMore" 
    #     data-service-code="crm" 
    #     style="display: none;"
    #     >
    # Загрузить ещё
    # </a>

    # <div 
    #     class="alert alert-success green-success"
    #     >
    # Все загрузили
    # </div>

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

                # yield {
                #     'category_name': category_name,
                #     'link_name': link_name,
                #     'link': link,
                # }

                yield response.follow(url=link, callback=self.parse_cats, meta={'category_name': category_name})
    
    def parse_cats(self, responce):
        pass
