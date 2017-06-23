import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse		

class NewsSpider(CrawlSpider):
	name = "newsspider"
	start_urls = ["http://www.bbc.com"]
	rules = (		
		Rule(LinkExtractor(allow=('/news/?',)), callback='parse_item'),
	)
	def parse_item(self, res):
		print(res.url)
		print(res.css('h1.story-body__h1 ::text').extract_first())
		raw = res.css('div.story-body__inner p ::text')
		body = ''.join(raw.extract())
		print(body)
		print('\n\n')
