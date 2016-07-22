# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from zhihu.items import TopicItem


class TopicSpider(CrawlSpider):
	name = 'topic'
	allowed_domains = ['zhihu.com']
	start_urls = [
#		'https://www.zhihu.com/explore',
		'https://www.zhihu.com/question/41351785',
#		'https://www.zhihu.com/topic',
	]

	rules = (
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://www.zhihu.com/explore$'), follow=True),
		Rule(LinkExtractor(allow=r'/topic/\[^\]+'), callback='parse_topic'),
#		Rule(LinkExtractor(allow=r'/topic/\d+$'), callback='parse_topic'),
#		Rule(LinkExtractor(allow=r'/topic/\d+/hot'), callback='parse_topic'),
#		Rule(LinkExtractor(allow=r'/question/\d+$'), follow=True),
#		Rule(LinkExtractor(allow=r'/question/\d+/answer/\d+'), follow=True),
	)

	def parse_topic(self, response):
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		t = TopicItem()
		t['typ'] = u'topic'
		t['title'] = response.xpath('//h1[@class="zm-editable-content"]/text()').extract()
		t['description'] = response.xpath('//div[@class="zm-editable-content"]/text()').extract()
 		t['parent'] = self.format_parents(response.xpath('//div[@id="zh-topic-side-parents-list"]/div/div/a/@href').extract())
		t['tid'] = self.get_topic_id(response.url)
		
		yield t


	def parse_question(self, response):
		links = response.xpath("//a[@class='zm-item-tag']")
		for link in links:		
			t = TopicItem()
			t['tid'] = link.xpath('@href').extract()[0].strip().split('/')[-1]
			t['title'] = link.xpath('text()').extract()[0]
			print t['tid']
			yield t

	def format_parents(self, parents):
		pids = [e.split('/')[-1] for e in parents]
		return ','.join(pids)

	def get_topic_id(self, url):
		if url[-3:] == 'hot':
			tid = response.url.split('/')[-2]
		else:
			tid = response.url.split('/')[-1]
		return tid	
