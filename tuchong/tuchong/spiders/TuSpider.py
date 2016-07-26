# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tuchong.items import TuItem

#create table zh_answer (id int auto_increment, aid int, qid int, title varchar(128), author varchar(32), upvote varchar(16), issue varchar(32), content text, primary key(id));


class TuSpider(CrawlSpider):
	name = 'tu'
	allowed_domains = ['tuchong.com']
	start_urls = [
		#'https://www.tuchong.com/explore',
		'https://tuchong.com/1466846/',
	]

	rules = (
		Rule(LinkExtractor(allow=r'https://www.tuchong.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://www.tuchong.com/explore$'), follow=True),
		Rule(LinkExtractor(allow=r'/tags/\d+/$'), follow=True),		
		Rule(LinkExtractor(allow=r'/\d+/\d+/'), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=r'/\d+/$'), follow=True, callback='parse_0')
	)

	def parse_0(sefl, response):
		print "!!!!!!##############################"
		print response.url 

	def parse_image(self, response):
		print "sssssssssssssssssssssssssssssssssssssssssssssssssssss"
		t = TuItem()
		t['author'] = self.get_author(response)
		t['subject'] = self.get_subject(response)
		t['subject_id'] = self.get_subject(response)
		t['url'] = self.get_url(response)
    
		yield t

	def get_author(self,response):
		#return response.xpth()
		return ''

	def get_subject(self,response):
		#return response.xpth()
		return ''

	def get_subject_id(self,response):
		#return response.xpth()
		return ''

	def get_url(self,response):
		arr = response.xpath('//section/@data-pic').extract()
		return arr[0] if any(arr) else u''
