# ScraperExample
News site scrapping example using Scrapy &amp; MongoDB

##Usage
scrapy crawl bbc

##Description
This is a Scrapy project with:
- BbcSpider, a spider that crawls the BBC site
- SanitizePipeline, a Readability pipeline item to sanitize input
- MongoPipeline, a MongoDB pipeline item that stores the scrapped items

##Note
SanitizePipeline is not implemented fully because it seems that the fine tuned selectors in the spider produced way more cleaner items than using Readability. Readability consistently failed to recognize important parts of the contents and would require another step of parsing and selecting of the elements it produced. 
