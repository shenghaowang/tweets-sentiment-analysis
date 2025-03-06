import os

import requests
import scrapy
from tweet_context.items import TweetContextItem


class TweetContextSpider(scrapy.Spider):
    name = "tweet_context_scraper"
    urls_dir = "./"
    # urls_filename = 'expanded_urls.txt'
    urls_filename = "final_urls.txt"
    tweet_ids = []
    start_urls = []

    with open(os.path.join(urls_dir, urls_filename), "r") as f:
        for i, line in enumerate(f):
            id_url_pair = line.split("\t")
            tweet_ids.append(id_url_pair[0])
            final_url = id_url_pair[1].replace("\n", "")
            start_urls.append(final_url)
        print(start_urls)
        f.close()

    def parse(self, response):
        tweet_id = self.tweet_ids[self.start_urls.index(response.url)]
        new_callback = lambda response: self.parse_context(response, tweet_id)
        yield scrapy.Request(response.url, callback=new_callback)

    def parse_context(self, response, id):
        item = TweetContextItem()
        item["tweetId"] = id
        item["contextTitle"] = response.xpath("//head//title/text()").extract_first()

        yield item
