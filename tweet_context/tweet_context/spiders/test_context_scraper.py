import os, scrapy, requests
from tweet_context.items import TweetContextItem

class TestContextSpider(scrapy.Spider):
	name = "shenghao"
	urls_dir = './'
	# urls_filename = 'expanded_urls.txt'
	urls_filename = 'final_urls.txt'
	tweet_ids = []
	start_urls = []

	with open(os.path.join(urls_dir, urls_filename), 'r') as f:
		for i, line in enumerate(f):
			id_url_pair = line.split('\t')
			tweet_ids.append(id_url_pair[0])
			final_url = id_url_pair[1].replace('\n', '')
			start_urls.append(final_url)
		print(start_urls)
		f.close()

	def parse(self, response):
		# time.sleep(1)
		tweet_id = self.tweet_ids[self.start_urls.index(response.url)]
		new_callback = lambda response: self.parse_context(response, tweet_id)
		yield scrapy.Request(response.url, callback=new_callback)

		# for url in self.start_urls:
		# 	tweet_id = self.tweet_ids[self.start_urls.index(url)]
		# 	print("*******************" + str(tweet_id))
		# 	new_callback = lambda response: self.parse_context(response, tweet_id)
		# 	yield scrapy.Request(url, callback=new_callback)

		# for j, url in enumerate(self.start_urls):
		# 	tweet_id = self.tweet_ids[j]
		# 	time.sleep(5)
		# 	new_callback = lambda response: self.parse_context(response, tweet_id)
		# 	yield scrapy.Request(url, callback=new_callback)

		

	def parse_context(self, response, id):
		item = TweetContextItem()
		item['tweetId'] = id
		item['contextTitle'] = response.xpath("//head//title/text()").extract_first()

		yield item
