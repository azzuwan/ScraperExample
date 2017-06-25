# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from readability import Document
import datetime
from pprint import pprint

class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    published = scrapy.Field()
    body = scrapy.Field()
    agency = scrapy.Field()

class BbcSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['http://bbc.com/news']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    def parse_item(self, res):        
        title = self.get_title(res)
        article = Article()        
        # Only do further processing if there is a title element in the page
        if title != None:             
            # Readability sanitization not implemented because it sucks
            # The hand tuned selectors are already way cleaner and useful 
            # res = self.sanitize(res)
            self.sanitize(res)
            article = Article()
            article['url'] = res.url 
            article['title']=title
            article['body']= self.get_body(res)
            article['published']= self.get_published(res)
            article['author']= self.get_author(res)
            article['agency']= self.get_agency(res)
            # self.log(article)           
            return article
        else:
            return None

    def sanitize(self, res):
        """
        Using readability to clean up content from the response.
        This method is not fully implemented.
        """        
        res._set_body(bytes(doc))
        return res

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
