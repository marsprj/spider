from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor
from douban.items import MovieItem

class TopMovieSpider(CrawlSpider):
	name = 'topmovie'
	allow_domains = [
		'douban.com',
	]

	start_urls = [
		'https://movie.douban.com/top250',
	]

	rules = [
#		Rule(LinkExtractor(allow=('https://movie.douban.com/top250?start=\d+&filter=')), follow=True),
		Rule(LinkExtractor(allow=('\?start=\d+&filter=')), follow=True),
		Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/$')), callback='parse_movie'),
	]
	
	def parse_movie(self, response):
		x = Selector(response)
		
		item = MovieItem()
		item['name'] = x.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
		item['director'] = x.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
		item['actors'] = ''.join(x.css('.actor .attrs').xpath('a/text()').extract())
		item['year'] = x.xpath('//*[@id="content"]/h1/span[2]/text()').extract()[1:-1]
		item['abstract'] = x.xpath('//*[@id="link-report"]/span[1]/text()').extract()

#		print item['name']

		yield item
		
