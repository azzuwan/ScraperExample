import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from models.news import Article
from parsers.bbc import BBCParser
from parsers.guardian import GuardianParser
import datetime

class NewsSpider(CrawlSpider):
	name = "newsspider"	
	bbc = "http://www.bbc.com"
	guardian = "https://www.theguardian.com/world"
	# start_urls = [bbc, guardian]
	start_urls = [bbc]
	# start_urls = [guardian]
	allowed_domains =["bbc.com", "bbc.co.uk", "theguardian.com"]
	
	bbc_parser = BBCParser()
	guardian_parser = GuardianParser()	
	
	rules = (
		# Since BBC is using RESTful and pretty url schema, 
		# we just need to crawl for http://www.bbc.com/news/xxx links
		# from the main page.
		# Rule(LinkExtractor(allow=('/news/+.',)), callback='parse_item'),		
		Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),		
		# Guardian top level news links are clasified into regional sections
		# Rule(LinkExtractor(allow=(guardian +'/+.',)), callback='parse_item'),
		)
	# Entry point and main callback for Scrapy
	def parse_item(self, res):
		# Here the all the major processing steps are made obvious and simplified. 
		# We segregated the process into
		# 1) Parsing factory that allows us to add more parsers in the future
		# 2) Database insertion operation		
		
		# Parsing handler that loads site dependent parsers
		article = yield self.parse(res)
		
		# Sanitizer will go here 
		# Mercury / Readability is not implemented here because it sucks
		# Data from hand tuned crawler is cleaner and more complete 
		# Implementing it only adds more noise with zero gain

		# Save processed article to Compose MongoDB instances
		yield self.save(article)
		return None

	# Our parser factory
	def parse(self, res):
		article = None
		if self.bbc in res.url:
			print ("BBBBBBBBBBBBBBBBBBBS")
			try:			
				article = yield self.bbc_parser.parse(res)
			except Exception as e:
				print("BBC content parsing error: ", e)
		else:
			print ("GGGGGGGGGGGGGGGGGGG")
			try:
				article = yield self.guardian_parser.parse(res)
			except Exception as e:
				print("Guardian content parsing error: ", e)
		return article

	# Saves processed articles into MongoDB
	def save(self, article):		
		try:
			yield article.save()
		except Exception as e:
			print ('Unable to save Article in database: ', e)

