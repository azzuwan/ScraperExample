import sys, os, unittest
sys.path.insert(0, os.path.abspath('__file__'))
import models.news
# connect(host='mongodb://<username>:<password>@aws-ap-southeast-1-portal.2.dblayer.com:15496,aws-ap-southeast-1-portal.0.dblayer.com:15496/admin?ssl=true')
class NewsSpiderTester(unittest.TestCase):
	def test_query(self):		
		total = Article.objects.count()
		self.assertEqual(total, 1)


if __name__ == '__main__':
    unittest.main()