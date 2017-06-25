# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime

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

    # def parse_item(self, response):
    #     i = {}
    #     #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
    #     #i['name'] = response.xpath('//div[@id="name"]').extract()
    #     #i['description'] = response.xpath('//div[@id="description"]').extract()
    #     return i
    def parse_item(self, res):               
        title = self.get_title(res)
        article = Article()
        print("TTTTTTTTTT")
        if title != None:                       
            print("OOOOOOOOOOOOO")
            article = Article()
            article['url'] = res.url 
            article['title']=title
            article['body']= self.get_body(res)
            article['published']= self.get_published(res)
            article['author']= self.get_author(res)
            article['agency']= self.get_agency(res)
            self.log(article)           
        return article
    
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
