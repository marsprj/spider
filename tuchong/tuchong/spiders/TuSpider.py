# -*- coding: utf-8 -*-

import string
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from tuchong.items import TuItem

#create table zh_answer (id int auto_increment, aid int, qid int, title varchar(128), author varchar(32), upvote varchar(16), issue varchar(32), content text, primary key(id));


class TuSpider(CrawlSpider):
	name = 'tu'
	allowed_domains = ['tuchong.com','taobao.com']
	start_urls = [
		#'https://www.tuchong.com/explore',
		#'https://tuchong.com/1466846/',
		u'https://tuchong.com/tags/%E4%BA%BA%E5%83%8F/'，
		u'https://tuchong.com/1287992/13331141/',
		u'https://tuchong.com/287158/13325154/',
		u'https://tuchong.com/395783/13325515/',
		u'https://tuchong.com/tags/%E4%BA%BA%E6%96%87/',
		u'https://tuchong.com/tags/%E5%85%89%E5%BD%B1/',
		u'https://tuchong.com/tags/%E7%A7%81%E6%88%BF/',
		u'https://tuchong.com/tags/%E9%9D%92%E6%98%A5/',
		u'https://tuchong.com/1451143/13244588/',
		u'https://tuchong.com/tags/%E8%8D%89%E5%8E%9F/',
		u'https://tuchong.com/tags/%E6%99%AF%E8%A7%82/',
		u'https://tuchong.com/tags/%E9%9B%A8/',
		u'https://tuchong.com/photos/recent/',
		u'https://tuchong.com/tags/%E6%8A%93%E6%8B%8D',
		u'https://tuchong.com/tags/%E5%B9%BF%E5%B7%9E/',
		u'https://tuchong.com/tags/%E5%B0%91%E5%A5%B3/',
		u'https://tuchong.com/tags/%E7%BE%8E%E5%A5%B3/',
		#u'https://tuchong.com/tags/%E4%BA%BA%E5%83%8F/',
	]

	rules = (
		Rule(LinkExtractor(allow=r'https://www.tuchong.com/'), follow=True),
		Rule(LinkExtractor(allow=r'https://www.tuchong.com/explore$'), follow=True),
		Rule(LinkExtractor(allow=r'/tags/\d+/$'), follow=True),	
		Rule(LinkExtractor(allow=r'/categories/subject/\?page=\d+/$'), follow=True),	
		Rule(LinkExtractor(allow=r'/\d+/\d+/'), follow=True, callback='parse_image'),
		Rule(LinkExtractor(allow=r'/\d+/$'), follow=True, callback='parse_0')
		https://tuchong.com/categories/subject/?page=5
	)

	def parse_0(sefl, response):
		print "!!!!!!##############################"
		print response.url 

	def parse_image(self, response):
		print "sssssssssssssssssssssssssssssssssssssssssssssssssssss"
		if self.is_taget(response):
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

	def is_taget(self, response):
		#arr = response.xpath(u"//a[text()='花卉'] or //a[text()='']").extract()
		#arr = response.xpath(u"//a[text()='花卉']").extract()
		arr = response.xpath(u"//a[@class='tag' and (text()='美女' or text()='少女')]").extract()
		if any(arr):
			print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
			print len(arr)
			print ','.join(arr)
		else:
			print "))))))))))))))))))))))))))))))))"
		return True if any(arr) else False
