import scrapy
from bitcoin.items import SummaryItem, DetailsItem
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class BitcoinSpider(scrapy.Spider):
    name = 'btc_spider'
    allowed_domains = ['coindesk.com']
    start_urls = ['https://coindesk.com/tag/bitcoin/1/']

    def parse(self, response):
        article_cards = response.xpath('//div[contains(@class, "hKWAzg")]')

        for article in article_cards:
            category = article.xpath('.//a[@class="category"]/text()').get()
            loader1 = ItemLoader(item=SummaryItem(), selector=article)

            if category != 'Podcasts':
                article_url = article.xpath('.//h6[contains(@class,"gGbIdf")]/a/@href').get()
                loader1.add_xpath('article_cover', './/div[@class="img-block"][not(ancestor::div[@class="under-headline-img"])]//img/@src')
                loader1.add_value('category', category)
                loader1.add_xpath('headline', './/a[@class="card-title"]/text()')
                loader1.add_xpath('content_summary', './/span[@class="content-text"]/text()')
            
                yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article,meta={'items': loader1.load_item()})
        
        last_page = int(response.xpath('(.//li[@class="page-item"]/a)[last()-1]/text()').get())
        for page_number in range(2, 5):#last_page+1):
            next_page = f'https://coindesk.com/tag/bitcoin/{page_number}/'
            yield scrapy.Request(next_page, self.parse)


    def parse_article(self, response):
        items =response.meta['items']
        authors_block = response.xpath('//div[contains(@class,"cnfQcl")]/following-sibling::div[@class="authors-block"]')
        names = authors_block.xpath('.//div[@class="name"]//text()').getall()
        socials = authors_block.xpath('.//a[contains(@target, "_blank")]/@href').getall()
        authors = dict(zip(names, socials))
        #updated_date = authors_block.xpath('.//div[@class="at-updated"]//text()').get()[-1]
        
        

        publishing = response.xpath('//div[@class="at-row"]')
        updated_date = publishing.xpath('.//div[@class="at-updated"]//text()[position()=2]').get()
        loader2 = ItemLoader(item=DetailsItem(), selector=publishing, meta={'items': items})
        
        loader2.add_xpath('published_date','.//div[contains(@class,"at-created")]//text()')
        loader2.add_value('updated_date', updated_date if updated_date is not None else None)
        #loader2.add_value('updated_date', updated_date)
        loader2.add_value('authors', authors)

        for k, v in items.items():
            loader2.add_value(k, v)
        
        yield loader2.load_item()

#process = CrawlerProcess()
#process.crawl(BitcoinSpider)
#process.start()

#response.xpath('(.//li[@class="page-item"]/a)[last()]/@href').get()