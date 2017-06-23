from mongoengine import connect

connect(host='mongodb://<username>:<password>@aws-ap-southeast-1-portal.2.dblayer.com:15496,aws-ap-southeast-1-portal.0.dblayer.com:15496/admin?ssl=true')

class Article(Document):
	# The title of the news article
	title = StringField(required=True)
	# News content	
	body = StringField(required=True)
	# Publication date
	published = DateTimeField()
	# Article author 
	author = StringField()
	# Category tags
	tags = ListField(StringField())
	# News agency name
	agency = StringField(required=True)
	# Original URL of the article
	url = StringField(required=True)