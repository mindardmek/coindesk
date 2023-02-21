import scrapy
from bitcoin.items import SummaryItem, DetailsItem
from scrapy.loader import ItemLoader



class BitcoinSpider(scrapy.Spider):
    name = 'btc_spider2'
    allowed_domains = ['coindesk.com']
    start_urls = ['https://coindesk.com/tag/bitcoin/1/']

    def parse(self, response):
        article_cards = response.xpath('//div[contains(@class, "hKWAzg")]')

        for article in article_cards:
            category = article.xpath('.//a[@class="category"]/text()').get()
            #if article.xpath('.//a[@class="category"]/text()').get() != 'Podcasts':
            if category != 'Podcasts':
                loader1 = ItemLoader(item=SummaryItem(), selector=article)
                article_url = article.xpath('.//h6[contains(@class,"gGbIdf")]/a/@href').get()
                loader1.add_xpath('article_cover', './/div[@class="img-block"][not(ancestor::div[@class="under-headline-img"])]//img/@src')
                loader1.add_value('category', category)
                loader1.add_xpath('headline', './/a[@class="card-title"]/text()')
                loader1.add_xpath('content_summary', './/span[@class="content-text"]/text()')
                loader1.add_value('meta', {'item': loader1.load_item()})

            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article, meta={'items': loader1.load_item()})


    def parse_article(self, response):
        items =response.meta['items']
        authors_block = response.xpath('//div[contains(@class,"cnfQcl")]/following-sibling::div[@class="authors-block"]')
        names = authors_block.xpath('.//div[@class="name"]//text()').getall()
        socials = authors_block.xpath('.//a[contains(@target, "_blank")]/@href').getall()
        authors = dict(zip(names, socials))

        publishing = response.xpath('//div[@class="at-row"]')
        loader2 = ItemLoader(item=DetailsItem(), selector=publishing, meta={'items': items})
        loader2.add_xpath('published_date','.//div[contains(@class,"at-created")]//text()')
        loader2.add_xpath('updated_date', './/div[@class="at-updated"]//text()')[-1]
        loader2.add_value('authors', authors)
        #loader2.add_value('items', items)
        yield loader2.load_item()