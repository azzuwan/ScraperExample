# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from readability import Document
import datetime
from pprint import pprint

class Articles(scrapy.Item):
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
            article = Articles()
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

    def get_title(self, res):
        """
        Get the title of the article
        """
        title = res.css('h1.story-body__h1 ::text').extract_first()
        return title

    def get_body(self, res):
        """
        Get the actual text of the article
        """
        raw = res.css('div.story-body__inner p ::text')
        body =  ''.join(raw.extract())
        return body

    def get_published(self, res):
        """
        Get the article timestamp
        """
        timestamp = res.css('div.story-body div.date ::attr(data-seconds)').extract_first()     
        published = datetime.datetime.fromtimestamp(int(timestamp))
        return published

    def get_author(self, res):
        """
        Get the author of the article. BBC is somewhat shy about putting a name  on articles
        So we just return the string "bbc"        
        """
        return 'bbc'

    def get_agency(self, res):
        """
        Get the agency name
        """
        return 'bbc'
