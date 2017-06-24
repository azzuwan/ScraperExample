import sys, os, unittest, datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from models.news import Article

class NewsSpiderTester(unittest.TestCase):	
	def test_insert(self):
		article = Article(title='Test Title', body='Test Body', published= datetime.datetime.utcnow, author='Test Author', agency='Test Agency', url='http://test.com')
		article.tags = ['Test Tag 1', 'Test Tag 2']
		article.save()
		self.article = article
		self.assertIsNotNone(article.id)

	def test_count(self):		
		total = Article.objects.count()
		self.assertEqual(total, 1)

	def test_query(self):
		for article in Article.objects:
			print(article)
		self.assertEqual(Article.objects[0].title, "Test Title")

	def test_delete(self):
		for article in Article.objects:
			article.delete()
		total = Article.objects.count()
		self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()