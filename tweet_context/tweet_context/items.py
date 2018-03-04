# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TweetContextItem(scrapy.Item):
    tweetId = scrapy.Field()
    contextTitle = scrapy.Field()