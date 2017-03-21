# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YifySubtitles(scrapy.Item):
    imdb_id = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    language = scrapy.Field()
    name = scrapy.Field()
    file_urls = scrapy.Field()
