from models.news import Article
import datetime

class GuardianParser():
	def parse(self, res):
		title = self.get_title(res)
		if title != None:						
			article = Article()
			article.url = res.url 
			article.title=title
			article.body= self.get_body(res)
			article.published= self.get_published(res)
			article.author= self.get_author(res)
			article.agency= self.get_agency(res)
			self.log(article)
			return article
	
	def get_title(self, res):
		title = res.css('#article.content__headline ::text').extract_first()
		return title

	def get_body(self, res):
		raw = res.css('#article.content__article-body p ::text')
		body =  ''.join(raw.extract())
		return body

	def get_published(self, res):
		timestamp = res.css('time.content__dateline-wpd ::attr(data-timestamp)').extract_first()		
		published = datetime.datetime.fromtimestamp(int(timestamp))
		return published

	def get_author(self, res):
		author = res.css('a[rel="author"] span ::text')
		return author

	def get_agency(self, res):
		return 'guardian'

	def log(self, article):
		print ('\n\n')
		print ("URL: " + article.url)
		print ("TITLE: " + article.title)
		print ('PUBLISHED: ' + article.published.strftime('%d, %b %Y'))
		print ("BODY:")
		print (article.body)
		print ('\n\n')