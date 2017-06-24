import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from models.news import Article
import datetime

class NewsSpider(CrawlSpider):
	name = "newsspider"	
	start_urls = ["http://www.bbc.com"]
	
	# Since BBC is using RESTful and pretty url schema, 
	# we just need to crawl for http://www.bbc.com/news/xxx links
	# from the main page.
	rules = (Rule(LinkExtractor(allow=('/news/+.',)), callback='parse_item'),)
	
	def parse_item(self, res):				
		title = self.get_title(res)
		if title != None:						
			article = Article()
			article.url = res.url 
			article.title=title
			article.body= self.get_body(res)
			article.published= self.get_published(res)
			article.author= self.get_author(res)
			article.agency= self.get_agency(res)
			self.print_response(article)
			try:
				yield article.save()
			except Exception, e:
				print 'Unable to save Article in database: ', e
			return None

	def print_response(self, article):
		print '\n\n'
		print "URL: " + article.url
		print "TITLE: " + article.title
		print 'PUBLISHED: ' + article.published.strftime('%d, %b %Y')
		print "BODY:"			
		print article.body
		print '\n\n'

	def get_title(self, res):
		title = res.css('h1.story-body__h1 ::text').extract_first()
		return title

	def get_body(self, res):
		raw = res.css('div.story-body__inner p ::text')
		body =  ''.join(raw.extract())
		return body

	def get_published(self, res):
		timestamp = res.css('div.story-body div.date ::attr(data-seconds)').extract_first()		
		published = datetime.datetime.fromtimestamp(int(timestamp))
		return published

	def get_author(self, res):
		return 'bbc'

	def get_agency(self, res):
		return 'bbc'