import sys, os, unittest
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from mongoengine import Document
import models.news

class NewsSpiderTester(unittest.TestCase):
	def test_query(self):		
		total = Article.objects.count()
		self.assertEqual(total, 1)

if __name__ == '__main__':
    unittest.main()