# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from moji.items import ImageItem

class ImageSpider(CrawlSpider):
	name = u'moji'
	allowed_domains = [
		'moji.com',
	]
	start_urls = [
		'http://tianqi.moji.com/liveview',
	]

	rules = [
		Rule(LinkExtractor(allow=r'https://www.moji.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://tianqi.moji.com'), follow=True),
		Rule(LinkExtractor(allow=r'/liveview/picture/\d+$'), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=r'/liveview/china/[^/]+/[^/]+'), callback='parse_info',follow=True),
		Rule(LinkExtractor(allow=r'/liveview/china/[^/]+'), follow=True),
	]

	def parse_image(self, response):
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		
		item = ImageItem()
		item['typ'] = u'image'
		item['pid'] = response.url.split('/')[-1]
		# item['country'] = self.get_(response)
		# item['province'] = self.get_(response)
		# item['district'] = self.get_(response)
		item['location'] = self.get_location(response)
		# item['lon'] = self.get_(response)
		# item['lat'] = self.get_(response)
		item['ptime'] = self.get_ptime(response)
		item['pname'] = self.get_pname(response)
		item['url'] = self.get_url(response)
		yield item

	# def get_pid(self, response):
	# 	return response.url.split('/')[-1]

	# def get_country(self, response):
	# 	return response.xpath().extract()[0]

	# def get_province(self, response):
	# 	return response.xpath().extract()[0]

	# def get_district(self, response):
	# 	return response.xpath().extract()[0]

	def get_location(self, response):
		return response.xpath('//div[@id="picture_info_addr"]/text()').extract()[0]

	# def get_(self, response):
	# 	return response.xpath().extract()[0]

	# def get_(self, response):
	# 	return response.xpath().extract()[0]

	def get_ptime(self, response):
		return response.xpath('//p[@id="picture_info_date"]/text()').extract()[0]

	def get_pname(self, response):
		url =  response.xpath('//div[@class="scenery_image_detail"]/img/@src').extract()[0]
		return url.split('/')[-1]

	def get_url(self, response):
		return response.xpath('//div[@class="scenery_image_detail"]/img/@src').extract()[0]


	def parse_info(self, response):
		arr = response.xpath("//div[@class='crumb clearfix']/ul/li/a/text()").extract()
		if len(arr) >= 3:
			country = arr[1].strip()
			province= arr[2].strip()
			district= response.xpath("//div[@class='crumb clearfix']/ul/li/text()").extract()[-1].strip()

			urls = response.xpath("//div[@id='scenery_list']/ul/li/a/@href").extract()
			for url in urls:
				item = ImageItem()
				item['typ'] = 'info'
				item['pid'] = url.split('/')[-1]
				item['country'] = country
				item['province']= province
				item['district'] = district

				#yield item

