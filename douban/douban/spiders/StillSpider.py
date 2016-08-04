# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
from scrapy.linkextractor import LinkExtractor
from douban.items import ImageItem
import string

class MovieSpider(CrawlSpider):
	name = 'still'
	allow_domains = [
		'douban.com',
	]

	start_urls = [
		'https://movie.douban.com/tag/',
		'https://movie.douban.com/subject/1297011/',
		'https://movie.douban.com/tag/%E7%83%82%E7%89%87',
		'https://movie.douban.com/subject/26599625/',
		'https://movie.douban.com/tag/%E7%BA%AA%E5%BD%95%E7%89%87',
		'https://movie.douban.com/subject/10741871/',
		'https://movie.douban.com/celebrity/1049485/',
		'https://movie.douban.com/subject/26599625/all_photos',
		'https://movie.douban.com/subject/26599625/photos?type=S',

		'https://movie.douban.com/tag/%E6%83%8A%E6%82%9A',
		'https://movie.douban.com/subject/3011051/',
		'https://movie.douban.com/subject/3011051/photos?type=S',
		'https://movie.douban.com/celebrity/1054442/',
		'https://movie.douban.com/celebrity/1054442/photos/',
		'https://movie.douban.com/subject/1307332/',
		'https://movie.douban.com/subject/1307332/photos?type=S',
	]

	rules = [
		Rule(LinkExtractor(allow=('/tag/$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+/?$')), follow=True),
		Rule(LinkExtractor(allow=('/tag/[^/]+\?start=\d+&type=T$')), follow=True),
		Rule(LinkExtractor(allow=('/subject/\d+/\?from=subject-page$')), follow=True),
		Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/$'))),

		Rule(LinkExtractor(allow=('/subject/\d+/all_photos$')), follow=True),
		Rule(LinkExtractor(allow=('/subject/\d+/photos$')), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=('/subject/\d+/photos\?type=S$')), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=('/subject/\d+/photos\?type=S&start=\d+&sortby=vote&size=a&subtype=a$')), follow=True, callback='parse_image'),

		Rule(LinkExtractor(allow=('/celebrity/\d+/?$')), follow=True),
		Rule(LinkExtractor(allow=('/celebrity/\d+/\?from=showing$')), follow=True),
	]
	
	def parse_image(self, response):
		mid = response.url.split('/')[4]
		urls = response.xpath("//div[@class='cover']/a/img/@src").extract()
		for url in urls:
			i = ImageItem()
			i['typ'] = 'image'
			i['mid'] = mid
			i['url'] = url.replace('thumb','photo')
			yield i