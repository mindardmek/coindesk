# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SummaryItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    headline = scrapy.Field()
    content_summary = scrapy.Field()
    article_cover = scrapy.Field()

class DetailsItem(scrapy.Item):
    #category = scrapy.Field()
    #headline = scrapy.Field()
    #content_summary = scrapy.Field()
    #article_cover = scrapy.Field()
    authors = scrapy.Field()
    published_date = scrapy.Field()
    updated_date = scrapy.Field(default=None)
    
