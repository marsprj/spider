from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor
from douban.items import MovieItem

class MovieSpider(CrawlSpider):
	name = 'book'
	allow_domains = [
		'douban.com',
	]

	start_urls = [
		'https://book.douban.com/tag/',
	]

	rules = [
		Rule(LinkExtractor(allow=('/tag/$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+/?$')), follow=True),
		Rule(LinkExtractor(allow=('https://book.douban.com/subject/\d+/$')), callback='parse_movie'),
	]
	
	def parse_book(self, response):
		x = Selector(response)
		
		item = MovieItem()
		#item['subject_id'] = response.url.split("/")[-1]
		#item['url'] = response.url
		item['name'] = ''.join(x.xpath('//*[@id="content"]/h1/span[1]/text()').extract()).strip()
		item['director'] = ''.join(x.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()).strip()
		item['editor'] = ''.join(x.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract()).strip()
		item['actors'] = ''.join(x.css('.actor .attrs').xpath('a/text()').extract())
		item['mtype'] = ''.join(x.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract())
		#item['country'] = ''.join(x.xpath('//*[@id="info"]/text()[3]').extract()).strip()
		item['country'] = ''.join(x.xpath('//*[@id="info"]/span[8]/text()').extract()).strip()
		item['language'] = ''.join(x.xpath('//*[@id="info"]/text()[4]').extract()).strip()
		item['issue'] = ''.join(x.xpath('//*[@id="info"]/span[12]/text()').extract()).strip()
		item['year'] = ''.join(x.xpath('//*[@id="content"]/h1/span[2]/text()').extract()).strip()[1:-1]
		#item['abstract'] = ''.join(x.xpath('//*[@id="link-report"]/span[1]/text()').extract()).strip()
		item['abstract'] = ''.join(x.xpath('//*[@id="link-report"]/span[1]/text()').extract()).strip()
		item['rating'] = ''.join(x.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()).strip()
		item['rating_people'] = ''.join(x.css('.rating_people').xpath('span/text()').extract()).strip()

		yield item
		
