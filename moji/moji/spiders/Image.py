# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ImageSpider(CrawlSpider):
	name = u'image'
	allowed_domains = ['moji.com']
	start_urls = [
		'http://tianqi.moji.com/liveview',
	]

	rules = [
		Rule(LinkExtractor(allow=r'https://www.moji.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://tianqi.moji.com'), follow=True),
		Rule(LinkExtractor(allow=r'/liveview/picture/\d+$'), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=r'/liveview/china/[^/]+'), follow=True),
		Rule(LinkExtractor(allow=r'/liveview/china/[^/]+/[^/]+'), callback='parse_people',follow=True),
	]

	def parse_image(self, response):
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print response.url

	def parse_people(self, response):
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		print response.url
