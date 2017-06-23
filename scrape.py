import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import models		

class NewsSpider(CrawlSpider):
	name = "newsspider"
	start_urls = ["http://www.bbc.com"]

	#Just check for http://www.bbc.com/news/xxx  
	rules = (Rule(LinkExtractor(allow=('/news/+.',)), callback='parse_item'),)

	def parse_item(self, res):				
		title = res.css('h1.story-body__h1 ::text').extract_first()			
		if title != None:
			url = res.url
			print('\n\n')
			print("URL: " + url)
			print("TITLE: " + title)
			print("BODY:")
			raw = res.css('div.story-body__inner p ::text')
			body =  ''.join(raw.extract())
			print(body)
			print('\n\n')
